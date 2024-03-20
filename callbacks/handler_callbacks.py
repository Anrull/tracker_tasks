import ast

from aiogram import Router, F, types, Bot
from aiogram.enums import ParseMode

import callbacks.callbacks as callbacks
import db.user as user
import db.temp_db as temp_db
import db.tasks as db_tasks
import backend.other as other
import config

router = Router()
bot = Bot(token=config.TOKEN)


@router.callback_query(callbacks.CallbacksDelimetr.filter(F.foo == "delimetr"))
async def choice_bot(query: types.CallbackQuery, callback_data: callbacks.CallbacksDelimetr):
    await other.delete_messages(query)
    try:
        await user.add_delimetr(query.message, callback_data.delimetr)
        await query.answer("Разделитель добавлен")
    except:
        await query.answer("Нет связи с БД... Попробуйте снова или обратитесь к @Anrull")
        await query.ans


@router.callback_query(callbacks.CallbacksDelete.filter(F.foo == "delete_tasks"))
async def delete_tasks(query: types.CallbackQuery, callback_data: callbacks.CallbacksDelete):
    match callback_data.id_task:
        case -1:
            await other.delete_messages(query)
        case -2:
            pass
        case _:
            try:
                # last_id = await temp_db.get_last_ids(query.message)
                lst_id_tasks = await temp_db.get_ids_tasks_delete(query.message)
                if callback_data.id_task not in lst_id_tasks:
                    await temp_db.add_ids_tasks_delete(query.message, callback_data.id_task)
                else:
                    await temp_db.delete_ids_tasks_delete(query.message, callback_data.id_task)
                msg: types.Message = ast.literal_eval(await temp_db.get_message(query.message))
                lst_id_tasks = await temp_db.get_ids_tasks_delete(query.message)
                print(lst_id_tasks)
                text = "Выберите номер задачи / задач\n\nВыбранные задачи: {}".format(
                    ", ".join(list(map(str, lst_id_tasks))))
                print(5)
                # await query.message.answer(text)
                print(msg)
                id_task = await temp_db.get_mode(query.message)
                result = await db_tasks.get_tasks(query.message, id_task)
                count = result["tasks"].keys()
                await bot.edit_message_text(chat_id=query.message.chat.id,
                                            message_id=msg["message_id"],
                                            text=text,
                                            parse_mode=ParseMode.HTML,
                                            reply_markup=await callbacks.delete_builder(count))
                # await msg.edit_text(text)
            except Exception as e:
                print(e)
                print("Error: callbacks delete_tasks (module handler_callbacks.py)")
            await query.answer()
