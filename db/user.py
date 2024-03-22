from peewee import *


db = SqliteDatabase('db/user.db')


class User(Model):
    user_id = IntegerField()
    chat_id = IntegerField()
    name = TextField()
    username = TextField()
    jsons = TextField()
    delimetr = TextField(default="*")

    class Meta:
        database = db


# db.create_tables([User])


async def create_user(message):
    try:
        User.get(user_id=message.from_user.id)
    except:
        User.create(user_id=message.from_user.id, chat_id=message.chat.id,
                    name=message.from_user.first_name, username=message.from_user.username, jsons="")


async def add_delimetr(message, delimetr):
    user = User.get(chat_id=message.chat.id)
    user.delimetr = f"{delimetr}"
    user.save()


async def get_name(message):
    user = User.get(user_id=message.chat.id)
    return user.name


async def get_delimetr(message):
    return User.get(user_id=message.chat.id).delimetr
