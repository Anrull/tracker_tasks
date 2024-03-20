import ast
from pprint import pprint

from peewee import *
import datetime

db = SqliteDatabase('db/tasks.db')
json_dict = {"tasks": {}, "other": {}}


class Tasks(Model):
    id_task = IntegerField()
    owner_name = TextField()
    owner_id = IntegerField()
    users_names = TextField(default="[]")
    users_ids = TextField()
    create_data = DateTimeField(default=datetime.datetime.now())
    tasks = TextField(default=f"{json_dict}")
    column1 = TextField(default="")
    column2 = TextField(default="")
    column3 = TextField(default="")

    class Meta:
        database = db


# db.create_tables([Tasks])


async def create_tasks(message, owner_name):
    count = Tasks.select().count() + 1
    Tasks.create(id_task=count,
                 owner_name=owner_name,
                 owner_id=message.from_user.id,
                 users_ids=f"[{message.from_user.id}]")
    return count


async def add_tasks(message, id_task, tasks):
    print(tasks)
    tsk = Tasks.get(id_task=int(id_task))
    if message.chat.id in ast.literal_eval(tsk.users_ids):
        dct = ast.literal_eval(tsk.tasks)
        list_tasks = dct["tasks"]
        len_tasks = len(list_tasks) + 1
        for task in tasks:
            if task[:1] == " ":
                task = task[1:]
            list_tasks[len_tasks] = task.capitalize()
            len_tasks += 1
        dct["tasks"] = list_tasks
        tsk.tasks = dct
        tsk.save()
        return "Задачи добавленны"
    return "Вы не имеете доступ к этим задачам"


async def get_tasks(message, id_task):
    tsk = Tasks.get(id_task=int(id_task))
    if message.chat.id in ast.literal_eval(tsk.users_ids):
        return ast.literal_eval(tsk.tasks)
    raise ValueError("Нет доступа")


async def delete_tasks(message, id_task, delete_task_id):
    tsk = Tasks.get(id_task=int(id_task))
    if message.chat.id in ast.literal_eval(tsk.users_ids):
        dct = ast.literal_eval(tsk.tasks)
        del dct["tasks"][delete_task_id]
        return
    raise ValueError("Нет доступа")
