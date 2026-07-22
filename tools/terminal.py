import subprocess
from typing import Dict, Any
from tools.base_tool import BaseTool

class TerminalTool(BaseTool):
    def __init__(self):
        super().__init__(
            name = "execute_command",
            description = "Thực thi một câu lệnh trên Terminal (Shell) của hệ thống. Trả về kết quả stdout hoặc stderr. Giới hạn thời gian chạy tối đa là 10 giây.",
            parameters = {
                "command" : "Câu lệnh shell cần chạy (ví dụ: 'python test.py', 'pip list')"
            }
        )

    def execute(self, parameters: Dict[str, Any]) -> str:
        try:
            command = parameters.get("command")
            if not command:
                return "Lỗi: Thiếu tham số 'command'"
            
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=10,
                encoding='utf-8',
                errors='replace' # Tránh lỗi crash khi Console in ra ký tự lạ (như tiếng Việt bị lỗi font) trên Windows
            )

            # Khôn khéo gộp cả stdout và stderr
            output = ""
            if result.stdout:
                output += result.stdout
            if result.stderr:
                output += f"\n[Lỗi/Cảnh báo từ hệ thống]:\n{result.stderr}"
                
            # Đánh giá thành công hay thất bại dựa vào mã Exit Code
            if result.returncode == 0:
                return output.strip() if output.strip() else "Lệnh thực thi thành công nhưng không có kết quả in ra màn hình."
            else:
                return f"Lệnh thất bại (Exit Code: {result.returncode}):\n{output.strip()}"
        except subprocess.TimeoutExpired:
            return "Lỗi: Lệnh chạy quá 10 giây."
        except Exception as e:
            return f"Lỗi: {str(e)}"
        