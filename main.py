from tools.terminal import TerminalTool
from core import tool_registry
import sys
import os
from dotenv import load_dotenv
from agent import SimpleAgent
from core.groq_client import GroqClient
from core.tool_registry import ToolRegistry
from core.tool_executor import ToolExecutor
from tools.read_file import ReadFileTool
from tools.write_file import WriteFileTool
from tools.search_files import SearchFilesTool

def main():
    """
    Hàm chính để chạy chương trình. Giao tiếp vòng lặp (Agent Loop) cơ bản với người dùng.
    """
    # 0. Nạp biến môi trường từ file .env
    load_dotenv()
    
    # 1. Khởi tạo Client (Chuyển sang dùng bộ não Groq Cloud)
    llm_client = GroqClient(
        model="llama-3.1-8b-instant" 
    )
    
    # 2. Khởi tạo Registry và đăng ký Tools
    registry = ToolRegistry()
    registry.register(ReadFileTool())
    registry.register(WriteFileTool())
    registry.register(SearchFilesTool())
    registry.register(TerminalTool())

    # 3. Khởi tạo Executor
    executor = ToolExecutor(tool_registry=registry)
    
    # 4. Khởi tạo Agent
    agent = SimpleAgent(
        llm_client=llm_client, 
        tool_registry=registry, 
        tool_executor=executor
    )
    
    print("AI Agent đã sẵn sàng! Gõ 'exit' hoặc 'quit' để thoát.")
    
    while True:
        try:
            user_input = input("\nUser: ").strip()
            
            # Xử lý thoát chương trình
            if user_input.lower() in ['exit', 'quit']:
                print("Tạm biệt!")
                break
                
            # Bỏ qua nếu người dùng không nhập gì
            if not user_input:
                continue
                
            response = agent.run(user_input)
            print(f"\nAgent:\n{response}")
            
        except KeyboardInterrupt:
            # Xử lý khi người dùng bấm Ctrl+C (Interrupt)
            print("\nĐã hủy bởi người dùng. Tạm biệt!")
            sys.exit(0)

if __name__ == "__main__":
    main()