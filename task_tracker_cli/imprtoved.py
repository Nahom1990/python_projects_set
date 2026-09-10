from datetime import datetime,timezone
import json
import os
from typing import Optional

class Task:

    VALID_STATES={"pending","inprogress","done"}

    def __init__(self,task_id:int,
                 description:str,
                 status:str="pending",
                 created_at:Optional[str]=None,
                 updated_at:Optional[str]=None) -> None:

        self.task_id=task_id
        self.description=description
        self.status=status if status in self.VALID_STATES else "pending"
        self.created_at=created_at or self._current_timestamp()
        self.updated_at=updated_at


    @staticmethod
    def _current_timestamp():
        return datetime.now(timezone.utc).isoformat()

    def set_status(self,new_status):
        if new_status not in self.VALID_STATES:
            raise ValueError(f"statuses must be one of these {self.VALID_STATES}")

        if self.status == "pending" and new_status == "done":
            raise ValueError("Task must be marked 'inprogress' before being completed.")
        if self.status == "inprogress" and new_status == "pending":
            raise ValueError("Task in progress cannot revert to pending.")

        self.status=new_status
        self.updated_at=self._current_timestamp()

    def update_description(self,new_description):
        if self.status != "pending":
            raise ValueError("Only pending tasks can be edited.")
        self.description = new_description
        self.updated_at = self._current_timestamp()

    def to_dict(self):
        return {
                "id": self.task_id,
                "description": self.description,
                "status": self.status,
                "created_at": self.created_at,
                "updated_at": self.updated_at,
            }
    @classmethod
    def from_dict(cls,data):
        return cls(
            task_id=data["task_id"],
            description=data["description"],
            status=data.get("status", "pending"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )
    def __repr__(self) -> str:
        return f"Task(id={self.task_id}, description='{self.description}', status='{self.status}')"


class TaskManager:
    def __init__(self,file_path:str="tasks2.json") -> None:
        self.file_path=file_path
        self.tasks:dict[str,Task]={}
        self._load_from_file()

    def _load_from_file(self):
        if not os.path.exists(self.file_path):
            return
        try:
            with open(self.file_path,"r",encoding="utf-8") as file:
                raw=json.loads(file)
                for item in raw.values():
                    task=Task.from_dict(item)
                    self.tasks[task.task_id]=task