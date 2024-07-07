import telebot
import schedule
import time
from get_price import getPrice

API_TOKEN = '7484643757:AAEiL6haJr4NXWYXDttFUGYB-I0iIAREFJs'
CHANNEL_USERNAME = '@TapSwap_strike_price'

bot = telebot.TeleBot(API_TOKEN)

def send_price():

    price = getPrice('not')
    price = float(price)  
    message = (
        f"<i>Strike Savdo NOT narxi:</i>\n"
        f"<blockquote>1 NOT - <b>{price:.2f} UZS</b></blockquote>\n"
        f"<blockquote>1000 NOT - <b>{price * 1000:,.2f} UZS</b></blockquote>\n"
        f"<blockquote>5000 NOT - <b>{price * 5000:,.2f} UZS</b></blockquote>"
    )
    bot.send_message(CHANNEL_USERNAME, message, parse_mode='HTML')


schedule.every(1).minutes.do(send_price)

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    send_price()
    run_schedule()
