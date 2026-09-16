from google import genai
import src.config as config

class GeminiService:
    def __init__(self):
        self.client = genai.Client(api_key=config.GEMINI_API_KEY)
        self.model_name = "gemini-3.6-flash"
        self.fast_model = "gemini-3.6-flash"

    def analyze_rules(self, current_rules, new_files_context=""):
        """Agent 1: Analizuje zasady i proponuje aktualizacje jeśli potrzebne."""
        prompt = f"""
Jesteś Agentem 1 (Głównym Architektem) księgozbioru.
Zasada nadrzędna to 'Metadata First'. Zadbaj by zachować wytyczne IFLA ICP.

Oto obecny plik Zasad:
{current_rules}

Zdarzenia w bibliotece:
{new_files_context}

Twoje zadanie: 
Zwróć zaktualizowaną treść pliku Markdown. Nie dodawaj wstępu, ani formatowania blokowego markdown (```markdown) wokół całości. Jeśli plik nie wymaga zmian, po prostu go zwróć.
"""
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
        )
        text = response.text.strip()
        if text.startswith("```markdown"):
            text = text[11:]
        if text.endswith("```"):
            text = text[:-3]
        return text.strip()

    def clean_filename(self, filename):
        """Agent 2 pomocniczo: czyści nazwy z błędów."""
        prompt = f"""
Przeformatuj nazwę: '{filename}'.
Wymogi: schemat 'Tytul_Autor.rozszerzenie', brak spacji (zamień na _), całkowity brak polskich znaków diakrytycznych.
Zwróć TYLKO wygenerowaną nową nazwę.
"""
        response = self.client.models.generate_content(
            model=self.fast_model,
            contents=prompt,
        )
        return response.text.strip()
