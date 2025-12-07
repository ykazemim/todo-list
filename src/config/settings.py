"""Application configuration settings."""

import os
from dotenv import load_dotenv

load_dotenv()

# Database Configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"postgresql://{os.getenv('POSTGRES_USER', 'todolist')}:"
    f"{os.getenv('POSTGRES_PASSWORD', 'todolist')}@"
    f"{os.getenv('POSTGRES_HOST', 'localhost')}:"
    f"{os.getenv('POSTGRES_PORT', '5432')}/"
    f"{os.getenv('POSTGRES_DB', 'todolist')}",
)

# Application Limits
MAX_NUMBER_OF_PROJECTS = int(os.getenv("MAX_NUMBER_OF_PROJECTS", 10))
MAX_NUMBER_OF_TASKS_PER_PROJECT = int(os.getenv("MAX_NUMBER_OF_TASKS_PER_PROJECT", 50))

MAX_PROJECT_NAME_CHARS = int(os.getenv("MAX_PROJECT_NAME_CHARS", 30))
MAX_PROJECT_DESCRIPTION_CHARS = int(os.getenv("MAX_PROJECT_DESCRIPTION_CHARS", 150))
MAX_TASK_TITLE_CHARS = int(os.getenv("MAX_TASK_TITLE_CHARS", 30))
MAX_TASK_DESCRIPTION_CHARS = int(os.getenv("MAX_TASK_DESCRIPTION_CHARS", 150))
