from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from datetime import datetime
from src.lexicon.lexicon import captcha_text, actual_url
from src.services.sheoduler import add_job, delete_job
from src.model.models import SetSheodule
from src.db.db import BDController
from src.services.domen_checker import handle_message
from src.config.config import load_settings
from apscheduler.schedulers.asyncio import AsyncIOScheduler

shedule = AsyncIOScheduler()
rt = Router()
bd = BDController("src//db//test.db")

@rt.message(CommandStart())
async def start_process(message : Message):
    await message.answer(text = captcha_text)

@rt.message(Command("list"))
async def cheak_process(message : Message):
    data = bd.get_data(int(message.from_user.id))
    if data:
        await message.answer(bd.get_data(int(message.from_user.id)))
    else:
        await message.answer("Нет активных задач")
    
@rt.message(Command("clear"))
async def clear_data(message : Message):
    bd.delete_data(message.from_user.id)
    await delete_job(schedule=shedule)
    await message.answer("Задачи очищены /list")
    
@rt.message(Command("setup"), StateFilter(None))
async def start_setup(message : Message, state : FSMContext):
    await message.answer(text= actual_url)
    await state.set_state(SetSheodule.domen_set)

@rt.message(StateFilter(SetSheodule.domen_set))
async def set_domen(message : Message, state : FSMContext):
    if len(message.text.split()) == 2:
        domen, time = message.text.split()
        bd.add_user(message.from_user.id, message.from_user.username, domen, int(time))
        await  add_job(func=handle_message, 
                interval=int(time), 
                domen= domen, 
                token = load_settings().api_token, 
                bot=message.bot,
                tg_id=message.chat.id,
                shedule=shedule)
        shedule.start()
        await message.answer(bd.get_data(int(message.from_user.id)))
    else:
        await message.answer("Неправильный формат данных")
    await state.clear()

    
