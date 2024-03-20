from aiogram import Bot
import config
import db.temp_db as temp


bot = Bot(token=config.TOKEN)


async def delete_messages(query):
    try:
        last_ids = await temp.get_last_ids(query.message)
        for msg_id in last_ids:
            await bot.delete_message(
                chat_id=query.message.chat.id,
                message_id=msg_id
            )
    except:
        pass