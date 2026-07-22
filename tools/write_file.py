import os
from typing import Dict, Any
from tools.base_tool import BaseTool

class WriteFileTool(BaseTool):
    def __init__(self, workspace_dir: str = None):
        # 1. Cho phép truyền workspace_dir tùy chọn (default = None) để tránh crash ở main.py
        self.workspace_dir = workspace_dir or os.getcwd()
        
        # 2. Gọi super().__init__ của BaseTool để đăng ký đúng đặc tả
        super().__init__(
            name="write_file",  # Sửa lỗi chính tả "write_flie" -> "write_file"
            description="Ghi đè hoặc tạo mới một file với nội dung văn bản cụ thể. Bắt buộc dùng đường dẫn tương đối.",
            parameters={
                "file_path": "Đường dẫn tương đối của file cần ghi (ví dụ: 'hello.py', 'core/utils.py')",
                "content": "Nội dung văn bản đầy đủ cần ghi vào file"
            }
        )

    def execute(self, parameters: Dict[str, Any]) -> str:
        """Ghi nội dung vào file"""
        try:
            file_path = parameters.get("file_path")
            if not file_path:
                return "Lỗi: Thiếu tham số 'file_path'"

            content = parameters.get("content")
            if content is None:  # Cho phép content là chuỗi rỗng
                return "Lỗi: Thiếu tham số 'content'"
            
            # Loại bỏ dấu xuyệt ở đầu nếu có (tránh việc os.path.join bị lỗi)
            file_path = file_path.lstrip("/\\")
                
            # Tạo đường dẫn tuyệt đối
            absolute_path = os.path.abspath(os.path.join(self.workspace_dir, file_path))
            
            # Bảo mật Sandbox: Ngăn chặn LLM dùng '../' để thoát ra khỏi thư mục dự án
            if not absolute_path.startswith(os.path.abspath(self.workspace_dir)):
                return f"Lỗi: Security - Không được phép ghi file ngoài thư mục dự án."
                
            # LOẠI BỎ: os.path.exists(absolute_path) 
            # Vì đây là lệnh GHI file, nếu file chưa tồn tại thì ta phải tạo mới nó chứ không báo lỗi.

            # Tạo thư mục cha nếu chưa tồn tại
            os.makedirs(os.path.dirname(absolute_path), exist_ok=True)

            # Ghi đè nội dung vào file bằng mã hóa utf-8
            with open(absolute_path, "w", encoding="utf-8") as f:
                f.write(content)
                
            # Trả về chuỗi thông báo thay vì số lượng ký tự (f.write trả về int, sai Type Hint -> str)
            return f"Ghi file thành công tại đường dẫn tương đối: {file_path}"
            
        except Exception as e:
            return f"Lỗi khi ghi file: {str(e)}"
            