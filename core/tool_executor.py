from typing import Any, Dict

from core.contracts import ToolResult
from core.tool_registry import ToolRegistry


class ToolExecutor:
    """Validate and execute registered tools."""

    def __init__(self, tool_registry: ToolRegistry):
        self.registry = tool_registry

    def execute(self, tool_name: str, parameters: Dict[str, Any]) -> ToolResult:
        if not isinstance(parameters, dict):
            return ToolResult.failure("Tool parameters must be a dictionary", tool_name=tool_name)

        tool = self.registry.get_tool(tool_name)
        if not tool:
            return ToolResult.failure(f"Tool '{tool_name}' was not found", tool_name=tool_name)

        try:
            result = tool.execute(parameters)
            if isinstance(result, ToolResult):
                return result
            return ToolResult.success(text=str(result))
        except Exception as e:
            return ToolResult.failure(
                f"System error while running tool '{tool_name}': {e}",
                tool_name=tool_name,
            )
