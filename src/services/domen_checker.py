import requests
from aiogram import Bot

async def handle_message(bot : Bot, url, api_key, tg_id):
    
    headers = {"x-apikey": api_key, "accept": "application/json"}
    response = requests.get(f"https://www.virustotal.com/api/v3/domains/{url}", headers=headers)
    return await check(response.json()["data"]["attributes"]["last_analysis_results"], tg_id, bot, url)
    
async def check(data : dict, tg_id, bot : Bot, url):
    print("Проверка")
    result = []
    for k,v in data.items():
        if not(v["category"] in ["harmless", "undetected"] and v["result"] in ["unrated", "clean"]):
            result.append(k)
    if not result:
        print("Проверка успешна, чисто")
    else:
        print("Найдены угрозы")
        info = "\n".join(result)
        text = f"Данные сервисы считают этот сайт: {url} подозрительным\n{info}"
        await bot.send_message(chat_id=tg_id, text=text)
        


        
    