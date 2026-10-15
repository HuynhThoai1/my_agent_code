from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class AgentMessage:
    task_id: str
    agent: str
    input: Dict[str, Any]
    output: Dict[str, Any]
    status: str
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "agent": self.agent,
            "input": self.input,
            "output": self.output,
            "status": self.status,
            "error": self.error,
        }


@dataclass
class ToolResult:
    status: str
    output: Dict[str, Any]
    error: Optional[str] = None

    @classmethod
    def success(cls, **output: Any) -> "ToolResult":
        return cls(status="success", output=output, error=None)

    @classmethod
    def failure(cls, error: str, **output: Any) -> "ToolResult":
        return cls(status="error", output=output, error=error)

    def to_dict(self) -> Dict[str, Any]:
        return {"status": self.status, "output": self.output, "error": self.error}

    def to_text(self) -> str:
        if self.status == "success":
            return f"ToolResult(success): {self.output}"
        return f"ToolResult(error): {self.error}; output={self.output}"
