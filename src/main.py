"""Main application entry point.

DEPRECATED: The CLI interface is deprecated and will be removed in a future version.
Please use the Web API instead: uvicorn src.api.app:app --reload
"""

import sys
import warnings
from typing import Literal, cast

from src.cli.cli import (
    display_main_menu,
    prompt_for_main_choice,
    prompt_for_project_data,
    prompt_for_project_id,
    display_projects_list,
    display_project_details_and_menu,
    prompt_for_task_menu_choice,
    prompt_for_task_data,
    prompt_for_task_id,
    prompt_for_new_status,
    display_tasks_list,
    display_success,
    display_error,
    display_exit_message,
)
from src.db.session import get_session
from src.repositories.project_repository import ProjectRepository
from src.repositories.task_repository import TaskRepository
from src.services.project_service import ProjectService
from src.services.task_service import TaskService
from src.exceptions import (
    ValidationError,
    ProjectNotFoundError,
    TaskNotFoundError,
    LimitExceededError,
)
from src.models.project import Project


# --- PROJECT MANAGEMENT HANDLERS ---

def handle_create_project(project_service: ProjectService) -> None:
    """Handles the creation of a new project."""
    try:
        data = prompt_for_project_data(is_edit=False)
        project = project_service.create_project(
            name=data["name"], description=data["description"]
        )
        display_success(
            f"Project '{project.name}' (ID: {project.id}) created successfully!"
        )
    except (ValidationError, LimitExceededError) as e:
        display_error(str(e))
    except Exception:
        display_error("An unexpected error occurred during project creation.")


def handle_list_projects(project_service: ProjectService) -> None:
    """Handles listing all projects."""
    projects = project_service.list_projects()
    display_projects_list(projects)


def handle_edit_project(project_service: ProjectService) -> None:
    """Handles editing an existing project."""
    projects = project_service.list_projects()
    if not projects:
        display_error("No projects to edit.")
        return

    handle_list_projects(project_service)
    project_id = prompt_for_project_id("edit")
    if project_id is None:
        return

    try:
        data = prompt_for_project_data(is_edit=True)
        # Only proceed with update if name or description are provided
        if not data["name"] and not data["description"]:
            display_error(
                "Both project name and description cannot be empty for edit."
            )
            return

        # Fetch current project to get existing values if new ones are empty
        current_project = project_service.get_project(project_id)
        new_name = data["name"] if data["name"] else current_project.name
        new_description = (
            data["description"]
            if data["description"]
            else current_project.description
        )

        project = project_service.update_project(
            project_id, new_name, new_description
        )
        display_success(
            f"Project '{project.name}' (ID: {project.id}) updated successfully."
        )
    except (ProjectNotFoundError, ValidationError) as e:
        display_error(str(e))
    except Exception:
        display_error("An unexpected error occurred during project editing.")


def handle_delete_project(project_service: ProjectService) -> None:
    """Handles deleting a project."""
    projects = project_service.list_projects()
    if not projects:
        display_error("No projects to delete.")
        return

    handle_list_projects(project_service)
    project_id = prompt_for_project_id("delete")
    if project_id is None:
        return

    try:
        project_service.delete_project(project_id)
        display_success(
            f"Project (ID: {project_id}) deleted successfully (including all tasks)."
        )
    except ProjectNotFoundError as e:
        display_error(str(e))
    except Exception:
        display_error("An unexpected error occurred during project deletion.")


# --- TASK MANAGEMENT HANDLERS ---

def handle_add_task(
    task_service: TaskService, project_service: ProjectService, project_id: int
) -> None:
    """Handles adding a new task to a project."""
    try:
        data = prompt_for_task_data(is_edit=False)
        task = task_service.create_task(
            project_id=project_id,
            title=data["title"],
            description=data["description"],
            status=data["status"] if data["status"] else "todo",
            deadline=data["deadline"],
        )
        display_success(f"Task '{task.title}' (ID: {task.id}) added to project.")
    except (ValidationError, ProjectNotFoundError, LimitExceededError) as e:
        display_error(str(e))
    except Exception:
        display_error("An unexpected error occurred during task creation.")


def handle_list_tasks(
    task_service: TaskService, project: Project
) -> None:
    """Handles listing tasks for a project."""
    # Refresh project with tasks from database
    tasks = task_service.list_tasks(project.id)
    project.tasks = tasks
    display_tasks_list(project)


def handle_edit_task(
    task_service: TaskService, project_service: ProjectService, project_id: int
) -> None:
    """Handles editing an existing task."""
    try:
        project = project_service.get_project(project_id)
        tasks = task_service.list_tasks(project_id)
        if not tasks:
            display_error("No tasks to edit in this project.")
            return

        project.tasks = tasks
        handle_list_tasks(task_service, project)
        task_id = prompt_for_task_id("edit")
        if task_id is None:
            return

        data = prompt_for_task_data(is_edit=True)
        updates = {k: v for k, v in data.items() if v is not None}

        if not updates:
            display_error("No fields were provided for update.")
            return

        task = task_service.update_task(project_id, task_id, **updates)
        display_success(
            f"Task '{task.title}' (ID: {task.id}) updated successfully."
        )
    except (ProjectNotFoundError, TaskNotFoundError, ValidationError) as e:
        display_error(str(e))
    except Exception:
        display_error("An unexpected error occurred during task editing.")


def handle_change_task_status(
    task_service: TaskService, project_service: ProjectService, project_id: int
) -> None:
    """Handles changing the status of a task."""
    try:
        project = project_service.get_project(project_id)
        tasks = task_service.list_tasks(project_id)
        if not tasks:
            display_error("No tasks to change status.")
            return

        project.tasks = tasks
        handle_list_tasks(task_service, project)
        task_id = prompt_for_task_id("change status")
        if task_id is None:
            return

        new_status_str = prompt_for_new_status()
        if not new_status_str:
            return

        if new_status_str not in ("todo", "doing", "done"):
            display_error(
                f"Invalid status: {new_status_str}. Must be one of: todo, doing, done."
            )
            return

        new_status = cast(Literal["todo", "doing", "done"], new_status_str)
        task = task_service.change_task_status(project_id, task_id, new_status)
        display_success(
            f"Status of Task '{task.title}' (ID: {task.id}) changed to {task.status.upper()}."
        )
    except (ProjectNotFoundError, TaskNotFoundError, ValidationError) as e:
        display_error(str(e))
    except Exception:
        display_error("An unexpected error occurred while changing task status.")


def handle_delete_task(
    task_service: TaskService, project_service: ProjectService, project_id: int
) -> None:
    """Handles deleting a task."""
    try:
        project = project_service.get_project(project_id)
        tasks = task_service.list_tasks(project_id)
        if not tasks:
            display_error("No tasks to delete in this project.")
            return

        project.tasks = tasks
        handle_list_tasks(task_service, project)
        task_id = prompt_for_task_id("delete")
        if task_id is None:
            return

        task_service.delete_task(project_id, task_id)
        display_success(f"Task (ID: {task_id}) deleted successfully.")
    except (ProjectNotFoundError, TaskNotFoundError) as e:
        display_error(str(e))
    except Exception:
        display_error("An unexpected error occurred during task deletion.")


def project_task_menu(
    task_service: TaskService,
    project_service: ProjectService,
    project: Project,
) -> None:
    """The menu for managing tasks within a specific project."""
    while True:
        # Refresh project with latest tasks
        project.tasks = task_service.list_tasks(project.id)
        display_project_details_and_menu(project)
        choice = prompt_for_task_menu_choice()

        if choice == 1:
            handle_add_task(task_service, project_service, project.id)
        elif choice == 2:
            handle_list_tasks(task_service, project)
        elif choice == 3:
            handle_edit_task(task_service, project_service, project.id)
        elif choice == 4:
            handle_change_task_status(task_service, project_service, project.id)
        elif choice == 5:
            handle_delete_task(task_service, project_service, project.id)
        elif choice == 6:
            # Return to main menu
            return
        else:
            display_error("Invalid choice. Please enter a number from 1 to 6.")


def main_menu_loop(
    project_service: ProjectService, task_service: TaskService
) -> None:
    """The main application loop."""
    while True:
        display_main_menu()
        choice = prompt_for_main_choice()

        if choice == 1:
            handle_create_project(project_service)
        elif choice == 2:
            handle_list_projects(project_service)
        elif choice == 3:
            projects = project_service.list_projects()
            if not projects:
                display_error("No projects available to edit/view tasks.")
                continue

            handle_list_projects(project_service)
            project_id = prompt_for_project_id("manage (view/edit tasks)")
            if not isinstance(project_id, int):
                display_error("Invalid project ID. Please enter a project ID.")
            if project_id:
                try:
                    project = project_service.get_project(project_id)
                    project_task_menu(task_service, project_service, project)
                except ProjectNotFoundError:
                    display_error(f"Project with ID {project_id} not found.")
        elif choice == 4:
            handle_delete_project(project_service)
        elif choice == 5:
            display_exit_message()
            sys.exit(0)
        else:
            display_error("Invalid choice. Please enter a number from 1 to 5.")


if __name__ == "__main__":
    warnings.warn(
        "The CLI is deprecated and will be removed in a future version. "
        "Use the Web API instead: uvicorn src.api.app:app --reload",
        DeprecationWarning,
        stacklevel=2,
    )
    print("\n⚠️  WARNING: The CLI is deprecated. Use the Web API instead.\n")

    try:
        session_gen = get_session()
        session = next(session_gen)

        try:
            project_repo = ProjectRepository(session)
            task_repo = TaskRepository(session)
            project_service = ProjectService(project_repo)
            task_service = TaskService(task_repo)

            main_menu_loop(project_service, task_service)
        finally:
            session.close()
    except KeyboardInterrupt:
        display_exit_message()
        sys.exit(0)
