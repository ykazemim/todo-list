"""
Command-Line Interface (CLI) for the ToDo List application.

Handles user commands for managing projects and tasks.
Uses argparse for parsing commands and integrates with InMemoryRepository.
"""

import argparse
from src.repositories.memory_repository import InMemoryRepository, ValidationError


def create_project(repo: InMemoryRepository, name: str, description: str) -> None:
    """Create a new project."""
    try:
        repo.add_project(name, description)
        print(f"✅ Project '{name}' created successfully.")
    except ValidationError as e:
        print(f"❌ Error: {e}")


def list_projects(repo: InMemoryRepository) -> None:
    """List all existing projects."""
    projects = repo.list_all_projects()
    if not projects:
        print("No projects found.")
        return

    print("📁 Projects:")
    for project in projects:
        print(f"[{project.id}] {project.name} — {project.description}")


def main() -> None:
    """Main entry point for the CLI."""
    repo = InMemoryRepository()

    parser = argparse.ArgumentParser(
        description="ToDo List CLI - Manage projects and tasks"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Create project
    create_parser = subparsers.add_parser("create-project", help="Create a new project")
    create_parser.add_argument("name", type=str, help="Project name")
    create_parser.add_argument("description", type=str, help="Project description")

    # List projects
    subparsers.add_parser("list-projects", help="List all projects")

    # Edit task
    edit_task_parser = subparsers.add_parser("edit-task", help="Edit a task")
    edit_task_parser.add_argument("project_id", type=int, help="ID of the project")
    edit_task_parser.add_argument("task_id", type=int, help="ID of the task")
    edit_task_parser.add_argument("--title", type=str, help="New title")
    edit_task_parser.add_argument("--description", type=str, help="New description")
    edit_task_parser.add_argument("--status", type=str, choices=["todo", "doing", "done"], help="New status")
    edit_task_parser.add_argument("--deadline", type=str, help="New deadline (YYYY-MM-DD)")
    edit_project_parser = subparsers.add_parser("edit-project", help="Edit a project's name and description")
    edit_project_parser.add_argument("project_id", type=int, help="ID of the project")
    edit_project_parser.add_argument("new_name", type=str, help="New name for the project")
    edit_project_parser.add_argument("new_description", type=str, help="New description for the project")

    # Delete task
    delete_task_parser = subparsers.add_parser("delete-task", help="Delete a task")
    delete_task_parser.add_argument("project_id", type=int, help="ID of the project")
    delete_task_parser.add_argument("task_id", type=int, help="ID of the task")
    delete_project_parser = subparsers.add_parser("delete-project", help="Delete a project")
    delete_project_parser.add_argument("project_id", type=int, help="ID of the project")

    args = parser.parse_args()

    if args.command == "create-project":
        create_project(repo, args.name, args.description)
    elif args.command == "list-projects":
        list_projects(repo)
    elif args.command == "add-task":
        add_task(repo, args.project_id, args.title, args.description, args.status, args.deadline)
    elif args.command == "list-tasks":
        list_tasks(repo, args.project_id)
    elif args.command == "edit-project":
        edit_project_cli(repo, args.project_id, args.new_name, args.new_description)
    elif args.command == "delete-project":
        delete_project_cli(repo, args.project_id)


def add_task(
        repo: InMemoryRepository,
        project_id: int,
        title: str,
        description: str,
        status: str = "todo",
        deadline: str | None = None,
) -> None:
    """Add a task to a specific project."""
    try:
        repo.add_task(project_id, title, description, status, deadline)
        print(f"✅ Task '{title}' added to project ID {project_id}.")
    except ValidationError as e:
        print(f"❌ Error: {e}")


def list_tasks(repo: InMemoryRepository, project_id: int) -> None:
    """List all tasks for a specific project."""
    try:
        tasks = repo.list_tasks(project_id)
    except ValidationError as e:
        print(f"❌ Error: {e}")
        return

    if not tasks:
        print(f"No tasks found for project ID {project_id}.")
        return

    print(f"📝 Tasks for Project ID {project_id}:")
    for task in tasks:
        print(f"[{task.id}] {task.title} ({task.status}) — {task.deadline or 'No deadline'}")


def edit_project_cli(repo: InMemoryRepository, project_id: int, new_name: str, new_description: str) -> None:
    """CLI handler for editing a project's name and description."""
    try:
        repo.edit_project(project_id, new_name, new_description)
        print(f"✅ Project {project_id} updated successfully.")
    except ValidationError as e:
        print(f"❌ Error: {e}")


def delete_project_cli(repo: InMemoryRepository, project_id: int) -> None:
    """CLI handler for deleting a project."""
    try:
        repo.delete_project(project_id)
        print(f"🗑️ Project {project_id} deleted successfully.")
    except ValidationError as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
