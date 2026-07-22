import os
from typing import Dict, Any
from tools.base_tool import BaseTool

class SearchFilesTool(BaseTool):
    def __init__(self, workspace_dir: str = None):
        self.workspace_dir = workspace_dir or os.getcwd()
        self.ignore_dirs = {'.git', '.venv', '__pycache__', '.vscode'}
        super().__init__(
            name = 'search_files',
            description = 'Tìm kiếm các file trong thư mục dự án dựa trên từ khóa trong tên file. Trả về danh sách đường dẫn tương đối.',
            parameters = {
                "query": "Từ khóa tên file cần tìm (ví dụ: 'helper', 'main')"
            }
        )

    def execute(self, parameters: Dict[str, Any]) -> str:
        try:
            query = parameters.get("query")
            if not query:
                return "Lỗi: Thiếu tham số 'query'"
            
            # Tìm kiếm tên file chứa từ khóa
            matches = []
            for root, dirs, files in os.walk(self.workspace_dir):
                # Sửa đổi list dirs trực tiếp (in-place) để os.walk không đi sâu vào các thư mục rác
                dirs[:] = [d for d in dirs if d not in self.ignore_dirs]
                
                for file in files:
                    # Chuyển về chữ thường để tìm kiếm không phân biệt hoa/thường
                    if query.lower() in file.lower():
                        matches.append(os.path.join(root, file))

            # Chuyển đổi đường dẫn tuyệt đối về tương đối, và chuẩn hóa dấu gạch chéo '/' cho mọi HĐH
            matches = [os.path.relpath(p, self.workspace_dir).replace('\\', '/') for p in matches]
            
            # Trả về danh sách kết quả hoặc thông báo không tìm thấy
            if matches:
                return f"Tìm thấy {len(matches)} file:\n" + "\n".join(matches)
            else:
                return f"Không tìm thấy file nào chứa từ khóa '{query}' trong thư mục '{self.workspace_dir}'"
        except Exception as e:
            return f"Lỗi khi tìm kiếm file: {str(e)}"