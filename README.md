# 📚 Architekt Cyfrowego Księgozbioru (Digital Library AI Agents)

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![AI](https://img.shields.io/badge/Google_Gemini-3.6-orange)

Autonomiczny system automatyzacji, sanitacji i inwentaryzacji cyfrowego księgozbioru zlokalizowanego na Google Drive, zintegrowany z **Google Gemini API** oraz oprogramowaniem **Calibre**.

Projekt realizuje koncepcję **`Metadata First`** – priorytetem są ustandaryzowane metadane oraz czystość bazy danych, z zachowaniem pomocniczej struktury folderów fizycznych.

---

## 🚀 Główne Funkcjonalności

- 🤖 **Agent 1 (Architekt Zasad):** Odpowiada za analizę i ewolucję wytycznych katalogowania (`Zasady-katalogowania-ksiazek.md`) z wykorzystaniem Gemini AI, dbając o zgodność ze standardami **IFLA ICP (2016)** oraz **Biblioteki Narodowej**.
- 🧹 **Agent 2 (Monitoring & Sanitacja Nazw):** Przeszukuje rekursywnie całe drzewo folderów (bez ograniczeń zagnieżdżenia), fizycznie czyści nazwy plików i podfolderów (transliteracja polskich diakrytyków `POLISH_MAP`, zmiana spacji i myślników na `_`, usuwanie prefiksów/sufiksów pobierania).
- 📦 **Detekcja i Archiwizacja Duplikatów:** Automatycznie wykrywa powtarzające się pozycje (np. z dopiskami `(1)`, `kopia`) i przenosi je do bezpiecznego archiwum.
- 📊 **Inwentaryzacja (.CSV):** Generuje i aktualizuje plik `Lista-katalogowa-ksiazek.csv` zawierający Tytuł, Autora, Opis, Format, Status konwersji i bezpośredni link do Google Drive.
- ⚡ **Wydajność & Zero Quota Errors:** Hybrydowy algorytm sanitacji w lokalnym Pythonie eliminuje ryzyko przekroczenia darmowych limitów zapytań (Quota 429).

---

## 🛠️ Architektura Systemu

```text
[ Google Drive / Chmura ]
        │
        ├── Agent 1 ──> Ewolucja Zasad (Gemini AI + IFLA ICP 2016) + Backup
        │
        └── Agent 2 ──> Skanowanie Rekursywne (Wszystkie zagnieżdżenia)
                          ├── Sanitacja Nazw Plików & Podfolderów (POLISH_MAP + Regex)
                          ├── Automatyczna Detekcja i Archiwizacja Duplikatów
                          └── Inwentaryzacja w pliku CSV dla Calibre
```

---

## 📋 Szybki Start

### 1. Wymagania i Konfiguracja
1. Sklonuj repozytorium:
   ```bash
   git clone https://github.com/BartoszRadziszewski/Architekt_Cyfrowego_Ksiegozbioru.git
   cd Architekt_Cyfrowego_Ksiegozbioru
   ```
2. Zainstaluj zależności:
   ```bash
   pip install -r requirements.txt
   ```
3. Skopiuj szablon `.env.example` do `.env`:
   ```bash
   cp .env.example .env
   ```
4. Uzupełnij identyfikatory folderów Google Drive oraz klucz `GEMINI_API_KEY` w pliku `.env`.
5. Umieść pobrany z Google Cloud klucz Service Account pod nazwą `service_account.json`.

### 2. Uruchomienie
```bash
python run_agents.py
```

---

## 📄 Dokumentacja Projektowa

W repozytorium znajdują się szczegółowe dokumenty projektowe:
- [Opis Architektury](ARCHITECTURE.md)
- [Specyfikacja Systemowa i Prompty](PROMPT.md)
- [Plan Wdrożenia i Testów UAT](DEPLOYMENT.md)

---

## 📜 Licencja

Projekt udostępniany jest na licencji **MIT** - patrz plik [LICENSE](LICENSE).

Autorem projektu jest **Bartosz Radziszewski** ([GitHub Profile](https://github.com/BartoszRadziszewski)).
