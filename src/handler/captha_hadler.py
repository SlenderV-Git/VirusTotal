from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from datetime import datetime
from src.lexicon.lexicon import captcha_text, actual_url
from src.services.sheoduler import add_job, delete_job, stop_job
from src.model.models import SetSheodule
from src.db.db import BDController
from src.services.domen_checker import check_url
from src.config.config import load_settings
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

shedule = AsyncIOScheduler()

rt = Router()
bd = BDController("src//db//test.db")

@rt.message(CommandStart())
async def start_process(message : Message):
    await message.answer(text = captcha_text)
    
@rt.message(Command("stop"))
async def stop_run(message : Message):
    buttons = bd.get_button_data(tg_id=message.from_user.id)
    if buttons:
        but = [[InlineKeyboardButton(text=text, callback_data=data)] for text, data in buttons]
        await message.answer(text="Нажмите на задачу для удаления✍", reply_markup=InlineKeyboardMarkup(inline_keyboard=but))
    else:
        await message.answer(text="📄Нет активных задач📄")
@rt.callback_query()
async def cancel_job(callback : CallbackQuery):
    bd.delete_job(callback.data)
    await callback.message.edit_text("Задача удалена✔️")
    await stop_job(schedule=shedule, job_id=callback.data)
    
    
@rt.message(Command("list"))
async def cheak_process(message : Message):
    data = bd.get_data(int(message.from_user.id))
    if data:
        await message.answer(bd.get_data(int(message.from_user.id)))
    else:
        await message.answer("📄Нет активных задач📄")
    
@rt.message(Command("clear"))
async def clear_data(message : Message):
    bd.delete_data(message.from_user.id)
    await delete_job(schedule=shedule)
    await message.answer("🚫Задачи очищены /list🚫")
    
@rt.message(Command("setup"), StateFilter(None))
async def start_setup(message : Message, state : FSMContext):
    await message.answer(text= actual_url)
    await state.set_state(SetSheodule.domen_set)

@rt.message(StateFilter(SetSheodule.domen_set))
async def set_domen(message : Message, state : FSMContext):
    if len(message.text.split()) == 2:
        domen, time = message.text.split()
        await add_job(func=check_url, 
                interval=int(time), 
                domen= domen, 
                token = load_settings().api_token, 
                bot=message.bot,
                tg_id=message.chat.id,
                shedule=shedule,
                time= time,
                message = message,
                bd=bd)
        await message.answer(text=f"✅Задача на проверку домена {domen} каждые {time} секунд добавлена")
        await message.answer(bd.get_data(int(message.from_user.id)))
    else:
        await message.answer("Неправильный формат данных")
    await state.clear()
    shedule.start()
    
