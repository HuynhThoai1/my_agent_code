# Autonomous AI Agent from Scratch

An autonomous AI Agent built entirely from scratch in Python, without relying on heavy frameworks like LangChain, AutoGen, or LlamaIndex. This project aims to demystify the core concepts behind modern Agentic AI systems by implementing them step-by-step.

## 🚀 Features

Built through 7 distinct milestones, this Agent is fully capable of Reasoning and Acting (ReAct):

1. **Tool Calling Engine**: The LLM can interact with the host system using robustly parsed JSON parameters.
2. **Read & Write Files**: Ability to inspect codebase and write/modify scripts dynamically.
3. **Smart File Search**: Recursively scan project directories to locate target files.
4. **Terminal Execution**: Directly run shell commands (with timeouts and safety encoding) to test code, install dependencies, or read logs.
5. **ReAct Agent Loop**: The core engine that enables the Agent to perform multi-step tasks autonomously. It thinks, executes a tool, reads the observation, and decides the next step until the goal is completed.
6. **Self-Correction (Anti-Hallucination)**: Strict system prompts force the LLM to think before acting and prevents infinite tool-calling loops or fake actions.
7. **Context Management**: A built-in sliding window and token truncation mechanism that ensures the LLM's context window never overflows, saving API costs and preventing `429 Too Many Requests` rate limits.

## 🧠 Architecture Highlights

- **`core/llm_client.py`**: Wrapper for communicating with Groq / Ollama.
- **`core/tool_registry.py`**: A registry system to dynamically load and manage available tools.
- **`core/tool_executor.py`**: Safely parses `<TOOL>` blocks and dispatches execution.
- **`core/context_manager.py`**: Handles Sliding Window memory and observation truncation for LLMs.
- **`agent.py`**: The main ReAct loop orchestrating Thoughts, Actions, and Observations.

*(For detailed architectural sequence diagrams, please check `flow_design.md`)*

## 🛠️ Getting Started

### Prerequisites
- Python 3.9+
- A `.env` file containing your API Key (e.g., `GROQ_API_KEY`)

### Installation & Run
1. Clone this repository.
2. Create a virtual environment and install requirements (if any).
3. Run the Agent:
   ```bash
   python main.py
   ```
4. Ask a complex, multi-step question!
   *Example: "Find the math helper script, run it in the terminal, read the output, and write the final result into a new text file."*