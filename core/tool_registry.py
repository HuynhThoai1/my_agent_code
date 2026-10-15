from typing import Dict, Optional

from tools.base_tool import BaseTool


class ToolRegistry:
    """Registry for tools available to an agent."""

    def __init__(self):
        self.tools: Dict[str, BaseTool] = {}

    def register(self, tool: BaseTool) -> None:
        self.tools[tool.name] = tool

    def get_tool_descriptions(self) -> str:
        if not self.tools:
            return "No tools registered."

        descriptions = []
        for name, tool in self.tools.items():
            descriptions.append(
                f"- Name: {name}\n"
                f"  Description: {tool.description}\n"
                f"  Parameters: {tool.parameters}"
            )
        return "\n".join(descriptions)

    def get_tool(self, name: str) -> Optional[BaseTool]:
        return self.tools.get(name)
