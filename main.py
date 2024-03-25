from aiogram import Bot, Dispatcher
from asyncio import run, get_event_loop
from aiogram.fsm.storage.memory import MemoryStorage
from src.config.config import load_settings
from src.handler import captha_hadler



async def main():
    bot = Bot(token = load_settings().bot_token)
    storage = MemoryStorage()
    
    dp = Dispatcher(storage=storage)
    dp.include_router(captha_hadler.rt)
    await dp.start_polling(bot)
    
    
if __name__ == "__main__":
    run(main())