from datetime import datetime, timezone
import json
import os
from typing import Dict, List, Optional


class Task:
    VALID_STATUSES = {"pending", "inprogress", "done"}

    def __init__(
        self,
        description: str,
        task_id: int,
        status: str = "pending",
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
    ) -> None:
        self.id = task_id
        self.description = description
        self.status = status if status in self.VALID_STATUSES else "pending"
        self.created_at = created_at or self._current_timestamp()
        self.updated_at = updated_at

    @staticmethod
    def _current_timestamp() -> str:
        return datetime.now(timezone.utc).isoformat()

    def set_status(self, new_status: str) -> None:
        if new_status not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status: '{new_status}'")
        
        # Enforce status state transitions
        if self.status == "pending" and new_status == "done":
            raise ValueError("Task must be marked 'inprogress' before being completed.")
        if self.status == "inprogress" and new_status == "pending":
            raise ValueError("Task in progress cannot revert to pending.")

        self.status = new_status
        self.updated_at = self._current_timestamp()

    def update_description(self, new_description: str) -> None:
        if self.status != "pending":
            raise ValueError("Only pending tasks can be edited.")
        self.description = new_description
        self.updated_at = self._current_timestamp()

    def to_dict(self) -> dict:
        """Serializes the Task object into a plain dictionary."""
        return {
            "id": self.id,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """Factory method to construct a Task object from a dictionary."""
        return cls(
            task_id=data["id"],
            description=data["description"],
            status=data.get("status", "pending"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )

    def __repr__(self) -> str:
        return f"Task(id={self.id}, description='{self.description}', status='{self.status}')"


class TaskManager:
    def __init__(self, file_path: str = "tasks.json") -> None:
        self.file_path = file_path
        self.tasks: Dict[int, Task] = {}
        self._load_from_file()

    def _next_id(self) -> int:
        """Calculates the next available integer ID."""
        return max(self.tasks.keys(), default=0) + 1

    def _load_from_file(self) -> None:
        """Loads persistent JSON data into memory on initialization."""
        if not os.path.exists(self.file_path):
            return

        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                raw_data = json.load(file)
                for item in raw_data.values():
                    task = Task.from_dict(item)
                    self.tasks[task.id] = task
        except (json.JSONDecodeError, KeyError):
            self.tasks = {}

    def _save_to_file(self) -> None:
        """Flushes the current in-memory task dictionary to JSON disk storage."""
        data = {str(task_id): task.to_dict() for task_id, task in self.tasks.items()}
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def add_task(self, description: str) -> Task:
        """Creates and registers a new task with an auto-generated ID."""
        task_id = self._next_id()
        task = Task(description=description, task_id=task_id)
        self.tasks[task_id] = task
        self._save_to_file()
        return task

    def update_task(self, update_id: int | str, new_description: str) -> Task:
        task_id = int(update_id)
        if task_id not in self.tasks:
            raise KeyError(f"Task with ID {task_id} not found.")

        task = self.tasks[task_id]
        task.update_description(new_description)
        self._save_to_file()
        return task

    def mark_task(self, task_id: int | str, new_status: str) -> Task:
        int_id = int(task_id)
        if int_id not in self.tasks:
            raise KeyError(f"Task with ID {int_id} not found.")

        task = self.tasks[int_id]
        task.set_status(new_status)
        self._save_to_file()
        return task

    def list_tasks(self, status_filter: Optional[str] = None) -> List[Task]:
        """Returns all tasks or tasks matching a specific status."""
        if status_filter:
            return [t for t in self.tasks.values() if t.status == status_filter]
        return list(self.tasks.values())




