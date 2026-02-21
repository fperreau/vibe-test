#!/usr/bin/env python3
"""
Tests for cli_tutorial.py - the tutorial CLI task manager.

Run with:
    python -m pytest test_cli_tutorial.py -v
"""

import json
import os
import tempfile

import pytest

from cli_tutorial import (
    build_parser,
    cmd_add,
    cmd_done,
    cmd_list,
    cmd_remove,
    cmd_stats,
    get_next_id,
    load_tasks,
    main,
    save_tasks,
)


@pytest.fixture
def tmp_tasks_file(tmp_path):
    """Return a path to a temporary tasks JSON file."""
    return str(tmp_path / "tasks.json")


@pytest.fixture
def populated_tasks_file(tmp_path):
    """Return a tasks file pre-populated with sample data."""
    filepath = str(tmp_path / "tasks.json")
    tasks = [
        {
            "id": 1,
            "description": "Buy milk",
            "priority": "low",
            "status": "pending",
            "created_at": "2026-01-01T00:00:00+00:00",
        },
        {
            "id": 2,
            "description": "Write tests",
            "priority": "high",
            "status": "done",
            "created_at": "2026-01-02T00:00:00+00:00",
        },
        {
            "id": 3,
            "description": "Deploy app",
            "priority": "medium",
            "status": "pending",
            "created_at": "2026-01-03T00:00:00+00:00",
        },
    ]
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(tasks, f)
    return filepath


# ---------------------------------------------------------------------------
# load_tasks / save_tasks
# ---------------------------------------------------------------------------


class TestLoadSave:
    def test_load_missing_file(self, tmp_path):
        result = load_tasks(str(tmp_path / "nonexistent.json"))
        assert result == []

    def test_load_empty_file(self, tmp_path):
        filepath = str(tmp_path / "empty.json")
        with open(filepath, "w") as f:
            f.write("")
        assert load_tasks(filepath) == []

    def test_load_invalid_json(self, tmp_path):
        filepath = str(tmp_path / "bad.json")
        with open(filepath, "w") as f:
            f.write("{not valid json")
        assert load_tasks(filepath) == []

    def test_load_non_list_json(self, tmp_path):
        filepath = str(tmp_path / "obj.json")
        with open(filepath, "w") as f:
            json.dump({"key": "value"}, f)
        assert load_tasks(filepath) == []

    def test_save_and_load_roundtrip(self, tmp_tasks_file):
        tasks = [{"id": 1, "description": "Test", "priority": "low", "status": "pending"}]
        save_tasks(tasks, tmp_tasks_file)
        loaded = load_tasks(tmp_tasks_file)
        assert loaded == tasks


# ---------------------------------------------------------------------------
# get_next_id
# ---------------------------------------------------------------------------


class TestGetNextId:
    def test_empty_list(self):
        assert get_next_id([]) == 1

    def test_single_task(self):
        assert get_next_id([{"id": 5}]) == 6

    def test_multiple_tasks(self):
        assert get_next_id([{"id": 1}, {"id": 3}, {"id": 2}]) == 4


# ---------------------------------------------------------------------------
# Subcommands via main()
# ---------------------------------------------------------------------------


class TestAddCommand:
    def test_add_basic(self, tmp_tasks_file, capsys):
        exit_code = main(["--file", tmp_tasks_file, "add", "Hello world"])
        assert exit_code == 0
        output = capsys.readouterr().out
        assert "Task #1 added" in output
        assert "Hello world" in output

        tasks = load_tasks(tmp_tasks_file)
        assert len(tasks) == 1
        assert tasks[0]["description"] == "Hello world"
        assert tasks[0]["priority"] == "medium"
        assert tasks[0]["status"] == "pending"

    def test_add_with_priority(self, tmp_tasks_file, capsys):
        main(["--file", tmp_tasks_file, "add", "Urgent thing", "--priority", "high"])
        tasks = load_tasks(tmp_tasks_file)
        assert tasks[0]["priority"] == "high"

    def test_add_increments_id(self, tmp_tasks_file):
        main(["--file", tmp_tasks_file, "add", "First"])
        main(["--file", tmp_tasks_file, "add", "Second"])
        tasks = load_tasks(tmp_tasks_file)
        assert tasks[0]["id"] == 1
        assert tasks[1]["id"] == 2


class TestListCommand:
    def test_list_empty(self, tmp_tasks_file, capsys):
        exit_code = main(["--file", tmp_tasks_file, "list"])
        assert exit_code == 0
        assert "No tasks found" in capsys.readouterr().out

    def test_list_all(self, populated_tasks_file, capsys):
        exit_code = main(["--file", populated_tasks_file, "list"])
        assert exit_code == 0
        output = capsys.readouterr().out
        assert "Buy milk" in output
        assert "Write tests" in output
        assert "Deploy app" in output

    def test_list_filter_status(self, populated_tasks_file, capsys):
        main(["--file", populated_tasks_file, "list", "--status", "done"])
        output = capsys.readouterr().out
        assert "Write tests" in output
        assert "Buy milk" not in output

    def test_list_filter_priority(self, populated_tasks_file, capsys):
        main(["--file", populated_tasks_file, "list", "--priority", "low"])
        output = capsys.readouterr().out
        assert "Buy milk" in output
        assert "Deploy app" not in output

    def test_list_no_match(self, populated_tasks_file, capsys):
        main(["--file", populated_tasks_file, "list", "--priority", "high", "--status", "pending"])
        output = capsys.readouterr().out
        assert "No tasks match" in output


class TestDoneCommand:
    def test_done_success(self, populated_tasks_file, capsys):
        exit_code = main(["--file", populated_tasks_file, "done", "1"])
        assert exit_code == 0
        assert "marked as done" in capsys.readouterr().out
        tasks = load_tasks(populated_tasks_file)
        assert tasks[0]["status"] == "done"

    def test_done_not_found(self, populated_tasks_file, capsys):
        exit_code = main(["--file", populated_tasks_file, "done", "999"])
        assert exit_code == 1
        assert "not found" in capsys.readouterr().err


class TestRemoveCommand:
    def test_remove_success(self, populated_tasks_file, capsys):
        exit_code = main(["--file", populated_tasks_file, "remove", "2"])
        assert exit_code == 0
        assert "removed" in capsys.readouterr().out
        tasks = load_tasks(populated_tasks_file)
        assert len(tasks) == 2
        assert all(t["id"] != 2 for t in tasks)

    def test_remove_not_found(self, populated_tasks_file, capsys):
        exit_code = main(["--file", populated_tasks_file, "remove", "999"])
        assert exit_code == 1
        assert "not found" in capsys.readouterr().err


class TestStatsCommand:
    def test_stats_empty(self, tmp_tasks_file, capsys):
        exit_code = main(["--file", tmp_tasks_file, "stats"])
        assert exit_code == 0
        output = capsys.readouterr().out
        assert "Total tasks:   0" in output

    def test_stats_populated(self, populated_tasks_file, capsys):
        main(["--file", populated_tasks_file, "stats"])
        output = capsys.readouterr().out
        assert "Total tasks:   3" in output
        assert "Pending:       2" in output
        assert "Completed:     1" in output
        assert "high" in output
        assert "low" in output


class TestMainEntryPoint:
    def test_no_command_shows_help(self, capsys):
        exit_code = main([])
        assert exit_code == 0
        output = capsys.readouterr().out
        assert "usage" in output.lower() or "Task Manager" in output

    def test_version(self, capsys):
        with pytest.raises(SystemExit) as exc_info:
            main(["--version"])
        assert exc_info.value.code == 0
