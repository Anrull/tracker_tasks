from aiogram import Bot, Router, types
from aiogram.enums import ParseMode

import backend.commands as commands
import config
import db.temp_db as temp
import callbacks.callbacks as callbacks


bot = Bot(token=config.TOKEN)
router = Router()


async def delete_messages(query, message=False):
    try:
        if not message:
            last_ids = await temp.get_last_ids(query.message)
            for msg_id in last_ids:
                await bot.delete_message(
                    chat_id=query.message.chat.id,
                    message_id=msg_id
                )
        else:
            last_ids = await temp.get_last_ids(query)
            for msg_id in last_ids:
                await bot.delete_message(
                    chat_id=query.chat.id,
                    message_id=msg_id
                )
    except:
        print("Error: delete message")


@router.message()
async def other_message(message: types.Message):
    match await temp.get_status(message):
        case "add_description":
            await temp.add_message(message, message.text)
            text = "<em><b>Вы уверены в добавлении этого описания?</b></em>"
            msg = await message.reply(text, parse_mode=ParseMode.HTML, reply_markup=callbacks.builder_yes_no_keyboard)
            await delete_messages(message, message=True)
            await temp.add_ids(message, msg.message_id)
        case "add_tasks":
            await commands.add_tasks(message, add=True)
        case _:
            await message.answer("Текущий функционал", reply_markup=callbacks.builder_menu_main)
