# Workflow Design

This document stores the workflow diagrams of all Milestones in the process of building the AI Agent.

---

## MILESTONE 1: Minimal AI Chat Agent (Linear Flow)

A one-way linear flow from the User to the LLM, returning results directly to the User (like a basic Chatbot).

```mermaid
sequenceDiagram
    actor User as User
    participant Agent as SimpleAgent
    participant LLM as Groq Cloud API

    User->>Agent: 1. Input Prompt (e.g., "Hello")
    Agent->>LLM: 2. Send Prompt
    LLM-->>Agent: 3. Return Raw text response
    Agent->>User: 4. Print result to screen
```

---

## MILESTONE 2: Tool Calling - Read File (Agentic Loop)

Looping workflow: The Agent intercepts the LLM's response to execute a file reading tool on the hard drive, then feeds the result back to the LLM to synthesize the final answer.

```mermaid
sequenceDiagram
    actor User as User
    participant Agent as SimpleAgent
    participant LLM as Groq Cloud API
    participant Exec as ToolExecutor (ReadFileTool)
    participant Disk as Local File System

    User->>Agent: 1. Ask a question requiring file reading
    Agent->>LLM: 2. Send Prompt with Tools list
    LLM-->>Agent: 3. Return command <TOOL>read_file...
    
    Note over Agent: 4. Use Regex to extract Tool name & Parameters
    
    Agent->>Exec: 5. Forward read file command
    Exec->>Disk: 6. Find and read physical file
    Disk-->>Exec: Data (Text)
    Exec-->>Agent: 7. Return file content (Observation)
    
    Agent->>LLM: 8. Send file content back to LLM
    LLM-->>Agent: 9. Synthesize final answer
    Agent->>User: 10. Reply directly to User
```

---

## MILESTONE 3: Tool WriteFile - Write File (Creative Flow)

A workflow allowing the Agent to create new or overwrite file contents, automatically building the parent directory structure if it does not exist on the hard drive.

```mermaid
sequenceDiagram
    actor User as User
    participant Agent as SimpleAgent
    participant LLM as Groq Cloud API
    participant Exec as ToolExecutor (WriteFileTool)
    participant Disk as Local File System

    User->>Agent: 1. Request: "Create hello.py printing hello world"
    Agent->>LLM: 2. Send Prompt with Tools list (Read & Write)
    LLM-->>Agent: 3. Return command <TOOL>write_file|{"file_path": "hello.py", "content": "print('hello world')"}</TOOL>
    
    Note over Agent: 4. Use Regex to extract Tool name & Parameters
    
    Agent->>Exec: 5. Forward write file command with Content
    Exec->>Disk: 6. Create parent dir (if needed) & Overwrite/Create new file
    Disk-->>Exec: File saved successfully
    Exec-->>Agent: 7. Return write result (Observation)
    
    Agent->>LLM: 8. Send "Write successful" result back to LLM
    LLM-->>Agent: 9. Synthesize final confirmation answer
    Agent->>User: 10. Reply directly to User
```

---

## MILESTONE 4: Tool Search - Search Files (Exploration Flow)

A workflow allowing the Agent to scan the project's directory tree to find file locations by keyword, automatically ignoring junk/hidden directories (`.git`, `.venv`, `__pycache__`).

```mermaid
sequenceDiagram
    actor User as User
    participant Agent as SimpleAgent
    participant LLM as Groq Cloud API
    participant Exec as ToolExecutor (SearchTool)
    participant Disk as Local File System

    User->>Agent: 1. Request: "Check if there is any helper file"
    Agent->>LLM: 2. Send Prompt with Tools list
    LLM-->>Agent: 3. Return command <TOOL>search_files|{"query": "helper"}</TOOL>
    
    Note over Agent: 4. Use Regex to extract Tool name & Parameters
    
    Agent->>Exec: 5. Forward search command
    Exec->>Disk: 6. Scan project files (skip hidden dirs, venv)
    Disk-->>Exec: Return: ["output/utils/math_helper.py"]
    Exec-->>Agent: 7. Return relative file list (Observation)
    
    Agent->>LLM: 8. Send search result to LLM
    LLM-->>Agent: 9. Synthesize final confirmation answer
    Agent->>User: 10. Reply: "I found math_helper.py at..."
```

---

## MILESTONE 5: Tool Terminal - Execute Shell Command (OS Interaction Flow)

A workflow allowing the Agent to interact directly with the operating system via Shell/CLI commands (with a 10s Timeout mechanism and safe encoding), helping the Agent auto-run code, test, and read error logs.

```mermaid
sequenceDiagram
    actor User as User
    participant Agent as SimpleAgent
    participant LLM as Groq Cloud API
    participant Exec as ToolExecutor (TerminalTool)
    participant OS as Operating System Shell

    User->>Agent: 1. Request: "Run test_json.py to see the result"
    Agent->>LLM: 2. Send Prompt with Tools list
    LLM-->>Agent: 3. Return command <TOOL>execute_command|{"command": "python test_json.py"}</TOOL>
    
    Note over Agent: 4. Use Regex to extract Tool name & Parameters
    
    Agent->>Exec: 5. Forward execution command
    Exec->>OS: 6. Run subprocess with 10s timeout
    OS-->>Exec: Return stdout / stderr / exit code
    Exec-->>Agent: 7. Return Terminal result (Observation)
    
    Agent->>LLM: 8. Send Terminal result to LLM
    LLM-->>Agent: 9. Synthesize final integrated answer
    Agent->>User: 10. Reply directly with the execution result
```

---

## MILESTONE 6: Agent Loop (Self-Reasoning & Self-Correction Loop)

Automated multi-step workflow (ReAct Pattern): The Agent maintains interaction history (`history_messages`), automatically calls multiple tools in succession (e.g., create file ➔ run terminal ➔ read error ➔ self-correct), and only stops when the goal is achieved or the `max_iterations` threshold is hit.

```mermaid
sequenceDiagram
    actor User as User
    participant Agent as SimpleAgent (Agent Loop)
    participant LLM as Groq Cloud API
    participant Exec as ToolExecutor
    
    User->>Agent: 1. Multi-step request (e.g., "Create test_add.py and run it to check for errors")
    
    loop Agent Loop (Max N times, e.g., 10 steps, 3s delay/step)
        Agent->>LLM: 2. Send System Prompt + Context History
        LLM-->>Agent: 3. Response from LLM
        
        alt LLM wants to call a Tool (<TOOL>...</TOOL>)
            Note over Agent: 4. Extract Tool & Parameters
            Agent->>Exec: 5. Execute Tool (WriteFile / Terminal / Search...)
            Exec-->>Agent: 6. Return Observation result
            Note over Agent: 7. Log Observation into Context History & Continue loop
        else LLM replies directly (No <TOOL>)
            Note over Agent: 8. Goal achieved! Break from the loop.
        end
    end
    
    Agent->>User: 9. Return final synthesized answer
```

---

## MILESTONE 7: Context Management (Context Optimization & Memory Truncation)

A smart filter standing between the Agent and the LLM, trimming overly long Tool results and applying a Sliding Window to the conversation history. Ensures the Agent never exceeds the Token limit and saves API costs.

```mermaid
sequenceDiagram
    actor Agent as SimpleAgent
    participant CM as ContextManager
    participant LLM as Groq Cloud API

    Agent->>CM: 1. Push new message (User Prompt / Tool Observation)
    
    Note over CM: 2. Check Observation length<br/>(If > Max Chars ➔ Truncate the middle)
    
    Note over CM: 3. Check Message count in History<br/>(If > Max Messages ➔ Apply Sliding Window)
    
    Agent->>CM: 4. Request full formatted Context
    CM-->>Agent: 5. Return optimized Prompt (Clean & Concise)
    
    Agent->>LLM: 6. Send optimized Prompt to LLM (Saves 70-90% Tokens)
```