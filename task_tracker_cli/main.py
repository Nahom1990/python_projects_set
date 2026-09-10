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


class TaskManager:
    def __init__(self) -> None:
        self.tasks:list[Task]=[]
        self.file_path="tasks.json"

    def add_task(self, task:Task):
        
        self.tasks.append(task)
        if os.path.exists(self.file_path):
            with open(file=self.file_path,mode="r") as json_file:
                try:
                    data=json.load(json_file)
                    if not isinstance(data,list):
                        data=[data]
                except json.JSONDecodeError:
                    data=[]

        else:
            data=[]

        data.append(task.__dict__)

        with open(self.file_path,"w") as file:
            json.dump(data,file,indent=4)

        return True

    def update_task(self,id,new_description):
        if os.path.exists(self.file_path):
            with open(file=self.file_path,mode="r") as file:
                try:
                    data=json.load(file)
                    if not isinstance(data,list):
                        data=[data]
                except json.JSONDecodeError:
                    data=[]
        else:
            raise ValueError("no file in the given item")
        


        for task in self.tasks:
            if task.id==id:
                if not task.get_status()=="pending":
                    raise ValueError("tasks in progress or done cant be updated")

                task.updated_at=time.time()
                task.description=new_description
                return True
        return False
            

    def mark_task(self,id,new_status):
        for task in self.tasks:
            if task.id==id:
                task.set_status(new_status)
                return new_status
        return False
    
    def list_all_tasks(self)->list[Task]:
        return self.tasks

    def list_done_tasks(self)->list[Task]:
        done_tasks=[]
        for task in self.tasks:
            if task.get_status()=="done":
                done_tasks.append(task)

        return done_tasks

    def list_all_not_done_tasks(self)->list[Task]:
        not_done_tasks=[]
        for task in self.tasks:
            if not task.get_status()=="done":
                not_done_tasks.append(task)

        return not_done_tasks

    def list_progress_tasks(self)->list[Task]:
        progress_tasks=[]
        for task in self.tasks:
            if task.get_status()=="inprogress":
                progress_tasks.append(task)

        return progress_tasks


task1=Task("first_task")
task2=Task("second_task")

manager=TaskManager()

manager.add_task(task1)
manager.add_task(task2)