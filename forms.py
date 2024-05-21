from aiogram.fsm.state import StatesGroup, State


class TaskForm(StatesGroup):
    text = State()
