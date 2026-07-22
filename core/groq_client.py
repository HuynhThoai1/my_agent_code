import os
import requests

class GroqClient:
    """
    Client giao tiếp trực tiếp với Groq API.
    Sử dụng model Llama 3 qua hạ tầng siêu tốc của Groq.
    """
    def __init__(self, model: str = "llama-3.1-8b-instant"):
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = model
        
        # Lấy API key từ biến môi trường
        self.api_key = os.environ.get("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("Không tìm thấy GROQ_API_KEY trong môi trường. Hãy kiểm tra file .env")

    def generate(self, prompt: str) -> str:
        """
        Gửi prompt đến model thông qua Groq API và trả về kết quả dạng text.
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Groq API sử dụng chuẩn Chat Completions (giống cấu trúc của OpenAI)
        payload = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.0  # Set về 0 để mô hình trả lời deterministic (ít ảo giác)
        }
        
        try:
            response = requests.post(self.base_url, headers=headers, json=payload, timeout=60)
            response.raise_for_status() # Báo lỗi nếu HTTP status code không phải 200
            
            result = response.json()
            # Lấy text từ JSON response chuẩn OpenAI/Groq
            return result["choices"][0]["message"]["content"]
            
        except requests.exceptions.RequestException as e:
            print(f"[Lỗi Hệ Thống] Kết nối Groq API thất bại: {e}")
            return "Xin lỗi, tôi đang gặp sự cố kết nối với bộ não Cloud (Groq)."
