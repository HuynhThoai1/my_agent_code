import logging
import os
import re
import time

from core.parsing import robust_parse_json
from core.context_manager import ContextManager
from core.tool_executor import ToolExecutor
from core.tool_registry import ToolRegistry

logger = logging.getLogger(__name__)


class ReActAgent:
    """Minimal ReAct agent loop for the first platform milestone."""

    def __init__(self, llm_client, tool_registry: ToolRegistry, tool_executor: ToolExecutor):
        self.llm_client = llm_client
        self.registry = tool_registry
        self.executor = tool_executor
        self.max_iterations = 10

    def run(self, user_input: str) -> str:
        tools_info = self.registry.get_tool_descriptions()
        current_dir = os.getcwd()

        context_manager = ContextManager()
        context_manager.add_user_message(user_input)
        context_manager.add_observation(f"[System Dir]: {current_dir}")

        for step in range(self.max_iterations):
            logger.info("Agent iteration %s/%s", step + 1, self.max_iterations)
            context_str = context_manager.get_formatted_context()

            system_prompt = f"""You are a careful AI assistant that can use tools.
Available tools:
{tools_info}

Rules:
- You cannot inspect files, run code, or change the system by imagination. Use tools for real system interaction.
- If you need a tool, respond in exactly this format:
THOUGHT: one short sentence about the next action
<TOOL>tool_name|{{"parameter": "value"}}</TOOL>
- If the latest System Observation proves the user's request is complete, stop calling tools and answer normally.
- Never include a <TOOL> block in the final answer.

Conversation history:
{context_str}

Decide the next action:
"""
            time.sleep(1.0)
            response = self.llm_client.generate(system_prompt)
            match = re.search(r"<TOOL>(.*?)\|(.*?)(?:</TOOL>|$)", response, re.DOTALL)

            if not match:
                return response

            tool_name = match.group(1).strip()
            params_str = match.group(2).strip()
            clean_thought = response[: match.start()].strip()
            context_manager.add_agent_message(
                f"Thought: {clean_thought}\n[Executed action: {tool_name}]"
            )

            try:
                parameters = robust_parse_json(params_str)
                observation = self.executor.execute(tool_name, parameters)
                context_manager.add_observation(observation.to_dict())
            except Exception as e:
                context_manager.add_observation(f"Tool call error: {e}")

        return f"Failed: reached the {self.max_iterations} iteration limit."


SimpleAgent = ReActAgent
