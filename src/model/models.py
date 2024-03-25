from aiogram.fsm.state import StatesGroup, State

class SetSheodule(StatesGroup):
    domen_set = State()
    time_set = State