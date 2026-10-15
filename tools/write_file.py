import os
from typing import Any, Dict, Optional

from core.contracts import ToolResult
from core.path_utils import resolve_workspace_path
from tools.base_tool import BaseTool


class WriteFileTool(BaseTool):
    def __init__(self, workspace_dir: Optional[str] = None):
        self.workspace_dir = workspace_dir or os.getcwd()
        super().__init__(
            name="write_file",
            description="Create or overwrite a text file inside the configured workspace.",
            parameters={
                "file_path": "Relative path to the file.",
                "content": "Full text content to write.",
            },
        )

    def execute(self, parameters: Dict[str, Any]) -> ToolResult:
        file_path = parameters.get("file_path")
        if not file_path:
            return ToolResult.failure("Missing required parameter 'file_path'")

        content = parameters.get("content")
        if content is None:
            return ToolResult.failure("Missing required parameter 'content'", file_path=file_path)

        try:
            absolute_path = resolve_workspace_path(self.workspace_dir, file_path)
            os.makedirs(os.path.dirname(absolute_path), exist_ok=True)
            text = str(content)
            with open(absolute_path, "w", encoding="utf-8") as f:
                f.write(text)

            return ToolResult.success(
                file_path=file_path,
                bytes_written=len(text.encode("utf-8")),
            )
        except PermissionError as e:
            return ToolResult.failure(str(e), file_path=file_path)
        except Exception as e:
            return ToolResult.failure(f"Error writing file: {e}", file_path=file_path)
