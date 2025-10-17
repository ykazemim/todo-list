from datetime import datetime, date
from typing import Literal, Optional

from src.exceptions.todo_exceptions import ValidationError
from src.models.task import Task

StatusType = Literal["todo", "doing", "done"]
MAX_TASK_TITLE = 30
MAX_TASK_DESC = 150
VALID_STATUSES: list[StatusType] = ["todo", "doing", "done"]

class InMemoryRepository:
    # ... existing Project methods ...

    # ---------- Task CRUD ----------

    def add_task(
        self,
        project_id: int,
        title: str,
        description: str,
        status: StatusType = "todo",
        deadline: Optional[str] = None,
    ) -> Task:
        """
        Add a task to a project.
        """
        project = self.projects.get(project_id)
        if project is None:
            raise ValidationError("Project not found.")

        if len(project.tasks) >= int(os.getenv("MAX_NUMBER_OF_TASK", 200)):
            raise ValidationError("Maximum number of tasks reached for this project.")

        if len(title) > MAX_TASK_TITLE:
            raise ValidationError(f"Task title must be ≤ {MAX_TASK_TITLE} characters.")

        if len(description) > MAX_TASK_DESC:
            raise ValidationError(f"Task description must be ≤ {MAX_TASK_DESC} characters.")

        if status not in VALID_STATUSES:
            raise ValidationError(f"Invalid status: {status}")

        task_deadline: Optional[date] = None
        if deadline:
            try:
                task_deadline = datetime.strptime(deadline, "%Y-%m-%d").date()
            except ValueError:
                raise ValidationError("Deadline must be in YYYY-MM-DD format.")

        task = Task(
            id=self.next_task_id,
            title=title,
            description=description,
            status=status,
            deadline=task_deadline,
        )
        self.next_task_id += 1
        project.tasks.append(task)
        return task

    def edit_task(
        self,
        project_id: int,
        task_id: int,
        title: str,
        description: str,
        status: StatusType,
        deadline: Optional[str] = None,
    ) -> Task:
        """
        Edit a task's details.
        """
        project = self.projects.get(project_id)
        if not project:
            raise ValidationError("Project not found.")

        task = next((t for t in project.tasks if t.id == task_id), None)
        if not task:
            raise ValidationError("Task not found.")

        if len(title) > MAX_TASK_TITLE:
            raise ValidationError(f"Task title must be ≤ {MAX_TASK_TITLE} characters.")
        if len(description) > MAX_TASK_DESC:
            raise ValidationError(f"Task description must be ≤ {MAX_TASK_DESC} characters.")
        if status not in VALID_STATUSES:
            raise ValidationError(f"Invalid status: {status}")

        task_deadline: Optional[date] = None
        if deadline:
            try:
                task_deadline = datetime.strptime(deadline, "%Y-%m-%d").date()
            except ValueError:
                raise ValidationError("Deadline must be in YYYY-MM-DD format.")

        task.title = title
        task.description = description
        task.status = status
        task.deadline = task_deadline
        return task

    def delete_task(self, project_id: int, task_id: int) -> None:
        """
        Delete a task by ID within a project.
        """
        project = self.projects.get(project_id)
        if not project:
            raise ValidationError("Project not found.")

        task = next((t for t in project.tasks if t.id == task_id), None)
        if not task:
            raise ValidationError("Task not found.")

        project.tasks.remove(task)

    def change_task_status(self, project_id: int, task_id: int, status: StatusType) -> Task:
        """
        Change only the status of a task.
        """
        project = self.projects.get(project_id)
        if not project:
            raise ValidationError("Project not found.")

        task = next((t for t in project.tasks if t.id == task_id), None)
        if not task:
            raise ValidationError("Task not found.")

        if status not in VALID_STATUSES:
            raise ValidationError(f"Invalid status: {status}")

        task.status = status
        return task
