from aiogram import Router, F, types, Bot
from aiogram.enums import ParseMode

import callbacks.callbacks as callbacks
import db.user as user
import db.temp_db as temp_db
import db.tasks as db_tasks
import backend.other as other
import backend.commands as commands
import config
import ast

router = Router()
bot = Bot(token=config.TOKEN)


@router.callback_query(callbacks.CallbacksDelimetr.filter(F.foo == "delimetr"))
async def choice_bot(query: types.CallbackQuery, callback_data: callbacks.CallbacksDelimetr):
    await other.delete_messages(query=query)
    try:
        await user.add_delimetr(query.message, callback_data.delimetr)
        await query.answer("Разделитель добавлен")
    except:
        await query.answer("Нет связи с БД... Попробуйте снова или обратитесь к @Anrull")


@router.callback_query(callbacks.CallbacksDelete.filter(F.foo == "delete_tasks"))
async def delete_tasks(query: types.CallbackQuery, callback_data: callbacks.CallbacksDelete):
    match callback_data.id_task:
        case -1:
            await other.delete_messages(query=query)
        case -2:
            lst_id_tasks = await temp_db.get_ids_tasks_delete(query.message)
            id_task = await temp_db.get_mode(query.message)
            await db_tasks.delete_tasks(query.message, int(id_task), lst_id_tasks)
            await temp_db.get_ids_tasks_delete(query.message, delete=True)
            msg = ast.literal_eval(await temp_db.get_message(query.message))
            text = "Удаленные сообщения: <em><b>{}</b></em>".format(", ".join(list(map(str, lst_id_tasks))))
            await bot.edit_message_text(chat_id=query.message.chat.id,
                                        message_id=msg["message_id"],
                                        text=text,
                                        parse_mode=ParseMode.HTML)
        case _:
            try:
                lst_id_tasks = await temp_db.get_ids_tasks_delete(query.message)
                if callback_data.id_task not in lst_id_tasks:
                    await temp_db.add_ids_tasks_delete(query.message, callback_data.id_task)
                else:
                    await temp_db.delete_ids_tasks_delete(query.message, callback_data.id_task)
                msg = ast.literal_eval(await temp_db.get_message(query.message))
                lst_id_tasks = await temp_db.get_ids_tasks_delete(query.message)
                text = "<b><em>Выберите номер задачи / задач</em></b>\n\nВыбранные задачи: <em>{}</em>".format(
                    ", ".join(list(map(str, lst_id_tasks))))
                await bot.edit_message_text(inline_message_id=query.inline_message_id,
                                            chat_id=query.message.chat.id,
                                            message_id=msg["message_id"],
                                            text=text,
                                            parse_mode=ParseMode.HTML,
                                            reply_markup=query.message.reply_markup)
            except Exception as e:
                print(e)
                print("Error: callbacks delete_tasks (module handler_callbacks.py)")
    await query.answer()


@router.callback_query(callbacks.MenuCallbaks.filter(F.foo == "menu"))
async def menu_callbaks(query: types.CallbackQuery, callback_data: callbacks.MenuCallbaks):
    await other.delete_messages(query)
    match callback_data.command:
        case "Да-add_to_description":
            text = await temp_db.get_message(query.message)
            id_task = await temp_db.get_mode(query.message)
            try:
                await db_tasks.add_description(query.message, id_task, text)
                await temp_db.delete_status(query.message)
                await query.message.answer("Описание добавлено")
            except:
                await query.message.answer("У вас нет доступа к этому файлу")
        case "Нет-add_to_description":
            await query.message.answer("Описание не было добавлено")
            await temp_db.delete_status(query.message)
        case "Добавить-add_tasks":
            id_task = await temp_db.get_mode(query.message)
            tasks = ast.literal_eval(await temp_db.get_message(query.message))
            answer = await db_tasks.add_tasks(query.message, id_task, tasks)
            await query.message.answer(answer)
            await temp_db.delete_status(query.message)
        case "Отмена-add_tasks":
            await query.message.answer("Задачи не были добавленны")
            await temp_db.delete_status(query.message)
        case "Отмена":
            await temp_db.delete_status(query.message)
        case _:
            await query.message.answer("Текущий функционал", reply_markup=callbacks.builder_menu_main)
    await query.answer()


@router.callback_query(callbacks.MenuCallbaks.filter(F.foo == "main_menu"))
async def menu_callbaks(query: types.CallbackQuery, callback_data: callbacks.MenuCallbaks):
    match callback_data.command:
        case "Добавить задачу":
            await temp_db.add_status(query.message, "add_tasks")
            msg = await query.message.answer("Введите текст задачи", reply_markup=callbacks.builder_back_keyboard)
            await temp_db.add_ids(query.message, msg.message_id)
        case "Удалить задачи":
            await commands.delete(query.message)
        case "Просмотреть задачи":
            await commands.get_my_tasks(query.message)
        case "Создать блокнот":
            await commands.create(query.message)
        case "Добавить описание":
            await commands.description(query.message)
        case "Изменить разделитель":
            await commands.delimetr(query.message)
    await query.answer()
