#!/usr/bin/env python3
"""
CLI Tutorial - A Python command-line interface example.

This module demonstrates how to build a proper Python CLI application using
argparse. It provides a simple task manager that supports adding, listing,
and completing tasks, all stored in a local JSON file.

Usage examples:
    python cli_tutorial.py add "Buy groceries"
    python cli_tutorial.py add "Write docs" --priority high
    python cli_tutorial.py list
    python cli_tutorial.py list --status pending
    python cli_tutorial.py done 1
    python cli_tutorial.py remove 1
    python cli_tutorial.py stats
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone


# Default file where tasks are stored
DEFAULT_TASKS_FILE = "tasks.json"


def load_tasks(filepath):
    """
    Load tasks from a JSON file.

    Args:
        filepath (str): Path to the JSON tasks file.

    Returns:
        list[dict]: A list of task dictionaries. Returns an empty list
        if the file does not exist or is empty.
    """
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, IOError):
        return []


def save_tasks(tasks, filepath):
    """
    Save tasks to a JSON file.

    Args:
        tasks (list[dict]): The list of task dictionaries to persist.
        filepath (str): Path to the JSON tasks file.
    """
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)


def get_next_id(tasks):
    """
    Compute the next available task ID.

    Args:
        tasks (list[dict]): Current list of tasks.

    Returns:
        int: The next ID to use.
    """
    if not tasks:
        return 1
    return max(task["id"] for task in tasks) + 1


def cmd_add(args):
    """
    Handle the 'add' subcommand: create a new task.

    Args:
        args: Parsed argparse namespace with 'description', 'priority',
              and 'file' attributes.

    Returns:
        int: Exit code (0 for success).
    """
    tasks = load_tasks(args.file)
    new_task = {
        "id": get_next_id(tasks),
        "description": args.description,
        "priority": args.priority,
        "status": "pending",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    tasks.append(new_task)
    save_tasks(tasks, args.file)
    print(f"Task #{new_task['id']} added: {new_task['description']} [{new_task['priority']}]")
    return 0


def cmd_list(args):
    """
    Handle the 'list' subcommand: display tasks.

    Args:
        args: Parsed argparse namespace with optional 'status', 'priority',
              and 'file' attributes.

    Returns:
        int: Exit code (0 for success).
    """
    tasks = load_tasks(args.file)

    if not tasks:
        print("No tasks found.")
        return 0

    # Apply filters
    filtered = tasks
    if args.status:
        filtered = [t for t in filtered if t["status"] == args.status]
    if args.priority:
        filtered = [t for t in filtered if t["priority"] == args.priority]

    if not filtered:
        print("No tasks match the given filters.")
        return 0

    # Display header
    print(f"{'ID':<5} {'Status':<10} {'Priority':<10} {'Description'}")
    print("-" * 50)

    for task in filtered:
        status_icon = "[x]" if task["status"] == "done" else "[ ]"
        print(f"{task['id']:<5} {status_icon:<10} {task['priority']:<10} {task['description']}")

    return 0


def cmd_done(args):
    """
    Handle the 'done' subcommand: mark a task as completed.

    Args:
        args: Parsed argparse namespace with 'task_id' and 'file' attributes.

    Returns:
        int: Exit code (0 for success, 1 for not found).
    """
    tasks = load_tasks(args.file)

    for task in tasks:
        if task["id"] == args.task_id:
            task["status"] = "done"
            save_tasks(tasks, args.file)
            print(f"Task #{args.task_id} marked as done.")
            return 0

    print(f"Error: Task #{args.task_id} not found.", file=sys.stderr)
    return 1


def cmd_remove(args):
    """
    Handle the 'remove' subcommand: delete a task.

    Args:
        args: Parsed argparse namespace with 'task_id' and 'file' attributes.

    Returns:
        int: Exit code (0 for success, 1 for not found).
    """
    tasks = load_tasks(args.file)
    original_len = len(tasks)
    tasks = [t for t in tasks if t["id"] != args.task_id]

    if len(tasks) == original_len:
        print(f"Error: Task #{args.task_id} not found.", file=sys.stderr)
        return 1

    save_tasks(tasks, args.file)
    print(f"Task #{args.task_id} removed.")
    return 0


def cmd_stats(args):
    """
    Handle the 'stats' subcommand: show task statistics.

    Args:
        args: Parsed argparse namespace with 'file' attribute.

    Returns:
        int: Exit code (0 for success).
    """
    tasks = load_tasks(args.file)
    total = len(tasks)
    done = sum(1 for t in tasks if t["status"] == "done")
    pending = total - done

    by_priority = {}
    for task in tasks:
        p = task["priority"]
        by_priority[p] = by_priority.get(p, 0) + 1

    print(f"Total tasks:   {total}")
    print(f"Pending:       {pending}")
    print(f"Completed:     {done}")
    if by_priority:
        print("\nBy priority:")
        for priority in ["high", "medium", "low"]:
            if priority in by_priority:
                print(f"  {priority:<10} {by_priority[priority]}")

    return 0


def build_parser():
    """
    Build and return the argument parser for the CLI.

    Returns:
        argparse.ArgumentParser: The fully configured parser with all
        subcommands registered.
    """
    parser = argparse.ArgumentParser(
        prog="cli_tutorial",
        description="Task Manager CLI - A tutorial example for building Python CLI programs.",
        epilog="Run '%(prog)s COMMAND --help' for more information on a command.",
    )
    parser.add_argument(
        "--file", "-f",
        default=DEFAULT_TASKS_FILE,
        help=f"Path to the tasks JSON file (default: {DEFAULT_TASKS_FILE})",
    )
    parser.add_argument(
        "--version", "-v",
        action="version",
        version="%(prog)s 1.0.0",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # --- add ---
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("description", type=str, help="Task description")
    add_parser.add_argument(
        "--priority", "-p",
        choices=["low", "medium", "high"],
        default="medium",
        help="Task priority (default: medium)",
    )
    add_parser.set_defaults(func=cmd_add)

    # --- list ---
    list_parser = subparsers.add_parser("list", help="List tasks")
    list_parser.add_argument(
        "--status", "-s",
        choices=["pending", "done"],
        default=None,
        help="Filter by status",
    )
    list_parser.add_argument(
        "--priority", "-p",
        choices=["low", "medium", "high"],
        default=None,
        help="Filter by priority",
    )
    list_parser.set_defaults(func=cmd_list)

    # --- done ---
    done_parser = subparsers.add_parser("done", help="Mark a task as done")
    done_parser.add_argument("task_id", type=int, help="ID of the task to complete")
    done_parser.set_defaults(func=cmd_done)

    # --- remove ---
    remove_parser = subparsers.add_parser("remove", help="Remove a task")
    remove_parser.add_argument("task_id", type=int, help="ID of the task to remove")
    remove_parser.set_defaults(func=cmd_remove)

    # --- stats ---
    stats_parser = subparsers.add_parser("stats", help="Show task statistics")
    stats_parser.set_defaults(func=cmd_stats)

    return parser


def main(argv=None):
    """
    Entry point for the CLI application.

    Args:
        argv (list[str] | None): Command-line arguments. Defaults to sys.argv
            when None.

    Returns:
        int: Exit code.
    """
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        return 0

    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
