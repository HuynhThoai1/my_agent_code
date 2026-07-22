from typing import Dict, Any
from core.tool_registry import ToolRegistry

class ToolExecutor:
    """
    Người thợ thực thi công cụ.
    """
    def __init__(self, tool_registry: ToolRegistry):
        self.registry = tool_registry

    def execute(self, tool_name: str, parameters: Dict[str, Any]) -> str:
        tool = self.registry.get_tool(tool_name)
        if not tool:
            return f"Lỗi: Không tìm thấy tool có tên '{tool_name}'"
            
        try:
            return tool.execute(parameters)
        except Exception as e:
            return f"Lỗi hệ thống khi chạy tool {tool_name}: {str(e)}"