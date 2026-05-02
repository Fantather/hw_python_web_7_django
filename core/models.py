from datetime import date
from itertools import count
from django.db import models

counter = count(start=1)

# Create your models here.
class UserTask:
    _id:int
    title:str
    text:str
    start_date:date
    end_date:date

    def __init__(self, name:str, text:str, start_date:date, end_date:date) -> None:
        self._id = next(counter)
        self.title = name
        self.text = text
        self.start_date = start_date
        self.end_date = end_date

    @property
    def id(self) -> int:
        return self._id


class TaskRepository:
    _tasks:dict[int, UserTask]

    def __init__(self) -> None:
        self._tasks = {}

    @property
    def tasks(self) -> dict[int, UserTask]:
        return self._tasks.copy()
    
    def add(self, task:UserTask) -> None:
        self._tasks[task.id] = task

    def delete_by_id(self, task_id:int) -> bool:
        removed_task = self._tasks.pop(task_id, None)
        return removed_task is not None
    

task_repo = TaskRepository()