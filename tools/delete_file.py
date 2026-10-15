import os
from typing import Any, Dict, Optional

from core.contracts import ToolResult
from core.path_utils import resolve_workspace_path
from tools.base_tool import BaseTool


class DeleteFileTool(BaseTool):
    def __init__(self, workspace_dir: Optional[str] = None):
        self.workspace_dir = workspace_dir or os.getcwd()
        super().__init__(
            name="delete_file",
            description="Delete a file inside the workspace. Requires confirm=true.",
            parameters={
                "file_path": "Relative path to the file.",
                "confirm": "Boolean true is required before deletion.",
            },
        )

    def execute(self, parameters: Dict[str, Any]) -> ToolResult:
        file_path = parameters.get("file_path")
        confirm = parameters.get("confirm")
        if not file_path:
            return ToolResult.failure("Missing required parameter 'file_path'")
        if confirm is not True:
            return ToolResult.failure("Deletion requires confirm=true", file_path=file_path)

        try:
            absolute_path = resolve_workspace_path(self.workspace_dir, file_path)
            if not os.path.isfile(absolute_path):
                return ToolResult.failure("File not found", file_path=file_path)
            os.remove(absolute_path)
            return ToolResult.success(file_path=file_path, deleted=True)
        except PermissionError as e:
            return ToolResult.failure(str(e), file_path=file_path)
        except Exception as e:
            return ToolResult.failure(f"Error deleting file: {e}", file_path=file_path)
