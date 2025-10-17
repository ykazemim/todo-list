from typing import Dict, List, Optional
from src.models.project import Project
from src.models.task import Task

class InMemoryRepository:
    """
    Stores Projects and Tasks in memory.
    """

    def __init__(self) -> None:
        self.projects: Dict[int, Project] = {}
        self.next_project_id: int = 1
        self.next_task_id: int = 1

    def add_project(self, project: Project) -> Project:
        project.id = self.next_project_id
        self.next_project_id += 1
        self.projects[project.id] = project
        return project

    def get_project(self, project_id: int) -> Optional[Project]:
        return self.projects.get(project_id)

    def list_projects(self) -> List[Project]:
        return list(self.projects.values())

    # Task handling will be added later
