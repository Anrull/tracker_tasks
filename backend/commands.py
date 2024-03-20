from aiogram import Router, types
from aiogram.enums import ParseMode
from aiogram.filters import Command

import callbacks.callbacks as callbacks
import db.temp_db as temp
import db.user as user
import db.tasks as db_tasks
import backend.other as other

router = Router()


@router.message(Command("delimetr"))
async def delimetr(message: types.Message):
    msg = await message.answer(
        f"Выберите разделитель (нужен для того, чтоб можно было задавать несколько задач в одном сообщении)",
        reply_markup=callbacks.builder_delimetr
    )
    await temp.add_ids(message, msg.message_id)


@router.message(Command("get"))
async def get_my_tasks(message: types.Message):
    id_task = await temp.get_mode(message)
    try:
        result = await db_tasks.get_tasks(message, id_task)
        text = f"✍️ <b><em>Задачи в кейсе {id_task}:</em></b>\n\n"
        for i in result["tasks"].keys():
            text = text + f"<b>Задача {i}</b>\n♦️ <em>{result['tasks'][i]}</em>\n\n"

        await message.answer(text, parse_mode=ParseMode.HTML)
    except ValueError:
        await message.answer("Вы не имеете доступа к файлу")
    except Exception as e:
        print(e)
        await message.answer("Задачи добавлены")


@router.message(Command("create"))
async def create(message: types.Message):
    msg = await message.answer("Обработка...")
    try:
        name = await user.get_name(message)
        count = await db_tasks.create_tasks(message, name)
        await temp.add_mode(message, count)
        await msg.edit_text("Создание успешно!")
    except:
        await msg.edit_text("Ошибка создания файла")


@router.message(Command("add"))
async def add_tasks(message: types.Message):
    text = message.text[5:]
    delimetr = await user.get_delimetr(message)
    tasks = text.split(delimetr)
    id_task = await temp.get_mode(message)
    text = "✍️ <b><em>Добавленные задачи:</em></b>\n\n"
    if len(tasks) > 1:
        answer = await db_tasks.add_tasks(message, id_task, tasks)
    else:
        answer = await db_tasks.add_tasks(message, id_task, tasks)
    if answer == "Задачи добавленны":
        count_added_tasks = 1
        answer_tasks = []
        for task in tasks:
            if len(answer_tasks) > 3076:
                answer_tasks.append(text)
                text = ""
            if task[:1] == " ":
                task = task[1:]
            text = text + f"<b>Задача {count_added_tasks}</b>\n🔹 <em>" + task + "</em>\n\n"
            count_added_tasks += 1
        answer_tasks.append(text)
        for task in answer_tasks:
            await message.answer(task, parse_mode=ParseMode.HTML)
    else:
        await message.answer(answer)


@router.message(Command("delete"))
async def delete(message: types.Message):
    id_task = await temp.get_mode(message)
    result = await db_tasks.get_tasks(message, id_task)
    count = result["tasks"].keys()
    msg = await message.answer("Выберите номер задачи / задач", reply_markup=await callbacks.delete_builder(count))
    dict_message = {'message_id': msg.message_id}
    await temp.add_message(message, f"{dict_message}")
    await temp.add_ids(message, msg.message_id)
