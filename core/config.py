import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class AppConfig:
    provider: str
    model: str
    workspace_dir: str
    log_level: str


def load_config(provider: Optional[str] = None, model: Optional[str] = None) -> AppConfig:
    selected_provider = (provider or os.environ.get("AGENT_MODEL_PROVIDER") or "groq").lower()
    default_model = "llama-3.1-8b-instant" if selected_provider == "groq" else "deepseek-r1:235b-cloud-q4"

    return AppConfig(
        provider=selected_provider,
        model=model or os.environ.get("AGENT_MODEL") or default_model,
        workspace_dir=os.path.abspath(os.environ.get("AGENT_WORKSPACE_DIR") or os.getcwd()),
        log_level=os.environ.get("AGENT_LOG_LEVEL", "INFO").upper(),
    )
