# Plan Wdrożenia i Testów (Cyfrowy Księgozbiór)

Poniższy plan został zaprojektowany, aby bezpiecznie i krok po kroku wdrożyć architekturę `Metadata First` oraz zautomatyzowanych Agentów AI bez ryzyka utraty lub uszkodzenia dotychczasowych zbiorów.

---

## Faza 1: Przygotowanie Środowiska Bazowego (Piaskownica)
Zanim uruchomimy automatyzacje na docelowym księgozbiorze, tworzymy bezpieczne środowisko testowe (Sandbox).

1. **Google Drive Sandbox:**
   - Utwórz folder `Books_Test` na swoim Dysku Google.
   - W folderze utwórz ręcznie szkielet: `_Inbox`, `archiwum/system`, `archiwum/stare_formaty`, `Fiction`, `Non-Fiction`.
   - Skopiuj tam wygenerowany plik `Zasady-katalogowania-ksiazek.md`.
2. **Klucze i Autoryzacja:**
   - Skonfiguruj projekt w **Google Cloud Console**.
   - Wygeneruj klucze Service Account (plik `.json`) i nadaj im uprawnienia (Editor) do folderu `Books_Test` (oraz docelowo `Books`).
3. **Środowisko lokalne:**
   - Zainstaluj testową, czystą bibliotekę w Calibre (aby nie zabrudzić głównej kolekcji podczas prób integracji metadanych).
   - Skonfiguruj środowisko Python (zalecane: `venv`), zainstaluj pakiety `google-api-python-client` oraz biblioteki do łączenia z API Gemini.

---

## Faza 2: Wdrożenie Skryptów i Agentów w Piaskownicy
1. **Agent 1 (Inicjalizacja i Zasady):**
   - Wdrożenie skryptu Python odbierającego stan folderu Drive i pytającego API Gemini z wcześniej przygotowanym **Promptem Systemowym**.
   - Skonfigurowanie harmonogramu (Cron w Linux/Mac, Harmonogram zadań w Windows) na `23:00` tylko dla folderu testowego.
2. **Agent 2 (Monitoring i Synchronizacja):**
   - Wdrożenie drugiego skryptu, który skanuje strukturę i deleguje analizę wykrytych plików do modelu AI.
   - Ustawienie harmonogramu generowania pliku `Lista-katalogowa-ksiazek.csv` na `23:30`.
3. **Zasilenie plikami testowymi:**
   - Wrzuć do `Books_Test/_Inbox` oraz do folderów testowych następujący pakiet:
     - Plik 1: `Dobry_Wzorzec_Jan_Kowalski.epub` (idealny).
     - Plik 2: `Zła nazwa ze spacjami i ąę (Janusz).mobi` (źle nazwany i zły format).
     - Plik 3: `Wykresy.pdf` (format dozwolony).
     - Plik 4: `Stary_Dokument_Ktos.doc` (format wycofany).

---

## Faza 3: Scenariusze Testowe (Quality Assurance & UAT)

Gdy środowisko testowe jest gotowe i uruchomione, przeprowadzamy 4 główne scenariusze testowe, które zwalidują logikę.

### Test 1: Mechanizm Kopii Zapasowej (Agent 1)
- **Działanie:** Dokonaj ręcznej (celowo lekko błędnej) modyfikacji w pliku `Zasady-katalogowania-ksiazek.md` na Dysku. Uruchom Agenta 1 ręcznie.
- **Oczekiwany rezultat:** 
  1. Agent tworzy nową wersję w głównym folderze.
  2. W folderze `Books_Test/archiwum/system/` ląduje plik z dodanym timestampem w nazwie (np. `Zasady..._20260915_2300.md`) chroniący starą wersję.
- **Kryterium sukcesu:** Plik backupu pojawia się *przed* wygenerowaniem nowego pliku zasad.

### Test 2: Sanitacja i Formatowanie Nazw (Agent 2)
- **Działanie:** Uruchom Agenta 2. Obserwuj jak przetwarza "Plik 2" (`Zła nazwa ze spacjami i ąę (Janusz).mobi`).
- **Oczekiwany rezultat:** 
  1. Na nowej liście `Lista-katalogowa-ksiazek.csv` tytuł i autor zostają odseparowane. 
  2. Zostaje wydana rekomendacja usunięcia spacji i polskich znaków.
- **Kryterium sukcesu:** Brak polskich znaków i zachowanie formatu `Tytul_Autor` na liście.

### Test 3: Identyfikacja Formatów i Status Konwersji (Agent 2)
- **Działanie:** Analiza wyjściowego pliku CSV.
- **Oczekiwany rezultat:**
  - `Dobry_Wzorzec` oraz `Wykresy.pdf` otrzymują status **Zostaw**.
  - `Zła nazwa` (.mobi) oraz `Stary_Dokument` (.doc) otrzymują jednoznaczny status **Konwertuj**.
- **Kryterium sukcesu:** W pliku CSV widnieje czytelna kolumna ze statusem "Konwertuj" dla przestarzałych formatów, umożliwiając szybkie odfiltrowanie w zewnętrznym narzędziu.

### Test 4: Zgodność z Calibre (Manualna i systemowa)
- **Działanie:** Zaimportuj wygenerowany plik `Lista-katalogowa-ksiazek.csv` do pustej testowej bazy Calibre używając funkcji "Dodaj puste książki na podstawie listy" (z wtyczką CSV Import lub wbudowanym narzędziem).
- **Oczekiwany rezultat:** Powstają nowe wpisy poprawnie identyfikujące Tytuł, Autora i unikalne Tagi.
- **Kryterium sukcesu:** Bezawaryjny import bez rozbitych metadanych.

---

## Faza 4: Wdrożenie Produkcyjne (Migracja)

Po pozytywnym zaliczeniu wszystkich testów w Piaskownicy:
1. **Zamrożenie edycji:** Wstrzymaj dodawanie nowych książek do prawdziwego folderu `Books`.
2. **Kopia bezpieczeństwa (One-time Backup):** Wykonaj lokalną kopię całego oryginalnego folderu `Books` w bezpieczne miejsce na dysku fizycznym na wypadek zdarzeń nieprzewidzianych.
3. **Przepięcie agentów:** Zmień w kodzie agentów folder z `Books_Test` na docelowy `Books`.
4. **Rozruch (Pierwsze Skanowanie):**
   - Pierwsze skanowanie może potrwać znacznie dłużej niż zwykle z uwagi na dużą liczbę plików.
   - Monitoruj logi na żywo.
5. **Sukces!** – System przechodzi w stan działania ciągłego z codziennym monitorowaniem o 23:00 i 23:30.
