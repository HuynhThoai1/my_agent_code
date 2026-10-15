# AI Agent Platform Foundation

This is the first runnable foundation for the multi-agent platform described in `../agent_platform`.

## What exists now

- A minimal ReAct agent loop.
- A tool registry and tool executor.
- Structured `ToolResult` and `AgentMessage` contracts.
- File tools for read, write, search, move, rename, and delete with workspace sandbox checks.
- A terminal tool for short shell commands.
- Groq and Ollama model clients.
- CLI support for interactive mode and one-shot tasks.

## Setup

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -e ".[dev]"
copy .env.example .env
```

Set `GROQ_API_KEY` in `.env` when using the default Groq provider.

## Run

Interactive mode:

```bash
python main.py
```

One-shot task:

```bash
python main.py --task "Search for README files"
```

Use Ollama instead:

```bash
python main.py --provider ollama --model deepseek-r1:235b-cloud-q4
```

## Test

```bash
pytest
```
