# vibe-test

A collection of tutorial examples for learning Python development.

## CLI Tutorial - Task Manager

[`cli_tutorial.py`](cli_tutorial.py) is a tutorial example showing how to build a Python CLI
program using `argparse`. It implements a simple task manager with the following
commands:

| Command  | Description                  | Example                                          |
|----------|------------------------------|--------------------------------------------------|
| `add`    | Create a new task            | `python cli_tutorial.py add "Buy groceries"`     |
| `list`   | Display tasks                | `python cli_tutorial.py list`                    |
| `done`   | Mark a task as completed     | `python cli_tutorial.py done 1`                  |
| `remove` | Delete a task                | `python cli_tutorial.py remove 1`                |
| `stats`  | Show summary statistics      | `python cli_tutorial.py stats`                   |

### Quick start

```bash
# Add some tasks
python cli_tutorial.py add "Write documentation" --priority high
python cli_tutorial.py add "Run the tests"
python cli_tutorial.py add "Take a break" --priority low

# List all tasks
python cli_tutorial.py list

# Filter by status or priority
python cli_tutorial.py list --status pending
python cli_tutorial.py list --priority high

# Complete a task
python cli_tutorial.py done 1

# View statistics
python cli_tutorial.py stats

# Remove a task
python cli_tutorial.py remove 2
```

### Global options

- `--file / -f` -- specify a custom tasks JSON file (default: `tasks.json`)
- `--version / -v` -- print the program version

### Key concepts demonstrated

- **Subcommands** via `argparse` subparsers (add, list, done, remove, stats)
- **Optional and positional arguments** with type validation and choices
- **JSON file persistence** for storing structured data
- **Clean function architecture** -- each command is a standalone function
- **Testable design** -- the `main()` function accepts an `argv` parameter

### Running the tests

```bash
python -m pytest test_cli_tutorial.py -v
```

## Other files

- [`calculatrice.py`](calculatrice.py) -- a tkinter GUI calculator
- [`test.py`](test.py) -- a minimal argparse example