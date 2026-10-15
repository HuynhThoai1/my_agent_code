from tools.delete_file import DeleteFileTool
from tools.move_file import MoveFileTool
from tools.read_file import ReadFileTool
from tools.rename_file import RenameFileTool
from tools.search_files import SearchFilesTool
from tools.write_file import WriteFileTool


def test_read_file_success(tmp_path):
    target = tmp_path / "note.txt"
    target.write_text("hello", encoding="utf-8")

    result = ReadFileTool(str(tmp_path)).execute({"file_path": "note.txt"})

    assert result.status == "success"
    assert result.output["content"] == "hello"


def test_read_file_missing(tmp_path):
    result = ReadFileTool(str(tmp_path)).execute({"file_path": "missing.txt"})

    assert result.status == "error"
    assert result.error == "File not found"


def test_read_file_blocks_path_traversal(tmp_path):
    result = ReadFileTool(str(tmp_path)).execute({"file_path": "../secret.txt"})

    assert result.status == "error"
    assert "outside" in result.error


def test_write_file_inside_workspace(tmp_path):
    result = WriteFileTool(str(tmp_path)).execute({"file_path": "nested/out.txt", "content": "saved"})

    assert result.status == "success"
    assert (tmp_path / "nested" / "out.txt").read_text(encoding="utf-8") == "saved"


def test_search_files_ignores_junk_dirs(tmp_path):
    (tmp_path / "keep_main.py").write_text("", encoding="utf-8")
    hidden = tmp_path / ".git"
    hidden.mkdir()
    (hidden / "main.py").write_text("", encoding="utf-8")

    result = SearchFilesTool(str(tmp_path)).execute({"query": "main"})

    assert result.status == "success"
    assert result.output["matches"] == ["keep_main.py"]


def test_move_rename_and_delete_file(tmp_path):
    (tmp_path / "a.txt").write_text("content", encoding="utf-8")

    moved = MoveFileTool(str(tmp_path)).execute(
        {"source_path": "a.txt", "destination_path": "folder/b.txt"}
    )
    assert moved.status == "success"
    assert (tmp_path / "folder" / "b.txt").exists()

    renamed = RenameFileTool(str(tmp_path)).execute({"file_path": "folder/b.txt", "new_name": "c.txt"})
    assert renamed.status == "success"
    assert (tmp_path / "folder" / "c.txt").exists()

    denied = DeleteFileTool(str(tmp_path)).execute({"file_path": "folder/c.txt"})
    assert denied.status == "error"
    assert "confirm=true" in denied.error

    deleted = DeleteFileTool(str(tmp_path)).execute({"file_path": "folder/c.txt", "confirm": True})
    assert deleted.status == "success"
    assert not (tmp_path / "folder" / "c.txt").exists()
