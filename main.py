from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
import db.user as user
import db.temp_db as temp_db
import backend.commands as commands
import callbacks.handler_callbacks as handler_callbacks

import config
import asyncio
import tracemalloc


bot = Bot(token=config.TOKEN)
dp = Dispatcher()

dp.include_router(router=handler_callbacks.router)
dp.include_router(router=commands.router)


@dp.message(Command("start"))
async def get_start(message: types.Message):
    await user.create_user(message)
    await temp_db.create_new_user(message)
    await message.answer("Добро пожаловать в бот-трекер задач")


@dp.message(Command("help"))
async def get_help(message: types.Message):
    await message.answer(config.help_message)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    tracemalloc.start()
    asyncio.run(main())
