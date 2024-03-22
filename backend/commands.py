from aiogram import Router, types, html
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

        list_tasks = []
        text = f"✍️ <b><em>Задачи в кейсе {id_task}:</em></b>\n\n{html.quote(result['info'])}\n\n"
        for i in result["tasks"].keys():
            if len(text) > 3076:
                list_tasks.append(text)
                text = ""
            text = text + f"<b>Задача {i}</b>\n♦️ <em>{result['tasks'][i]}</em>\n\n"
        list_tasks.append(text)

        for elem in list_tasks:
            await message.answer(elem, parse_mode=ParseMode.HTML)
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
async def add_tasks(message: types.Message, add=False):
    if not add:
        text = message.text[5:]
    else:
        text = message.text
    delimetr = await user.get_delimetr(message)
    tasks = text.split(delimetr)
    await temp.add_message(message, tasks)
    # id_task = await temp.get_mode(message)
    text = "✍️ <b><em>Добавленные задачи:</em></b>\n\n"
    # answer = await db_tasks.add_tasks(message, id_task, tasks)
    # if answer == "Задачи добавленны":
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
    list_msg = []
    for task in answer_tasks[:-1]:
        msg = await message.answer(task, parse_mode=ParseMode.HTML)
        list_msg.append(msg.message_id)
    msg = await message.answer(answer_tasks[-1],
                               parse_mode=ParseMode.HTML,
                               reply_markup=callbacks.builder_yes_no_keyboard_add_tasks)
    list_msg.append(msg.message_id)
    await temp.add_ids(message, *list_msg)
    # else:
    #     await message.answer(answer)


@router.message(Command("delete"))
async def delete(message: types.Message):
    id_task = await temp.get_mode(message)
    result = await db_tasks.get_tasks(message, id_task)
    count = result["tasks"].keys()
    builder = await callbacks.delete_builder(count)
    await temp.get_ids_tasks_delete(message, delete=True)
    msg = await message.answer("<b><em>Выберите номер задачи / задач</em></b>",
                               reply_markup=builder, parse_mode=ParseMode.HTML)
    dict_message = {'message_id': msg.message_id}
    await temp.add_message(message, f"{dict_message}")
    await temp.add_ids(message, msg.message_id)


@router.message(Command("description"))
async def description(message: types.Message):
    await temp.add_status(message, "add_description")
    msg = await message.answer("Введите описание", reply_markup=callbacks.builder_back_keyboard)
    await temp.add_ids(message, msg.message_id)


@router.message(Command("choice"))
async def choice_book(message: types.Message):
    info_dict = await db_tasks.get_books(message)
    await message.answer("Выберите нужный блокнот:", reply_markup=await callbacks.choice_builder(info_dict["ids"]))

