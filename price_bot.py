import telebot
import schedule
import time
from get_price import getPrice

API_TOKEN = '7484643757:AAEiL6haJr4NXWYXDttFUGYB-I0iIAREFJs'
CHANNEL_USERNAME = '@TapSwap_strike_price'

bot = telebot.TeleBot(API_TOKEN)

def send_price():
    price = getPrice('not')
    message = f"The current price of NOT is ${price}"
    bot.send_message(CHANNEL_USERNAME, message)

schedule.every(1).minutes.do(send_price)

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    send_price()
    run_schedule()
