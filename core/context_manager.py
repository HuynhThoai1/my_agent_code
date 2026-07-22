class ContextManager:
    def __init__(self, max_observation_chars: int = 1500, max_history_messages: int = 20):
        self.max_observation_chars = max_observation_chars
        self.max_history_messages = max_history_messages
        self.messages = []
    
    def add_user_message(self, text: str):
        self.messages.append(f"User: {text}")

    def add_agent_message(self, text: str):
        self.messages.append(f"Agent: {text}")

    def add_observation(self, text: str):
        text_str = str(text)
        # Rút gọn nếu kết quả Tool trả về quá dài (tránh tràn Token/Rate Limit)
        if len(text_str) > self.max_observation_chars:
            half = self.max_observation_chars // 2
            text_str = text_str[:half] + f"\n\n[... Đã cắt bớt {len(text_str) - self.max_observation_chars} ký tự ở giữa ...]\n\n" + text_str[-half:]
            
        self.messages.append(f"System Observation: {text_str}")

    def get_formatted_context(self) -> str:
        # Nếu chưa vượt quá giới hạn, trả về toàn bộ
        if len(self.messages) <= self.max_history_messages:
            return "\n\n".join(self.messages)
        
        # Cửa sổ trượt (Sliding Window): 
        # Giữ lại câu Prompt gốc của User (index 0) và (N-1) câu gần nhất
        recent_messages = self.messages[-(self.max_history_messages - 1):]
        
        final_list = [
            self.messages[0], 
            "\n... [Đã ẩn các bước trung gian cũ để tiết kiệm bộ nhớ LLM] ...\n"
        ] + recent_messages
        
        return "\n\n".join(final_list)