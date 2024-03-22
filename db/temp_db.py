from peewee import *
import ast

db = SqliteDatabase('db/temp.db')


class Temp(Model):
    user_id = IntegerField()
    last_message = TextField()
    mode = TextField()
    column1 = TextField(default="")     # id сообщений
    column2 = TextField(default="")     # id для удаления задач
    column3 = TextField(default="")     # ожидание действия
    column4 = TextField(default="")

    class Meta:
        database = db


db.create_tables([Temp])


async def create_new_user(message):
    try:
        Temp.get(user_id=message.from_user.id)
    except:
        Temp.create(user_id=message.from_user.id, last_message=message, mode="")


async def add_message(message, msg):
    try:
        temp = Temp.get(Temp.user_id == message.chat.id)
        temp.last_message = msg
        temp.save()
    except:
        Temp.create(user_id=message.from_user.id, last_message=f"{msg}",
                    mode="")


async def get_message(message):
    return Temp.get(Temp.user_id == message.chat.id).last_message


async def add_mode(message, text_json):
    temp = Temp.get(Temp.user_id == message.from_user.id)
    temp.mode = text_json
    temp.save()


async def get_mode(message):
    return Temp.get(Temp.user_id == message.chat.id).mode


async def get_last_ids(message):
    user = Temp.get(Temp.user_id == message.chat.id)
    return ast.literal_eval(user.column1)


async def add_ids(message, *ids):
    user = Temp.get(Temp.user_id == message.chat.id)
    user.column1 = f"{ids}"
    user.save()


async def add_ids_tasks_delete(message, id_task):
    temp = Temp.get(Temp.user_id == message.chat.id)
    lst = temp.column2
    if lst == "":
        temp.column2 = f"[{id_task}]"
    else:
        lst = ast.literal_eval(lst)
        lst.append(id_task)
        temp.column2 = lst
    temp.save()


async def delete_ids_tasks_delete(message, id_task):
    temp = Temp.get(Temp.user_id == message.chat.id)
    lst = ast.literal_eval(temp.column2)
    index = lst.index(id_task)
    lst.pop(index)
    temp.column2 = lst
    temp.save()


async def get_ids_tasks_delete(message, delete=False):
    if not delete:
        lst = Temp.get(Temp.user_id == message.chat.id).column2
        return ast.literal_eval(lst) if lst != "" else []
    temp = Temp.get(Temp.user_id == message.chat.id)
    lst = temp.column2
    temp.column2 = ""
    temp.save()
    if lst != "":
        return ast.literal_eval(lst)
    return []


async def add_status(message, status):  # column3
    temp = Temp.get(Temp.user_id == message.chat.id)
    temp.column3 = f"{status}"
    temp.save()


async def get_status(message):  # column3
    return Temp.get(Temp.user_id == message.chat.id).column3


async def delete_status(message):   # column3
    temp = Temp.get(Temp.user_id == message.chat.id)
    temp.column3 = ""
    temp.save()
