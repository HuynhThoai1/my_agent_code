import requests
from typing import Optional

class OllamaClient:
    """
    Client giao tiếp trực tiếp với Ollama API.
    Tách biệt logic gọi API khỏi Agent.
    """
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "deepseek-r1:235b-cloud-q4"):
        # Tránh hardcode: Cho phép truyền cấu hình từ bên ngoài (có default value)
        self.base_url = base_url
        self.model = model

    def generate(self, prompt: str) -> str:
        """
        Gửi prompt đến model thông qua Ollama API và trả về kết quả dạng text.
        """
        url = f"{self.base_url}/api/generate"
        payload = {
            "prompt": prompt,
            "model": self.model,
            "stream": False  # Đợi response đầy đủ trước khi trả về
        }
        
        try:
            response = requests.post(url, json=payload, timeout=300)
            response.raise_for_status()
            
            result = response.json()
            return result.get("response", "")
            
        except requests.exceptions.RequestException as e:
            # Xử lý lỗi tinh tế hơn thay vì trả về text lỗi làm Agent hiểu nhầm là câu trả lời của LLM.
            print(f"[Lỗi Hệ Thống] Kết nối Ollama API thất bại: {e}")
            return "Xin lỗi, tôi đang gặp sự cố kết nối với bộ não (Ollama)."