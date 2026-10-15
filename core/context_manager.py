class ContextManager:
    def __init__(self, max_observation_chars: int = 1500, max_history_messages: int = 20):
        self.max_observation_chars = max_observation_chars
        self.max_history_messages = max_history_messages
        self.messages = []

    def add_user_message(self, text: str) -> None:
        self.messages.append(f"User: {text}")

    def add_agent_message(self, text: str) -> None:
        self.messages.append(f"Agent: {text}")

    def add_observation(self, text) -> None:
        text_str = str(text)
        if len(text_str) > self.max_observation_chars:
            half = self.max_observation_chars // 2
            removed = len(text_str) - self.max_observation_chars
            text_str = (
                text_str[:half]
                + f"\n\n[... truncated {removed} characters from the middle ...]\n\n"
                + text_str[-half:]
            )

        self.messages.append(f"System Observation: {text_str}")

    def get_formatted_context(self) -> str:
        if len(self.messages) <= self.max_history_messages:
            return "\n\n".join(self.messages)

        recent_messages = self.messages[-(self.max_history_messages - 1) :]
        final_list = [
            self.messages[0],
            "\n... [older intermediate steps hidden to save context] ...\n",
        ] + recent_messages

        return "\n\n".join(final_list)
