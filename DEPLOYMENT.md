# Plan Wdrożenia i Testów

Podręcznik opisujący krok po kroku uruchomienie, testowanie oraz utrzymanie zautomatyzowanego księgozbioru cyfrowego.

---

## 1. Konfiguracja Środowiska (Krok po Kroku)

### A. Wstępne Przygotowanie na Dysku w Chmurze
1. Stwórz główny katalog biblioteczny (np. `Katalog_Glowny` lub `Katalog_Testowy`).
2. Stwórz podfoldery dla archiwum: `archiwum/system` oraz `archiwum/stare_formaty`.
3. **Krok Wstępny:** Utwórz i wgraj dwa pliki startowe do głównego folderu:
   - `Zasady-katalogowania-ksiazek.md`
   - `Lista-katalogowa-ksiazek.csv` (pusty plik tekstowy o tej nazwie).

### B. Konfiguracja Usług Chmurowych (GCP Service Account)
1. Utwórz nowy projekt w konsoli chmurowej (np. `Projekt-Katalog-AI`).
2. Włącz interfejs **Google Drive API**.
3. Utwórz Konto Usługi (Service Account), przejdź do zakładki **Klucze** i pobierz klucz w formacie **JSON**.
4. Zapisz plik jako `service_account.json` w katalogu ze skryptami.
5. Skopiuj adres e-mail konta usługi (np. `service-account-name@project-id.iam.gserviceaccount.com`).
6. **Udostępnij katalog biblioteczny** temu adresowi e-mail z uprawnieniami **Edytor** (odznacz opcję wysyłania powiadomienia mailowego).

### C. Konfiguracja Gemini API Key
1. Wygeneruj klucz API w konsoli dostawcy modeli językowych (`GEMINI_API_KEY`).

### D. Plik Konfiguracyjny (.env)
Utwórz plik `.env` i uzupełnij go szablonowymi zmiennymi (identyfikatory pozyskiwane z adresu URL folderu):
```env
GOOGLE_APPLICATION_CREDENTIALS=service_account.json
DRIVE_BOOKS_FOLDER_ID=TUTAJ_ID_GLOWNEGO_FOLDERU
DRIVE_ARCHIVE_SYSTEM_FOLDER_ID=TUTAJ_ID_ARCHIWUM_SYSTEM
DRIVE_ARCHIVE_OLD_FORMATS_FOLDER_ID=TUTAJ_ID_ARCHIWUM_STARE_FORMATY
GEMINI_API_KEY=TUTAJ_KLUCZ_API_GEMINI
```

---

## 2. Instalacja i Uruchomienie

1. Otwórz terminal w katalogu projektu:
   `C:\sciezka\do\projektu`
2. Zainstaluj biblioteki:
   ```bash
   pip install -r requirements.txt
   ```
3. Uruchom agentów:
   ```bash
   python run_agents.py
   ```

---

## 3. Scenariusze Testowe (Quality Assurance)

| Test | Opis Scenariusza | Oczekiwany Rezultat | Status |
| :--- | :--- | :--- | :--- |
| **Test 1** | Modyfikacja zasad przez Agenta 1 | Zaktualizowany plik zasad w chmurze + backup z timestampem. | ZALICZONY |
| **Test 2** | Skanowanie rekursywne podfolderów | Przetworzenie plików na dowolnej głębokości (np. `Kategoria/Podkategoria`). | ZALICZONY |
| **Test 3** | Sanitacja nazw i podfolderów | Fizyczna zamiana spacji, myślników i polskich znaków na `_`. | ZALICZONY |
| **Test 4** | Detekcja i przenoszenie duplikatów | Wykrycie powtórzeń `(1)`, `kopia` i przeniesienie ich do archiwum. | ZALICZONY |
| **Test 5** | Generowanie Inwentarza CSV | Bezawaryjna aktualizacja `Lista-katalogowa-ksiazek.csv`. | ZALICZONY |

---

## 4. Wnioski Eksploatacyjne

- **Błędy uprawnień Service Accounts:** Konta robocze nie posiadają własnego limity pamięci. Należy korzystać z operacji `UPDATE` na plikach stworzonych wcześniej przez właściciela lub korzystać z dysków współdzielonych.
- **Optymalizacja wydajnościowa:** Wykorzystanie lokalnych wyrażeń regularnych i tabel transliteracji znaków redukuje czas analizy i chroni przed przekraczaniem darmowych limitów zapytań (Quota 429).
