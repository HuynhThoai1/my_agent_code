import os
import shutil
from typing import Any, Dict, Optional

from core.contracts import ToolResult
from core.path_utils import resolve_workspace_path
from tools.base_tool import BaseTool


class MoveFileTool(BaseTool):
    def __init__(self, workspace_dir: Optional[str] = None):
        self.workspace_dir = workspace_dir or os.getcwd()
        super().__init__(
            name="move_file",
            description="Move a file to another relative path inside the configured workspace.",
            parameters={
                "source_path": "Relative path to the existing file.",
                "destination_path": "Relative path to the destination file.",
            },
        )

    def execute(self, parameters: Dict[str, Any]) -> ToolResult:
        source_path = parameters.get("source_path")
        destination_path = parameters.get("destination_path")
        if not source_path or not destination_path:
            return ToolResult.failure("Missing required parameters 'source_path' and/or 'destination_path'")

        try:
            source = resolve_workspace_path(self.workspace_dir, source_path)
            destination = resolve_workspace_path(self.workspace_dir, destination_path)
            if not os.path.isfile(source):
                return ToolResult.failure("Source file not found", source_path=source_path)
            os.makedirs(os.path.dirname(destination), exist_ok=True)
            shutil.move(source, destination)
            return ToolResult.success(source_path=source_path, destination_path=destination_path)
        except PermissionError as e:
            return ToolResult.failure(str(e), source_path=source_path, destination_path=destination_path)
        except Exception as e:
            return ToolResult.failure(f"Error moving file: {e}", source_path=source_path, destination_path=destination_path)
