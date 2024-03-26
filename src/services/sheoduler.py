
from typing import Callable
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from src.db.db import BDController
from src.services.domen_checker import post_url
from src.config.config import load_settings

bd = BDController("src//db//test.db")

async def add_job(func: Callable, interval, domen, token, bot, tg_id, shedule : AsyncIOScheduler, time, message, bd : BDController):
    print("Задача добавлена")
    url_id = bd.check_url(domen=domen)
    if not url_id:
        url_id = post_url(url=domen, api_key=load_settings().api_token)
        bd.add_url(domen=domen, url_id=url_id)
        
    job = shedule.add_job(func, trigger="interval", seconds = interval, kwargs={'bot' : bot, 'uid' : url_id, 'url' : domen, 'api_key' : token, 'tg_id' : tg_id})
    print(job.id)
    bd.add_user(message.from_user.id, message.from_user.username, domen, int(time), job_id=job.id)

async def delete_job(schedule : AsyncIOScheduler):
    schedule.remove_all_jobs()

async def stop_job(schedule : AsyncIOScheduler, job_id):
    schedule.remove_job(job_id=job_id)
