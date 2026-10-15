import os
from typing import Any, Dict, Optional

from core.contracts import ToolResult
from core.path_utils import resolve_workspace_path
from tools.base_tool import BaseTool


class ReadFileTool(BaseTool):
    def __init__(self, workspace_dir: Optional[str] = None):
        self.workspace_dir = workspace_dir or os.getcwd()
        super().__init__(
            name="read_file",
            description="Read a text file inside the configured workspace.",
            parameters={"file_path": "Relative path to the file, for example 'README.md'."},
        )

    def execute(self, parameters: Dict[str, Any]) -> ToolResult:
        file_path = parameters.get("file_path")
        if not file_path:
            return ToolResult.failure("Missing required parameter 'file_path'")

        try:
            absolute_path = resolve_workspace_path(self.workspace_dir, file_path)
            if not os.path.exists(absolute_path):
                return ToolResult.failure("File not found", file_path=file_path)
            if not os.path.isfile(absolute_path):
                return ToolResult.failure("Path is not a file", file_path=file_path)

            with open(absolute_path, "r", encoding="utf-8") as f:
                content = f.read()
            return ToolResult.success(file_path=file_path, content=content)
        except PermissionError as e:
            return ToolResult.failure(str(e), file_path=file_path)
        except Exception as e:
            return ToolResult.failure(f"Error reading file: {e}", file_path=file_path)
