import telebot
import sqlite3
from telebot import types

BOT_TOKEN = '7017269336:AAGgq3V8EJ6F4s180UchUCnI-LzR87iVJt8'

bot = telebot.TeleBot(BOT_TOKEN)

from db_nakrutka import *

user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Welcome! Please enter your user ID:")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id

    if chat_id not in user_data:
        user_data[chat_id] = {'step': 1}

    step = user_data[chat_id]['step']

    if step == 1:
        user_data[chat_id]['user_id'] = message.text
        user_data[chat_id]['step'] = 2
        bot.send_message(chat_id, "Got it! Now, please enter your authorization header:")
    elif step == 2:
        user_data[chat_id]['authorization_header'] = message.text
        user_id = user_data[chat_id]['user_id']
        authorization_header = user_data[chat_id]['authorization_header']

        add_user(user_id, authorization_header)

        bot.send_message(chat_id, "Thank you! Your information has been saved.")
        user_data.pop(chat_id)

bot.polling()
