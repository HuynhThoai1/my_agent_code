import requests


class OllamaClient:
    """Small client for a local Ollama generate endpoint."""

    def __init__(self, base_url: str = "http://localhost:11434", model: str = "deepseek-r1:235b-cloud-q4"):
        self.base_url = base_url
        self.model = model

    def generate(self, prompt: str) -> str:
        url = f"{self.base_url}/api/generate"
        payload = {"prompt": prompt, "model": self.model, "stream": False}

        try:
            response = requests.post(url, json=payload, timeout=300)
            response.raise_for_status()
            result = response.json()
            return result.get("response", "")
        except requests.exceptions.RequestException as e:
            return f"Ollama connection failed: {e}"
