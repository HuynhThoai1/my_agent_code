import os
from typing import Any, Dict, Optional

from core.contracts import ToolResult
from core.path_utils import resolve_workspace_path
from tools.base_tool import BaseTool


class RenameFileTool(BaseTool):
    def __init__(self, workspace_dir: Optional[str] = None):
        self.workspace_dir = workspace_dir or os.getcwd()
        super().__init__(
            name="rename_file",
            description="Rename a file in place inside the configured workspace.",
            parameters={
                "file_path": "Relative path to the existing file.",
                "new_name": "New filename only, not a directory path.",
            },
        )

    def execute(self, parameters: Dict[str, Any]) -> ToolResult:
        file_path = parameters.get("file_path")
        new_name = parameters.get("new_name")
        if not file_path or not new_name:
            return ToolResult.failure("Missing required parameters 'file_path' and/or 'new_name'")
        if os.path.basename(new_name) != new_name:
            return ToolResult.failure("'new_name' must be a filename, not a path", new_name=new_name)

        try:
            source = resolve_workspace_path(self.workspace_dir, file_path)
            destination = os.path.join(os.path.dirname(source), new_name)
            destination = resolve_workspace_path(self.workspace_dir, os.path.relpath(destination, self.workspace_dir))
            if not os.path.isfile(source):
                return ToolResult.failure("File not found", file_path=file_path)
            os.rename(source, destination)
            return ToolResult.success(file_path=file_path, new_path=os.path.relpath(destination, self.workspace_dir).replace("\\", "/"))
        except PermissionError as e:
            return ToolResult.failure(str(e), file_path=file_path, new_name=new_name)
        except Exception as e:
            return ToolResult.failure(f"Error renaming file: {e}", file_path=file_path, new_name=new_name)
