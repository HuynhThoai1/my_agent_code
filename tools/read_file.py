import os
from typing import Dict, Any
from tools.base_tool import BaseTool

class ReadFileTool(BaseTool):
    def __init__(self, workspace_dir: str = None):
        # Lấy thư mục hiện tại làm workspace gốc nếu không truyền vào
        self.workspace_dir = workspace_dir or os.getcwd()
        
        super().__init__(
            name="read_file",
            description="Đọc nội dung của một file. Bắt buộc dùng đường dẫn tương đối tính từ thư mục dự án.",
            parameters={"file_path": "Đường dẫn tương đối tới file (VD: 'idea.md', 'core/agent.py')"}
        )

    def execute(self, parameters: Dict[str, Any]) -> str:
        try:
            file_path = parameters.get("file_path")
            if not file_path:
                return "Lỗi: Thiếu tham số 'file_path'"
            
            # Loại bỏ dấu xuyệt ở đầu nếu có (tránh việc os.path.join bị lỗi)
            file_path = file_path.lstrip("/\\")
                
            # Tạo đường dẫn tuyệt đối
            absolute_path = os.path.abspath(os.path.join(self.workspace_dir, file_path))
            
            # Bảo mật Sandbox: Ngăn chặn LLM dùng '../' để thoát ra khỏi thư mục dự án
            if not absolute_path.startswith(os.path.abspath(self.workspace_dir)):
                return f"Lỗi: Security - Không được phép đọc file ngoài thư mục dự án."
                
            if not os.path.exists(absolute_path):
                return f"Lỗi: Không tìm thấy file tại '{absolute_path}'"
                
            with open(absolute_path, "r", encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"Lỗi khi đọc file: {str(e)}"