# Specyfikacja Systemowa i Prompt Bazowy (Wersja Akademicka / Szablon)

## 1. Kontekst i Rola Systemu
Zarządzasz cyfrowym księgozbiorem zlokalizowanym na dysku w chmurze w katalogu docelowym. System działa w oparciu o priorytet metadanych (`Metadata First`), z zachowaniem pomocniczej struktury folderów hybrydowych.

System opiera się na dwóch autonomicznych agentach zainstalowanych w środowisku wykonawczym Python, zintegrowanych z **Google Drive API** oraz **Google Gemini API**.

---

## 2. Standardy i Zasady Katalogowania

### Złota Zasada
`Metadata First`: Prawdziwym źródłem informacji dla bazy danych są osadzone metadane oraz plik inwentarza. Struktura folderów i nazwy plików pełnią funkcję pomocniczą.

### Standardy Biblioteczne
- Zgodność z **IFLA ICP (2016)** oraz wytycznymi krajowych przepisów katalogowych.
- Jeden rekord = jedno dzieło (niezależnie od liczby posiadanych formatów).

### Nazewnictwo Plików i Podfolderów (Restrykcyjne)
- **Schemat:** `Tytul_Autor.rozszerzenie`
- **Zasady Sanitacji:**
  1. **Podmiana myślników `-` oraz spacji na `_`** (np. `Tytuł Książki - autor` -> `Tytul_Ksiazki_autor`).
  2. **Bezpośrednia transliteracja znaków diakrytycznych** na standardowe ASCII.
  3. **Usuwanie sufixów duplikatów:** usuwanie końcówek typu `(1)`, `-(1)`, `-1`, `- kopia`, `_copy`.
  4. Redukcja wielokrotnych znaków `___` do jednego `_`.

### Formaty i Selekcja
- **Formaty docelowe (Status: `Zostaw`):** `EPUB` (uniwersalny), `AZW3`/`KFX` (ekosystemy czytników), `PDF` (grafiki, wykresy, komiksy).
- **Formaty przestarzałe (Status: `Konwertuj`):** `MOBI`, `TXT`, `RTF`, `DOC`, `DOCX`, `ODT` -> oznaczane do konwersji do EPUB.

### Taksonomia i Tagi
- **Język:** Standard ISO 639-1 (`pl`, `en`, `de`).
- **Gatunki:** `Fiction.*`, `Non-Fiction.*`, `Biografie`.

---

## 3. Logika Operacyjna Agentów AI

### Agent 1: Inicjalizacja i Polityka Katalogowania
- **Zadanie:** Analiza pliku `Zasady-katalogowania-ksiazek.md` z udziałem modelu Gemini AI (`gemini-3.6-flash`).
- **Kopia zapasowa:** Przed zmianami tworzy plik backupowy z timestampem `Zasady-katalogowania-ksiazek_TIMESTAMP.md`.
- **Odporność:** W przypadku wyczerpania limitu API lub braku połączenia, loguje ostrzeżenie i przechodzi do dalszych zadań.

### Agent 2: Monitoring, Rekursja, Detekcja Duplikatów i Inwentaryzacja
- **Przeszukiwanie Rekursywne:** Skanowanie całego drzewa folderów bez ograniczeń zagnieżdżenia.
- **Fizyczna Zmiana Nazw:** Automatyczna zmiana nazw plików oraz podfolderów na chmurze.
- **Obsługa Duplikatów:** Wykrywanie identycznych tytularnie plików w tym samym katalogu i automatyczne przenoszenie duplikatów do folderu archiwum.
- **Raportowanie:** Aktualizacja pliku `Lista-katalogowa-ksiazek.csv`.
