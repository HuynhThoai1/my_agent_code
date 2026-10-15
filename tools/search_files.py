import os
from typing import Any, Dict, Optional

from core.contracts import ToolResult
from tools.base_tool import BaseTool


class SearchFilesTool(BaseTool):
    def __init__(self, workspace_dir: Optional[str] = None):
        self.workspace_dir = workspace_dir or os.getcwd()
        self.ignore_dirs = {".git", ".venv", "__pycache__", ".vscode"}
        super().__init__(
            name="search_files",
            description="Search files by filename keyword inside the configured workspace.",
            parameters={"query": "Filename keyword to search for, for example 'main'."},
        )

    def execute(self, parameters: Dict[str, Any]) -> ToolResult:
        query = parameters.get("query")
        if not query:
            return ToolResult.failure("Missing required parameter 'query'")

        matches = []
        try:
            for root, dirs, files in os.walk(self.workspace_dir):
                dirs[:] = [d for d in dirs if d not in self.ignore_dirs]
                for file_name in files:
                    if str(query).lower() in file_name.lower():
                        absolute_path = os.path.join(root, file_name)
                        relative_path = os.path.relpath(absolute_path, self.workspace_dir)
                        matches.append(relative_path.replace("\\", "/"))

            return ToolResult.success(query=query, matches=matches, count=len(matches))
        except Exception as e:
            return ToolResult.failure(f"Error searching files: {e}", query=query)
