from abc import ABC, abstractmethod
from typing import Any, Dict

from core.contracts import ToolResult


class BaseTool(ABC):
    """Base class for every tool exposed to an agent."""

    def __init__(self, name: str, description: str, parameters: dict):
        self.name = name
        self.description = description
        self.parameters = parameters

    @abstractmethod
    def execute(self, parameters: Dict[str, Any]) -> ToolResult:
        """Run the tool and return a structured result."""
        pass
