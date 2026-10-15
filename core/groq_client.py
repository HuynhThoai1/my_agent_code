import os

import requests


class GroqClient:
    """Small client for Groq's OpenAI-compatible chat completions API."""

    def __init__(self, model: str = "llama-3.1-8b-instant"):
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = model
        self.api_key = os.environ.get("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY is missing. Add it to .env or choose --provider ollama.")

    def generate(self, prompt: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.0,
        }

        try:
            response = requests.post(self.base_url, headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except requests.exceptions.RequestException as e:
            return f"Groq connection failed: {e}"
