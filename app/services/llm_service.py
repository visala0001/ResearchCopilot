from google import genai
from google.genai import types

from app.config.settings import GEMINI_API_KEY


class GeminiService:

    def __init__(self):
        self.client = genai.Client(
            api_key=GEMINI_API_KEY
        )

        self.model = "gemini-3.5-flash-lite"

    def generate_structured(self, prompt: str, response_schema):

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=response_schema,
            ),
        )

        return response.parsed