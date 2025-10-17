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

    args = parser.parse_args()

    if args.command == "create-project":
        create_project(repo, args.name, args.description)
    elif args.command == "list-projects":
        list_projects(repo)


if __name__ == "__main__":
    main()
