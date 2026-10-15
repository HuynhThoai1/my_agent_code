import subprocess
from typing import Any, Dict

from core.contracts import ToolResult
from tools.base_tool import BaseTool


class TerminalTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="execute_command",
            description="Execute a shell command and return stdout, stderr, and exit code. Timeout is 10 seconds.",
            parameters={"command": "Shell command to run, for example 'python --version'."},
        )

    def execute(self, parameters: Dict[str, Any]) -> ToolResult:
        command = parameters.get("command")
        if not command:
            return ToolResult.failure("Missing required parameter 'command'")

        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=10,
                encoding="utf-8",
                errors="replace",
            )
            output = {
                "command": command,
                "exit_code": result.returncode,
                "stdout": result.stdout.strip(),
                "stderr": result.stderr.strip(),
            }
            if result.returncode == 0:
                return ToolResult.success(**output)
            return ToolResult.failure("Command failed", **output)
        except subprocess.TimeoutExpired:
            return ToolResult.failure("Command timed out after 10 seconds", command=command)
        except Exception as e:
            return ToolResult.failure(f"Error executing command: {e}", command=command)
