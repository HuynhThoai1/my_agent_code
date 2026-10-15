from core.config import AppConfig
from main import build_llm_client, build_registry


def test_build_registry_registers_foundation_tools(tmp_path):
    registry = build_registry(str(tmp_path))

    expected = {
        "read_file",
        "write_file",
        "search_files",
        "move_file",
        "rename_file",
        "delete_file",
        "execute_command",
    }
    assert expected.issubset(set(registry.tools))


def test_groq_provider_reports_missing_api_key(monkeypatch, tmp_path):
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    config = AppConfig(
        provider="groq",
        model="llama-3.1-8b-instant",
        workspace_dir=str(tmp_path),
        log_level="INFO",
    )

    try:
        build_llm_client(config)
    except ValueError as e:
        assert "GROQ_API_KEY is missing" in str(e)
    else:
        raise AssertionError("Expected ValueError")
