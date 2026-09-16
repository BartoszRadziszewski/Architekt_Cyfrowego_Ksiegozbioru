import datetime
import src.config as config
from src.drive_api import DriveService
from src.gemini_api import GeminiService

def run_agent1():
    print("Rozpoczęcie pracy Agenta 1 (Zasady)...")
    config.verify_config()
    
    drive = DriveService()
    gemini = GeminiService()

    # Szukamy aktualnego pliku zasad
    rules_file = drive.find_file_by_name(config.DRIVE_BOOKS_FOLDER_ID, config.RULES_FILENAME)
    
    if not rules_file:
        print(f"Brak pliku {config.RULES_FILENAME} w folderze docelowym. Wymagana ręczna inicjalizacja (lub przywrócenie).")
        return

    # 1. Pobranie obecnych zasad
    print("Pobieranie obecnych zasad...")
    current_rules = drive.download_file(rules_file['id'])

    context = "Brak nowych nietypowych formatów. Zweryfikuj i zoptymalizuj obecne reguły."
    
    # 2. Analiza Gemini
    print("Analiza zasad z udziałem AI...")
    try:
        updated_rules = gemini.analyze_rules(current_rules, context)
    except Exception as e:
        print(f"[Ostrzeżenie] Nie można przeanalizować zasad przez AI ({e}). Pomijam aktualizację zasad...")
        return

    if updated_rules and updated_rules != current_rules:
        # 3. Kopia zapasowa
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{config.RULES_FILENAME.replace('.md', '')}_{timestamp}.md"
        print(f"Tworzenie kopii zapasowej: {backup_name}...")
        try:
            drive.upload_file(backup_name, current_rules, config.DRIVE_ARCHIVE_SYSTEM_FOLDER_ID, mime_type="text/markdown")
        except Exception as e:
            print(f"[Info] Kopia zapasowa w archiwum pominięta ({e}). Nadpisuję plik główny.")

        # 4. Nadpisanie głównych zasad (UPDATE na istniejącym pliku)
        print("Nadpisywanie zaktualizowanych zasad...")
        drive.upload_file(config.RULES_FILENAME, updated_rules, config.DRIVE_BOOKS_FOLDER_ID, mime_type="text/markdown")
        print("Zasady zostały zaktualizowane pomyślnie.")
    else:
        print("AI uznało, że zasady nie wymagają modyfikacji.")

if __name__ == "__main__":
    run_agent1()
