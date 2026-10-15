import argparse
import os
import sys

from dotenv import load_dotenv

from agent import ReActAgent
from core.config import AppConfig, load_config
from core.groq_client import GroqClient
from core.llm_client import OllamaClient
from core.logging_config import configure_logging
from core.tool_executor import ToolExecutor
from core.tool_registry import ToolRegistry
from tools.delete_file import DeleteFileTool
from tools.move_file import MoveFileTool
from tools.read_file import ReadFileTool
from tools.rename_file import RenameFileTool
from tools.search_files import SearchFilesTool
from tools.terminal import TerminalTool
from tools.write_file import WriteFileTool


def build_llm_client(config: AppConfig):
    if config.provider == "groq":
        return GroqClient(model=config.model)
    if config.provider == "ollama":
        return OllamaClient(model=config.model)
    raise ValueError("Unsupported provider. Use 'groq' or 'ollama'.")


def build_registry(workspace_dir: str) -> ToolRegistry:
    registry = ToolRegistry()
    registry.register(ReadFileTool(workspace_dir))
    registry.register(WriteFileTool(workspace_dir))
    registry.register(SearchFilesTool(workspace_dir))
    registry.register(MoveFileTool(workspace_dir))
    registry.register(RenameFileTool(workspace_dir))
    registry.register(DeleteFileTool(workspace_dir))
    registry.register(TerminalTool())
    return registry


def build_agent(config: AppConfig) -> ReActAgent:
    llm_client = build_llm_client(config)
    registry = build_registry(config.workspace_dir)
    executor = ToolExecutor(tool_registry=registry)
    return ReActAgent(
        llm_client=llm_client,
        tool_registry=registry,
        tool_executor=executor,
    )


def run_interactive(agent: ReActAgent) -> None:
    print("AI Agent is ready. Type 'exit' or 'quit' to stop.")
    while True:
        try:
            user_input = input("\nUser: ").strip()
            if user_input.lower() in {"exit", "quit"}:
                print("Goodbye!")
                return
            if not user_input:
                continue
            print(f"\nAgent:\n{agent.run(user_input)}")
        except KeyboardInterrupt:
            print("\nCancelled by user. Goodbye!")
            sys.exit(0)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the AI Agent Platform foundation CLI.")
    parser.add_argument("--task", help="Run one task and exit.")
    parser.add_argument("--provider", choices=["groq", "ollama"], help="Model provider.")
    parser.add_argument("--model", help="Model name.")
    parser.add_argument("--workspace", help="Workspace directory for file tools.")
    return parser.parse_args()


def main() -> int:
    load_dotenv()
    args = parse_args()
    config = load_config(provider=args.provider, model=args.model)
    if args.workspace:
        config.workspace_dir = os.path.abspath(args.workspace)
    configure_logging(config.log_level)

    try:
        agent = build_agent(config)
    except ValueError as e:
        print(f"Configuration error: {e}")
        return 2

    if args.task:
        print(agent.run(args.task))
        return 0

    run_interactive(agent)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
