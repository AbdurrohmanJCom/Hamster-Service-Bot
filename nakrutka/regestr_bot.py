import telebot
from telebot import types
from db_manage import get_user, add_user

BOT_TOKEN = '6305513266:AAFYXJ3gvTSZHvmz__dk_mSSBABNTlupllo'

bot = telebot.TeleBot(BOT_TOKEN)

user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Добро пожаловать! Пожалуйста, введите свой Authorization Token пользователя:")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.chat.id
    authorization_header = message.text

    # Check if the Authorization Token starts with "Bearer "
    if not authorization_header.startswith("Bearer "):
        bot.send_message(user_id, "Недопустимый формат Authorization Token.")
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        return

    # Check if the user_id or authorization_header already exists
    existing_user_by_id = get_user(user_id=user_id)
    existing_user_by_token = get_user(authorization_header=authorization_header)

    if existing_user_by_id:
        bot.send_message(user_id, "User ID уже существует в базе данных.")
    elif existing_user_by_token:
        bot.send_message(user_id, "Authorization Token уже существует в базе данных.")
    else:
        add_user(user_id, authorization_header)
        bot.send_message(user_id, "Tashakkur! Balansingizni korish uchun @strike_nakrutka_bot ga obuna boling!")

    # Delete the user's message after handling
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

bot.polling()
