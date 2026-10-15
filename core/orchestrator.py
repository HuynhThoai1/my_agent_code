from uuid import uuid4
from typing import Optional

from core.contracts import AgentMessage


class Orchestrator:
    """Thin v1 orchestrator that wraps a single agent behind the platform contract."""

    def __init__(self, agent, name: str = "react_agent"):
        self.agent = agent
        self.name = name

    def run(self, user_input: str, task_id: Optional[str] = None) -> AgentMessage:
        resolved_task_id = task_id or str(uuid4())
        try:
            response = self.agent.run(user_input)
            return AgentMessage(
                task_id=resolved_task_id,
                agent=self.name,
                input={"prompt": user_input},
                output={"response": response},
                status="success",
            )
        except Exception as e:
            return AgentMessage(
                task_id=resolved_task_id,
                agent=self.name,
                input={"prompt": user_input},
                output={},
                status="error",
                error=str(e),
            )
