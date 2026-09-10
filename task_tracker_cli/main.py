import time
import json
import os

class Task:
    _initial=0
    def __init__(self,description) -> None:
        self.id=Task._initial
        self.description=description
        self._status="pending"
        self.created_at=time.time()
        self.updated_at=None
        Task._initial+=1

    def set_status(self,status):
        self._status=status

    def get_status(self):
        return self._status

    def __repr__(self) -> str:
        return f"id:{self.id}, description:{self.description}, status:{self._status}"


class TaskManager:
    def __init__(self) -> None:
        self.tasks:dict[int,Task]={}
        self.file_path="tasks.json"

    def read_json(self):
        if os.path.exists(self.file_path):
            with open(self.file_path,"r") as file:
                try:
                    data=json.load(file)
                    return data
                except json.JSONDecodeError:
                    return {}
        return {}


    def add_task(self, task:Task):
        task_id=task.id
        self.tasks[task_id]=task
        
        data=self.read_json()

        data[str(task_id)]=task.__dict__

        with open(self.file_path,"w") as file:
            json.dump(data,file,indent=4)

        return True

    def update_task(self,update_id,new_description):
        
        update_id=int(update_id)

        if update_id not in self.tasks:
            raise KeyError(f"Task with ID {update_id} not found.")

        task = self.tasks[update_id]
        if task.get_status()!="pending":
            raise ValueError("tasks in progress or done cant be updated")

        task.updated_at=time.time()
        task.description=new_description

        data=self.read_json()

        data[str(update_id)]=task.__dict__ #why isnt this replacing the initial ater update?

        with open(file=self.file_path,mode="w") as file:
            data=json.dump(data,file,indent=4)
        return False
            

    def mark_task(self,id,new_status):
        data=self.read_json()

        task=self.tasks[id]
        if task.get_status() == "pending":
            if new_status=="done":
                raise ValueError("must be in progress before being done")
            elif new_status=="inprogress":
                task.set_status(new_status)
        elif task.get_status() =="inprogress":
            if new_status=="done":
                task.set_status(new_status)
            elif new_status=="pending":
                raise ValueError("inprogress cant go back to pending")

        data[str(id)]=task.__dict__
        with open(file=self.file_path,mode="w") as file:
            data=json.dump(data,file,indent=4)
        

    
    def list_all_tasks(self)->dict[int,Task]:
        return self.tasks

    # def list_done_tasks(self)->list[Task]:
    #     done_tasks=[]
    #     for task in self.tasks:
    #         if task.get_status()=="done":
    #             done_tasks.append(task)

    #     return done_tasks

    # def list_all_not_done_tasks(self)->list[Task]:
    #     not_done_tasks=[]
    #     for task in self.tasks:
    #         if not task.get_status()=="done":
    #             not_done_tasks.append(task)

    #     return not_done_tasks

    # def list_progress_tasks(self)->list[Task]:
    #     progress_tasks=[]
    #     for task in self.tasks:
    #         if task.get_status()=="inprogress":
    #             progress_tasks.append(task)

    #     return progress_tasks


task1=Task("first_task")
task2=Task("second_task")

manager=TaskManager()

manager.add_task(task1)
manager.add_task(task2)
manager.update_task("1","this is the new description")
manager.mark_task(1,"inprogress")
print(manager.list_all_tasks())