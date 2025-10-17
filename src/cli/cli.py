# src/cli.py

from typing import List, Union, Dict, Any, Optional
from datetime import date
from src.models.project import Project
from src.models.task import Task, StatusType


# --- UTILITY DISPLAY FUNCTIONS ---

def _format_date(d: Optional[date]) -> str:
    """Formats a date object for display or returns 'N/A'."""
    return d.strftime("%Y-%m-%d") if d else "N/A"


def _color_status(status: StatusType) -> str:
    """A placeholder for adding color/style to status (CLI libraries like 'colorama' would be used in a real app)."""
    # In a simple terminal, we'll just return the status for now
    return status.upper()


# --- MAIN MENU & INPUT PROMPTS ---

def display_main_menu() -> None:
    """Displays the main menu options."""
    print("\n" + "=" * 40)
    print("      📝 ToDo List CLI")
    print("=" * 40)
    print("1. ➕ Create New Project")
    print("2. 📋 List All Projects")
    print("3. ✍️  Edit Project")
    print("4. 🗑️  Delete Project")
    print("5. 🚪 Exit Application")
    print("-" * 40)


def prompt_for_main_choice() -> Optional[int]:
    """Prompts the user for a main menu choice."""
    try:
        choice = input("Enter your choice (1-5): ").strip()
        if not choice:  # Handle empty input gracefully
            return None
        return int(choice)
    except ValueError:
        return None


def prompt_for_project_data(is_edit: bool = False) -> Dict[str, str]:
    """Prompts the user for Project Name and Description."""
    action = "new" if not is_edit else "edited"
    print(f"\n--- Enter {action.capitalize()} Project Details ---")
    name = input("Enter project name: ").strip()
    description = input("Enter project description: ").strip()
    return {"name": name, "description": description}


def prompt_for_project_id(action: str) -> Optional[int]:
    """Prompts the user for a Project ID for a specific action."""
    try:
        project_id_str = input(f"Enter the ID of the project to {action}: ").strip()
        if not project_id_str:
            return None
        return int(project_id_str)
    except ValueError:
        return None


# --- PROJECT LISTING & DETAILS ---

def display_projects_list(projects: List[Project]) -> bool:
    """Displays a list of all projects with their IDs and task counts."""
    if not projects:
        print("\nNo projects found. Start by creating one (Option 1).")
        return False

    print("\n" + "--- All Projects ---")
    for project in projects:
        task_count = len(project.tasks)
        print(f"[{project.id}] {project.name} (Tasks: {task_count})")
        print(f"    Description: {project.description[:70]}...")  # Truncate description for list view
    print("-" * 20)
    return True


def display_project_details_and_menu(project: Project) -> None:
    """Displays detailed project information and the task management menu."""
    print("\n" + "=" * 40)
    print(f"      Project: {project.name} (ID: {project.id})")
    print("=" * 40)
    print(f"Description: {project.description}")
    print(f"Total Tasks: {len(project.tasks)}")
    print("-" * 40)
    print("1. Add New Task")
    print("2. List Tasks")
    print("3. Edit Task")
    print("4. Change Task Status")
    print("5. Delete Task")
    print("6. Return to Main Menu")
    print("-" * 40)


def prompt_for_task_menu_choice() -> Optional[int]:
    """Prompts the user for a task menu choice."""
    try:
        choice = input("Enter your choice (1-6): ").strip()
        if not choice:
            return None
        return int(choice)
    except ValueError:
        return None


# --- TASK INPUT PROMPTS ---

def prompt_for_task_data(is_edit: bool = False) -> Dict[str, Union[str, None]]:
    """Prompts the user for Task Title, Description, Status, and Deadline."""
    action = "new" if not is_edit else "edited"
    print(f"\n--- Enter {action.capitalize()} Task Details ---")

    title = input("Enter task title: ").strip()
    description = input("Enter task description: ").strip()
    status = input("Enter status (todo/doing/done): ").strip().lower()
    deadline = input("Enter deadline (YYYY-MM-DD): ").strip()

    return {
        "title": title if title else None,
        "description": description if description else None,
        "status": status if status else None,
        "deadline": deadline if deadline else None
    }


def prompt_for_task_id(action: str) -> Optional[int]:
    """Prompts the user for a Task ID for a specific action."""
    try:
        task_id_str = input(f"Enter the ID of the task to {action}: ").strip()
        if not task_id_str:
            return None
        return int(task_id_str)
    except ValueError:
        return None


def prompt_for_new_status() -> Optional[str]:
    """Prompts the user for a new task status."""
    status = input("Enter new status (todo/doing/done): ").strip().lower()
    return status if status else None


# --- TASK LISTING & MESSAGES ---

def display_tasks_list(project: Project) -> None:
    """Displays all tasks for a given project."""
    tasks = project.tasks
    print(f"\n--- Tasks for Project '{project.name}' (ID: {project.id}) ---")
    if not tasks:
        print("No tasks in this project. Start by adding one (Option 1).")
        return

    # Header
    print(f"{'ID':<4} | {'STATUS':<12} | {'DEADLINE':<12} | {'TITLE':<30}")
    print("-" * 65)

    # List tasks
    for task in tasks:
        status_display = _color_status(task.status)
        deadline_display = _format_date(task.deadline)
        print(f"{task.id:<4} | {status_display:<12} | {deadline_display:<12} | {task.title:<30}")
        # print(f"       Description: {task.description}") # Optionally display description


# --- SYSTEM & ERROR MESSAGES ---

def display_success(message: str) -> None:
    """Displays a success message."""
    print(f"\n✅ Success: {message}")


def display_error(message: str) -> None:
    """Displays an error message."""
    print(f"\n❌ Error: {message}")


def display_message(message: str) -> None:
    """Displays a general message."""
    print(f"\n{message}")


def display_exit_message() -> None:
    """Displays the farewell message."""
    print("\n👋 Thank you for using the ToDo List CLI. Goodbye!")