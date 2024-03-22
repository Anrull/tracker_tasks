import ast
from peewee import *
import datetime

db = SqliteDatabase('db/tasks.db')
json_dict = {"info": "", "tasks": {}, "other": {}}


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
    count = Tasks.select()
    count = max([int(i.id_task) for i in count]) + 1
    Tasks.create(id_task=count,
                 owner_name=owner_name,
                 owner_id=message.from_user.id,
                 users_ids=f"[{message.from_user.id}]")
    return count


async def add_tasks(message, id_task, tasks):
    tsk = Tasks.get(id_task=int(id_task))
    if message.chat.id in ast.literal_eval(tsk.users_ids):
        dct = ast.literal_eval(tsk.tasks)
        list_tasks = dct["tasks"]
        if list_tasks.keys():
            len_tasks = max([i for i in list_tasks.keys()]) + 1
        else:
            len_tasks = 1
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


async def delete_tasks(message, id_task, delete_task_ids):
    tsk = Tasks.get(id_task=int(id_task))
    if message.chat.id in ast.literal_eval(tsk.users_ids):
        dct = ast.literal_eval(tsk.tasks)
        for i in delete_task_ids:
            del dct["tasks"][i]
        tsk.tasks = dct
        tsk.save()
        return
    raise ValueError("Нет доступа")


async def add_description(message, id_task, text):
    tsk = Tasks.get(id_task=int(id_task))
    if message.chat.id in ast.literal_eval(tsk.users_ids):
        dct = ast.literal_eval(tsk.tasks)
        dct["info"] = text
        tsk.tasks = dct
        tsk.save()
        return
    raise ValueError("Нет доступа")


async def get_books(message):
    notebooks = Tasks.select()
    my_notebooks = []
    ids_notebooks = []
    for notebook in notebooks:
        if message.chat.id in ast.literal_eval(notebook.users_ids):
            my_notebooks.append(notebook)
            ids_notebooks.append(notebook.id_task)
    return {"all": my_notebooks, "ids": ids_notebooks}
