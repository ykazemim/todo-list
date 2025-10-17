# ToDo List CLI

A command-line interface application for managing projects and their associated tasks. This tool allows users to create, view, edit, and delete projects and tasks with validation checks.

## Features

* **Project Management:** Create, list, edit, and delete projects.
* **Task Management:** Add, list, edit, change status, and delete tasks within a project.
* **Data Validation:** Ensures data integrity for project and task names, descriptions, statuses, and deadlines.
* **In-Memory Storage:** Uses a simple in-memory repository for application data storage.
* **Concurrency Limits:** Respects limits for the maximum number of projects and tasks (configured via environment variables).

## Getting Started

### Prerequisites

* Python 3.13+

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/ykazemim/todo-list.git
    cd todo-list
    ```

2.  **Install dependencies:**
    The project uses `poetry` for dependency management.

    ```bash
    pip install poetry
    poetry install
    ```
    
    *Alternatively, if you are not using `poetry`, you can install dependencies manually:*
    ```bash
    pip install python-dotenv
    ```

3.  **Set up Environment Variables (Optional):**
    The application reads configuration from a `.env` file (via `python-dotenv`). You can create a file named `.env` in the root directory to customize limits (or just rename .env.example to .env):

    ```
    # .env example
    MAX_NUMBER_OF_PROJECT=10
    MAX_NUMBER_OF_TASK=50
    ```
    If not specified, defaults are used (10 projects, 50 tasks - though task limits default to 200 in the `memory_repository.py` if the environment variable isn't set).

### Usage

Run the main application file:

```bash
poetry run python -m src.main
# OR
python src/main.py
```  

## Contributing

Contributions are welcome and highly appreciated! Whether it's reporting a bug, suggesting a new feature, or submitting a pull request, your input helps make this project better.  

## License

This project is licensed under the MIT License. See the **[LICENSE](LICENSE)** file for more details.