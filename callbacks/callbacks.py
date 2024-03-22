from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


class CallbacksDelimetr(CallbackData, prefix="my"):
    foo: str
    delimetr: str


class SmbdCallbacks(CallbackData, prefix="my"):
    foo: str
    smbd: str


class MenuCallbaks(CallbackData, prefix="my"):
    foo: str
    command: str


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


builder_back_keyboard = InlineKeyboardBuilder()
builder_back_keyboard.button(text="Отмена", callback_data=MenuCallbaks(foo="menu", command="Отмена"))
builder_back_keyboard = builder_back_keyboard.as_markup()


builder_yes_no_keyboard = InlineKeyboardBuilder()
for i in ["Да", "Нет"]:
    builder_yes_no_keyboard.button(text=f"{i}", callback_data=MenuCallbaks(foo="menu",
                                                                           command=f"{i}-add_to_description"))
builder_yes_no_keyboard = builder_yes_no_keyboard.adjust(2).as_markup()


builder_yes_no_keyboard_add_tasks = InlineKeyboardBuilder()
for i in ["Добавить", "Отмена"]:
    builder_yes_no_keyboard_add_tasks.button(text=f"{i}",
                                             callback_data=MenuCallbaks(foo="menu", command=f"{i}-add_tasks"))
builder_yes_no_keyboard_add_tasks = builder_yes_no_keyboard_add_tasks.adjust(2).as_markup()


builder_menu_main = InlineKeyboardBuilder()
for i in ["Добавить задачу", "Удалить задачи", "Просмотреть задачи", "Создать блокнот",
          "Добавить описание", "Изменить разделитель"]:
    builder_menu_main.button(text=f"{i}", callback_data=MenuCallbaks(foo="main_menu", command=f"{i}"))
builder_menu_main = builder_menu_main.adjust(1).as_markup()


async def choice_builder(books):
    builder = InlineKeyboardBuilder()
    for i in books:
        builder.button(text=f"{i}", callback_data=SmbdCallbacks(foo="choice_notebook", smbd=f"{i}"))
    return builder.adjust(3).as_markup()
