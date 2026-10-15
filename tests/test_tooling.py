from typing import Any, Dict

from core.contracts import ToolResult
from core.parsing import robust_parse_json
from core.tool_executor import ToolExecutor
from core.tool_registry import ToolRegistry
from tools.base_tool import BaseTool


class EchoTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="echo",
            description="Echo parameters.",
            parameters={"value": "Any value."},
        )

    def execute(self, parameters: Dict[str, Any]) -> ToolResult:
        return ToolResult.success(echo=parameters)


def test_registry_and_executor_success():
    registry = ToolRegistry()
    registry.register(EchoTool())
    executor = ToolExecutor(registry)

    result = executor.execute("echo", {"value": "ok"})

    assert result.status == "success"
    assert result.output["echo"] == {"value": "ok"}
    assert "echo" in registry.get_tool_descriptions()


def test_executor_unknown_tool():
    result = ToolExecutor(ToolRegistry()).execute("missing", {})

    assert result.status == "error"
    assert "not found" in result.error


def test_parse_json_object():
    assert robust_parse_json('{"file_path": "README.md"}') == {"file_path": "README.md"}


def test_parse_json_markdown_block():
    assert robust_parse_json('```json\n{"query": "main"}\n```') == {"query": "main"}


def test_parse_malformed_json_has_useful_error():
    try:
        robust_parse_json("{bad")
    except ValueError as e:
        assert "JSONDecodeError" in str(e)
    else:
        raise AssertionError("Expected ValueError")
