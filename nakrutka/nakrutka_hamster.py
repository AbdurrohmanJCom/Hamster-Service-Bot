import requests
import json
import time
from db_nakrutka import *
import telebot

TELEGRAM_BOT_TOKEN = '7422888656:AAGhPUGrnY3O_MAfZwUL8LmQk4xPnJovLMc'
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

url = "https://api.hamsterkombat.io/clicker/tap"

def headers(authorization_header):
    return {
        "Authorization": authorization_header,
        "Content-Type": "application/json",
        "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Telegram";v="9.5.2", "TelegramWeb";v="1.3.14"',
        "Sec-Ch-Ua-Mobile": "?1",
        "Sec-Ch-Ua-Platform": '"Android"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Linux; Android 12; SM-G980F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36 TelegramWeb/1.3.14"
    }

def data():
    return {
        "count": 10000,
        "availableTaps": 0,
        "timestamp": int(time.time() * 1000)
    }

def request(authorization_header):
    response = requests.post(url, headers=headers(authorization_header), data=json.dumps(data()))
    return response.status_code, response.json()

def main():
    users = get_users()
    for user_id, authorization_header in users:
        status_code, result = request(authorization_header)
        try:
            balance = result['clickerUser']['balanceCoins']
            formatted_balance = "{:,.0f}".format(balance)
            bot.send_message(user_id, f"HMSTR: {formatted_balance}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    while True:
        main()
        time.sleep(20)
