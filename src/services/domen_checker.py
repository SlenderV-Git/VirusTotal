import requests
from aiogram import Bot
from time import sleep

def post_url(url, api_key):
    headers = {"x-apikey": api_key, "accept": "application/json"}
    data = {"url" : url}
    response = requests.post(f"https://www.virustotal.com/api/v3/urls", headers=headers, data=data)
    print(response.content, response.status_code)
    return response.json()["data"]["id"]

async def check_url(bot, uid, url, api_key, tg_id):
    
    headers = {"x-apikey": api_key, "accept": "application/json"}
    data = {"url" : url}
    response = requests.post(f"https://www.virustotal.com/api/v3/urls", headers=headers, data=data)
    print(response.content, response.status_code)
    
    sleep(20)
    
    api_url = f"https://www.virustotal.com/api/v3/analyses/{uid}"
    headers = {"x-apikey" : api_key, "accept": "application/json"}
    response = requests.get(api_url, headers=headers)
    await check(data=response.json()["data"]["attributes"]["results"], 
                tg_id=tg_id, 
                bot=bot, 
                url = url)

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
        info = "☣\n".join(result)
        text = f"Данные сервисы считают этот сайт: 🦠 {url}🦠 подозрительным\n{info}"
        await bot.send_message(chat_id=tg_id, text=text)




        
    