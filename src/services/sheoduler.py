
from typing import Callable
from apscheduler.schedulers.asyncio import AsyncIOScheduler

async def add_job(func: Callable, interval, domen, token, bot, tg_id, shedule : AsyncIOScheduler):
    print("Задача добавлена")
    shedule.add_job(func, trigger="interval", seconds = interval, kwargs={'bot' : bot, 'url' : domen, 'api_key' : token, 'tg_id' : tg_id})

async def delete_job(schedule : AsyncIOScheduler):
    schedule.remove_all_jobs()
