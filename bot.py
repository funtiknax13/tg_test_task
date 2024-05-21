import asyncio
import datetime

from forms import TaskForm
from db import DBmanager
from config import config

from aiogram.filters import Command, StateFilter

from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode

import os
from dotenv import load_dotenv


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=dotenv_path)

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(storage=MemoryStorage())

db_connect = DBmanager(os.getenv('DB_NAME'), config())


@dp.message(StateFilter(None), Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет, этот бот поможет тебе планировать свои задачи.\n"
                         "Используй команды /add - для добавления задачи и /tsk - вывод задач",
                         parse_mode=ParseMode.HTML)


@dp.message(StateFilter(None), Command("add"))
async def cmd_add(message: types.Message, state: FSMContext):
    await message.answer("Введи текст задачи\n",
                         parse_mode=ParseMode.HTML)
    await state.set_state(TaskForm.text)


@dp.message(TaskForm.text)
async def process_task_form(message: types.Message, state: FSMContext):
    await db_connect.add_task(message.from_user.id, message.text, datetime.datetime.now())
    await state.clear()
    await message.answer("Задача сохранена.",
                         parse_mode=ParseMode.HTML)


@dp.message(StateFilter(None), Command("tsk"))
async def cmd_tsk(message: types.Message):
    data = await db_connect.get_task_list(message.from_user.id)
    tasks = ''
    for item in data:
        tasks += f'{item[0]}: {item[2]}\nВремя создания:{item[3].strftime("%d-%m-%Y %H:%M")}\n\n'

    await message.answer("<b>Твои задачи:</b>\n" + tasks,
                         parse_mode=ParseMode.HTML)


@dp.message(StateFilter(None))
async def unknown_commands(message: types.Message):
    await message.answer("Я не знаю такой команды, выбери /add - для добавления задачи и /tsk - вывод задач",
                         parse_mode=ParseMode.HTML)


async def main():
    await db_connect.create_table()
    await dp.start_polling(bot)


asyncio.run(main())
