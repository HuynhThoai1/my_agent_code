from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseTool(ABC):
    """
    Khuôn mẫu (Class cha) cho mọi tool.
    Các tool cụ thể bắt buộc phải kế thừa class này và ghi đè hàm execute.
    """
    def __init__(self, name: str, description: str, parameters: dict):
        self.name = name
        self.description = description
        self.parameters = parameters

    @abstractmethod
    def execute(self, parameters: Dict[str, Any]) -> str:
        """
        Thực thi chức năng của tool.
        """
        pass
