import os


def resolve_workspace_path(workspace_dir: str, file_path: str) -> str:
    if not file_path:
        raise ValueError("Missing file_path")

    cleaned = file_path.strip().lstrip("/\\")
    workspace = os.path.abspath(workspace_dir)
    absolute_path = os.path.abspath(os.path.join(workspace, cleaned))

    if os.path.commonpath([workspace, absolute_path]) != workspace:
        raise PermissionError("Path is outside the configured workspace")

    return absolute_path
