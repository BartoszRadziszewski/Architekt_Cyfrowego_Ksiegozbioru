import datetime
import re
import unicodedata
import pandas as pd
import src.config as config
from src.drive_api import DriveService
from src.gemini_api import GeminiService

POLISH_MAP = str.maketrans("ąćęłńóśźżĄĆĘŁŃÓŚŹŻ", "acelnoszzACELNOSZZ")

def local_clean_filename(filename):
    """Zaawansowana sanitacja nazwy pliku lub folderu z usuwaniem sufixów duplikatów."""
    if '.' in filename:
        parts = filename.rsplit('.', 1)
        name = parts[0]
        ext = f".{parts[1].lower()}"
    else:
        name = filename
        ext = ""

    # 1. Podmiana polskich znaków
    name_clean = name.translate(POLISH_MAP)

    # 2. Awaryjna normalizacja NFKD
    nfkd_form = unicodedata.normalize('NFKD', name_clean)
    name_ascii = "".join([c for c in nfkd_form if not unicodedata.combining(c)])

    # 3. Usuwanie sufixów duplikatów przeglądarki i systemu (' (1)', '-(1)', '-1', '- kopia', '_copy')
    name_ascii = re.sub(r'[\s_\-]*\(\d+\)', '', name_ascii)
    name_ascii = re.sub(r'[\s_\-]+\d+$', '', name_ascii)
    name_ascii = re.sub(r'[\s_\-]*(kopia|copy)\b', '', name_ascii, flags=re.IGNORECASE)

    # 4. Zamiana myślników (-), spacji oraz nie-liter/nie-cyfr na _
    clean_name = re.sub(r'[^\w]', '_', name_ascii)

    # 5. Redukcja wielokrotnych '_' do jednego i usunięcie brzegowych
    clean_name = re.sub(r'_+', '_', clean_name).strip('_')

    return f"{clean_name}{ext}"

def is_valid_name(name):
    """Sprawdza, czy nazwa jest czysta."""
    invalid_chars = " -()ąćęłńóśźżĄĆĘŁŃÓŚŹŻ"
    for char in invalid_chars:
        if char in name:
            return False
    return True

def run_agent2():
    print("Rozpoczęcie pracy Agenta 2 (Monitoring i Detekcja Duplikatów)...")
    config.verify_config()
    
    drive = DriveService()
    gemini = GeminiService()

    # 1. Skanowanie REKURSYWNE drzewa katalogów
    print("Skanowanie plików i podfolderów na wszystkich poziomach...")
    ignore_ids = [config.DRIVE_ARCHIVE_SYSTEM_FOLDER_ID, config.DRIVE_ARCHIVE_OLD_FORMATS_FOLDER_ID]
    all_files, all_folders = drive.list_files_and_folders_recursive(config.DRIVE_BOOKS_FOLDER_ID, ignore_folder_ids=ignore_ids)
    
    # 2. Sanitacja samych NAZW PODFOLDERÓW
    for folder in all_folders:
        foldername = folder.get('name')
        if not is_valid_name(foldername):
            clean_foldername = local_clean_filename(foldername)
            print(f"Zmieniam nazwę PODFOLDERU: '{foldername}' -> '{clean_foldername}'")
            try:
                drive.rename_file(folder['id'], clean_foldername)
            except Exception as e:
                print(f"[Ostrzeżenie] Błąd zmiany nazwy podfolderu ({e})")

    # 3. Sanitacja PLIKÓW + Detekcja i Przenoszenie Fizycznych Duplikatów
    data = []
    seen_files_per_folder = {}  # {parent_folder_id: set(clean_filenames)}
    
    for f in all_files:
        filename = f.get('name')
        parent_id = f.get('parents', [config.DRIVE_BOOKS_FOLDER_ID])[0]
        
        if parent_id not in seen_files_per_folder:
            seen_files_per_folder[parent_id] = set()
        
        # Filtrujemy pliki systemowe
        if filename in [config.RULES_FILENAME, config.LIST_FILENAME]:
            continue
            
        clean_name = local_clean_filename(filename) if not is_valid_name(filename) else filename
        
        # SPRAWDZENIE CZY TO DUPLIKAT
        if clean_name in seen_files_per_folder[parent_id]:
            print(f"[Wykryto Duplikat] Plik '{filename}' jest kopią '{clean_name}'. Przenoszę do archiwum...")
            status = "Duplikat - Zarchiwizowano"
            try:
                drive.move_file(f['id'], current_parent_id=parent_id, new_parent_id=config.DRIVE_ARCHIVE_OLD_FORMATS_FOLDER_ID)
            except Exception as e:
                print(f"[Ostrzeżenie] Nie udało się przenieść duplikatu ({e})")
        else:
            # Rejestrujemy nową unikalną pozycję
            seen_files_per_folder[parent_id].add(clean_name)
            
            # Zmiana nazwy jeśli była niepoprawna
            if not is_valid_name(filename):
                print(f"Zmieniam nazwę PLIKU na Dysku: '{filename}' -> '{clean_name}'")
                try:
                    drive.rename_file(f['id'], clean_name)
                    filename = clean_name
                except Exception as e:
                    print(f"[Ostrzeżenie] Błąd zmiany nazwy pliku ({e})")
                    
            format_ext = filename.split('.')[-1].lower() if '.' in filename else ""
            status = "Zostaw" if format_ext in ['epub', 'pdf', 'azw3', 'kfx'] else "Konwertuj"

        format_ext = filename.split('.')[-1].lower() if '.' in filename else ""
        link = f"https://drive.google.com/file/d/{f['id']}/view"
        clean_base = filename.replace('.'+format_ext, '') if format_ext else filename
        parts = clean_base.split('_')
        title = parts[0] if len(parts) > 0 else "Nieznany"
        author = " ".join(parts[1:]) if len(parts) > 1 else "Nieznany"

        data.append({
            "Tytuł": title,
            "Autor": author,
            "Opis": "Generowane przez System",
            "Status": status,
            "Format": format_ext.upper(),
            "Link": link
        })

    if not data:
        print("Brak odpowiednich książek do przetworzenia.")
        return

    # Generowanie pliku CSV
    df = pd.DataFrame(data)
    csv_content = df.to_csv(index=False)
    
    # Kopia zapasowa starej listy
    old_list = drive.find_file_by_name(config.DRIVE_BOOKS_FOLDER_ID, config.LIST_FILENAME)
    if old_list:
        try:
            old_csv_content = drive.download_file(old_list['id'])
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"{config.LIST_FILENAME.replace('.csv', '')}_{timestamp}.csv"
            print(f"Zapis kopii archiwalnej: {backup_name}...")
            drive.upload_file(backup_name, old_csv_content, config.DRIVE_ARCHIVE_SYSTEM_FOLDER_ID, mime_type="text/csv")
        except Exception as e:
            print(f"[Info] Kopia zapasowa w archiwum pominięta ({e}). Nadpisuję plik główny.")

    # Wgranie nowej wersji na Drive
    print("Aktualizacja pliku Lista-katalogowa-ksiazek.csv...")
    drive.upload_file(config.LIST_FILENAME, csv_content, config.DRIVE_BOOKS_FOLDER_ID, mime_type="text/csv")
    print("Agent 2 pomyślnie zakończył pracę.")

if __name__ == "__main__":
    run_agent2()
