
import time
import re
import os
import json
import ast
from core.llm_client import OllamaClient
from core.tool_registry import ToolRegistry
from core.tool_executor import ToolExecutor
from core.context_manager import ContextManager

def robust_parse_json(text: str) -> dict:
    """Hàm parse JSON siêu cường, xử lý mọi thể loại ảo giác của LLM."""
    text = text.strip()
    # Loại bỏ code block markdown nếu LLM thêm vào
    if text.startswith('```json'): text = text[7:]
    elif text.startswith('```'): text = text[3:]
    if text.endswith('```'): text = text[:-3]
    text = text.strip()
    
    try:
        return json.loads(text, strict=False)
    except Exception as e1:
        try:
            # Fallback 1: Thử dùng ast.literal_eval cho cú pháp Python Dict
            return ast.literal_eval(text)
        except Exception as e2:
            # Fallback 2: Trích xuất phần nằm giữa { }
            start = text.find('{')
            end = text.rfind('}')
            if start != -1 and end != -1:
                try:
                    return json.loads(text[start:end+1], strict=False)
                except Exception:
                    pass
            raise ValueError(f"JSONDecodeError: {e1} | ASTError: {e2}")

class SimpleAgent:
    """
    Agent thông minh có khả năng gọi tool.
    """
    def __init__(self, llm_client: OllamaClient, tool_registry: ToolRegistry, tool_executor: ToolExecutor):
        self.llm_client = llm_client
        self.registry = tool_registry
        self.executor = tool_executor
        self.max_iterations = 10

    def run(self, user_input: str) -> str:
        # Lấy danh sách tools
        tools_info = self.registry.get_tool_descriptions()
        current_dir = os.getcwd()
    
        context_manager = ContextManager() 
        context_manager.add_user_message(user_input)
        context_manager.add_observation(f"[System Dir]: {current_dir}")

        for step in range(self.max_iterations):
            print(f"\n--- [Bước {step + 1}] Agent đang suy nghĩ ---")

            # Gộp toàn bộ lịch sử thành một chuỗi dài
            context_str = context_manager.get_formatted_context()

            # Tạo Prompt hướng dẫn cho LLM
            system_prompt = f"""Bạn là một trợ lý AI thông minh. 
            Công cụ hiện có để bạn sử dụng:
            {tools_info}
            
            HƯỚNG DẪN QUAN TRỌNG & CHỐNG ẢO GIÁC:
            - Bạn KHÔNG THỂ tự chạy code, tự đoán kết quả, hay tự tạo file bằng trí tưởng tượng. Bạn BẮT BUỘC PHẢI GỌI TOOL để tương tác với hệ thống thực tế.
            - Nếu bạn CẦN dùng công cụ, bạn phải tuân thủ CHÍNH XÁC định dạng sau (Gồm 2 dòng: Suy nghĩ và Gọi Tool):
            SUY NGHĨ: (Viết ra 1 câu giải thích bạn định làm gì tiếp theo)
            <TOOL>tên_công_cụ|{{"tham_số": "giá trị"}}</TOOL>

            VÍ DỤ CHUẨN KHI GỌI TOOL ĐỌC FILE:
            SUY NGHĨ: Tôi cần đọc file idea.md để xem nội dung
            <TOOL>read_file|{{"file_path": "idea.md"}}</TOOL>

            VÍ DỤ CHUẨN KHI GỌI TOOL GHI FILE:
            SUY NGHĨ: Tôi sẽ tạo file hello.py như yêu cầu
            <TOOL>write_file|{{"file_path": "hello.py", "content": "print('hello')"}}</TOOL>

            QỦY TẮC DỪNG VÒNG LẶP (CỰC KỲ QUAN TRỌNG):
            - Kiểm tra phần LỊCH SỬ TƯƠNG TÁC bên dưới. 
            - Nếu kết quả từ `System Observation` chứng minh rằng MỌI YÊU CẦU CỦA USER ĐÃ ĐƯỢC HOÀN THÀNH, bạn KHÔNG ĐƯỢC PHÉP gọi thêm thẻ <TOOL> nào nữa.
            - ĐỂ KẾT THÚC: Hãy viết một đoạn văn bình thường tóm tắt lại những gì bạn đã làm thành công cho User. TUYỆT ĐỐI KHÔNG xuất thẻ <TOOL>.

            DƯỚI ĐÂY LÀ LỊCH SỬ TƯƠNG TÁC TỪ TRƯỚC ĐẾN NAY:
            {context_str}

            Dựa vào lịch sử trên, hãy đưa ra quyết định của bạn (Gọi <TOOL> hoặc Trả lời trực tiếp):
            """
            
            # Tạm dừng 3 giây giữa các bước để không bị vượt Rate Limit (429) của Groq API
            time.sleep(3.0)

            # Gọi LLM
            response = self.llm_client.generate(system_prompt)
            
            # Phân tích kết quả (Regex tìm <TOOL>...</TOOL>)
            match = re.search(r"<TOOL>(.*?)\|(.*?)(?:</TOOL>|$)", response, re.DOTALL)
            
            if match:
                tool_name = match.group(1).strip()
                params_str = match.group(2).strip()
                
                print(f"[Agent] Quyết định gọi tool: {tool_name} với tham số {params_str}")
                
                # [QUAN TRỌNG]: Mẹo chống lú (Anti-Loop Trick)
                # LLM rất dễ bị ám ảnh bởi các thẻ <TOOL> trong quá khứ. 
                # Ta sẽ xóa thẻ <TOOL> khỏi lịch sử và báo cho nó biết hành động này ĐÃ ĐƯỢC THỰC HIỆN.
                clean_thought = response[:match.start()].strip()
                context_manager.add_agent_message(f"Suy nghĩ: {clean_thought}\n[Hành động đã thực thi: {tool_name}]")
                
                try:
                    # Ép kiểu chuỗi thành dict bằng hàm siêu cường
                    parameters = robust_parse_json(params_str)
                    # Thực thi tool
                    observation = self.executor.execute(tool_name, parameters)

                    # Đưa kết quả của Tool vào lịch sử
                    context_manager.add_observation(observation)

                    continue

                except Exception as e:
                    # Nếu LLM truyền tham số láo, báo lỗi lại cho nó tự sửa
                    error_message = f"Lỗi parse JSON: {e}"
                    context_manager.add_observation(error_message)

                    continue
            
            else:
                # Vòng lặp kết thúc thành công!
                return response

        return f"Thất bại: Đạt giới hạn {self.max_iterations} bước lặp."