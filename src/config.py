import os
from dotenv import load_dotenv

# Wczytanie zmiennych środowiskowych z pliku .env
load_dotenv()

# Konfiguracja Google Drive
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
DRIVE_BOOKS_FOLDER_ID = os.getenv("DRIVE_BOOKS_FOLDER_ID")
DRIVE_ARCHIVE_SYSTEM_FOLDER_ID = os.getenv("DRIVE_ARCHIVE_SYSTEM_FOLDER_ID")
DRIVE_ARCHIVE_OLD_FORMATS_FOLDER_ID = os.getenv("DRIVE_ARCHIVE_OLD_FORMATS_FOLDER_ID")

# Konfiguracja Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Nazwy plików systemowych
RULES_FILENAME = "Zasady-katalogowania-ksiazek.md"
LIST_FILENAME = "Lista-katalogowa-ksiazek.csv"

# Weryfikacja
def verify_config():
    missing = []
    if not GOOGLE_APPLICATION_CREDENTIALS: missing.append("GOOGLE_APPLICATION_CREDENTIALS")
    if not DRIVE_BOOKS_FOLDER_ID: missing.append("DRIVE_BOOKS_FOLDER_ID")
    if not GEMINI_API_KEY: missing.append("GEMINI_API_KEY")
    
    if missing:
        raise ValueError(f"Brak krytycznych zmiennych środowiskowych: {', '.join(missing)}")
