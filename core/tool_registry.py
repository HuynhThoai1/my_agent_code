from typing import Dict, Optional
from tools.base_tool import BaseTool

class ToolRegistry:
    """
    Nơi đăng ký và chứa danh sách các công cụ.
    """
    def __init__(self):
        self.tools: Dict[str, BaseTool] = {}

    def register(self, tool: BaseTool):
        self.tools[tool.name] = tool

    def get_tool_descriptions(self) -> str:
        """
        Tạo danh sách mô tả các tool để đưa vào prompt cho LLM.
        """
        if not self.tools:
            return "Không có tool nào."
            
        descriptions = []
        for name, tool in self.tools.items():
            descriptions.append(f"- Tên: {name}\n  Mô tả: {tool.description}\n  Tham số: {tool.parameters}")
        return "\n".join(descriptions)

    def get_tool(self, name: str) -> Optional[BaseTool]:
        return self.tools.get(name)