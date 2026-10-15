import ast
import json
from typing import Any, Dict


def robust_parse_json(text: str) -> Dict[str, Any]:
    """Parse JSON-like tool parameters returned by an LLM."""
    cleaned = text.strip()
    if cleaned.startswith("```json"):
        cleaned = cleaned[7:]
    elif cleaned.startswith("```"):
        cleaned = cleaned[3:]
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]
    cleaned = cleaned.strip()

    try:
        result = json.loads(cleaned, strict=False)
    except Exception as json_error:
        try:
            result = ast.literal_eval(cleaned)
        except Exception as ast_error:
            start = cleaned.find("{")
            end = cleaned.rfind("}")
            if start != -1 and end != -1:
                try:
                    result = json.loads(cleaned[start : end + 1], strict=False)
                except Exception:
                    pass
            else:
                result = None
            if result is None:
                raise ValueError(f"JSONDecodeError: {json_error} | ASTError: {ast_error}")

    if not isinstance(result, dict):
        raise ValueError("Tool parameters must be a JSON object")
    return result
