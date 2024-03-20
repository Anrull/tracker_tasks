from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


class CallbacksDelimetr(CallbackData, prefix="my"):
    foo: str
    delimetr: str


class CallbacksDelete(CallbackData, prefix="my"):
    foo: str
    id_task: int


builder_delimetr = InlineKeyboardBuilder()
for elem in ["\\", "*", "/", "+", "-", "|", "_", "="]:
    builder_delimetr.button(text=elem, callback_data=CallbacksDelimetr(foo="delimetr", delimetr=elem))
builder_delimetr = builder_delimetr.adjust(5).as_markup()


async def delete_builder(count):
    builder = InlineKeyboardBuilder()
    builder.button(text="Отмена", callback_data=CallbacksDelete(foo="delete_tasks", id_task=-1))
    builder.button(text="Готово", callback_data=CallbacksDelete(foo="delete_tasks", id_task=-2))
    for i in count:
        builder.button(text=f"{i}", callback_data=CallbacksDelete(foo="delete_tasks", id_task=i))
    return builder.adjust(2, 5).as_markup()
