# Opis Projektu: Architekt Cyfrowego Księgozbioru i Inżynier Automatyzacji AI (Wersja Akademicka)

## 1. Wstęp i Wizja Projektu
Projekt **"Architekt Cyfrowego Księgozbioru"** to kompleksowy, zautomatyzowany system katalogowania, sanitacji i inwentaryzacji wielojęzycznych cyfrowych zasobów literackich i naukowych zlokalizowanych w chmurze (Google Drive). 

System został zaprojektowany w paradygmacie **`Metadata First`** – priorytetem są ustandaryzowane metadane zsynchronizowane z systemami bibliotecznymi (np. **Calibre**), podczas gdy fizyczna struktura folderów pełni rolę pomocniczą (model hybrydowy).

---

## 2. Architektura i Kluczowe Komponenty Systemu

System wykorzystuje moduły Pythona integrujące się z chmurą danych poprzez API oraz z wielomodalnymi modelami językowymi z rodziny **Google Gemini**.

```text
[ Chmura Danych / Google Drive ]
        │
        ├── Agent 1 ──> Analiza i Ewolucja Zasad Katalogowania (Gemini AI + IFLA ICP 2016)
        │
        └── Agent 2 ──> Rekursywne Skanowanie Drzewa Katalogów (Dowolne zagnieżdżenie)
                          ├── Sanitacja Nazw Plików i Podfolderów (POLISH_MAP + Regex)
                          ├── Automatyczna Detekcja i Archiwizacja Duplikatów
                          └── Generowanie Inwentarza (.CSV dla bazy danych)
```

### A. Agent 1: Architekt Zasad i Inicjalizacja
* **Rola:** Utrzymanie i ewolucja zasad katalogowania (`Zasady-katalogowania-ksiazek.md`).
* **Model AI:** Google Gemini API (`gemini-3.6-flash`).
* **Funkcja:** Odczytuje zasady, analizuje nowe zdarzenia biblioteczne, zapewnia zgodność ze standardami **IFLA ICP (2016)** oraz wytycznymi **Bibliotek Narodowych**, proponując optymalizacje.
* **Bezpieczeństwo:** Tworzenie historycznych kopii zapasowych zasad przed każdą modyfikacją.

### B. Agent 2: Monitoring, Sanitacja, Detekcja Duplikatów i Inwentaryzacja
* **Rola:** Strażnik spójności fizycznej w chmurze oraz generator inwentarza.
* **Skanowanie Rekursywne:** Przeszukiwanie całego drzewa folderów bez ograniczeń zagnieżdżenia (przechodzenie wszerz / BFS).
* **Fizyczna Sanitacja Nazw (Pliki i Podfoldery):**
  - **Transliteracja Diakrytyków (`POLISH_MAP`):** Zamiana znaków diakrytycznych na odpowiadające znaki ASCII (rozwiązująca problem braku dekompozycji złożonych liter diakrytycznych).
  - **Ujednolicenie Separatorów:** Zamiana spacji i myślników `-` na podkreślniki `_` oraz redukcja wielokrotnych krotek `___` do jednego `_`.
  - **Czyszczenie Sufiksów Pobierania:** Automatyczne usuwanie znaczników przeglądarek i systemu typu `(1)`, `-(1)`, `-1`, `- kopia`, `_copy`.
* **Detekcja i Archiwizacja Duplikatów:**
  - Jeśli w tym samym katalogu zostanie wykryty drugi plik o tej samej nazwie wzorcowej, Agent 2 identyfikuje go jako **DUPLIKAT**.
  - Zduplikowany plik jest **automatycznie przenoszony do folderu archiwum**, oczyszczając główną bibliotekę.
* **Generowanie Inwentarza (`Lista-katalogowa-ksiazek.csv`):**
  - Generowanie pliku CSV zawierającego: Tytuł, Autor, Opis, Status (`Zostaw` dla EPUB/PDF/AZW3; `Konwertuj` dla MOBI/DOC/TXT), Format oraz bezpośredni identyfikator URI pliku.

---

## 3. Kluczowe Wnioski Inżynieryjne i Dobre Praktyki

1. **Hybrydowa Sanitacja (Wydajność vs Limity API):**
   Przeniesienie czyszczenia nazw na lokalny algorytm deterministyczny w Pythonie eliminuje ryzyko przekroczenia limitów zapytań (Quota 429) i skraca czas wykonywania operacji do milisekund.
2. **Bezpieczne Zarządzanie Kontami Usługi (Service Accounts):**
   Wykorzystanie dedykowanych operacji `UPDATE` na plikach oraz parametrów `supportsAllDrives=True` pozwala na bezawaryjne współdzielenie dysku z kontami robotów bez naruszania limitów dyskowych.
3. **Odporność na Awaryjność (Graceful Degradation):**
   Zabezpieczenie zapytań AI w bloki `try-except` pozwala na nieprzerwaną pracę procesów inwentaryzacji nawet w przypadku chwilowej niedostępności usług zewnętrznych.
