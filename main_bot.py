import telebot
from telebot import types

API_TOKEN = '7251858052:AAFIYXu8v45VQySeDj-F1hrjMty_mOQ-ApM'
bot = telebot.TeleBot(API_TOKEN)

user_balances = {}

address_response = """
Send TAPS/HMSTR to address:
<p>YOUR_WALLET_ADDRESS</p>

Money will be deposited automatically to Balance 💰
"""


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    address_btn = types.KeyboardButton('Address 📥')
    balance_btn = types.KeyboardButton('Balance 💰')
    withdrawal_btn = types.KeyboardButton('Withdrawal 📤')
    help_btn = types.KeyboardButton('Help 🛠')
    sprt_btn = types.KeyboardButton('Support Center 👮‍♂️')
    markup.add(address_btn, balance_btn, withdrawal_btn, help_btn, sprt_btn)
    bot.send_message(message.chat.id, "Welcome! Choose an option:", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.text == 'Address 📥':
        bot.send_message(message.chat.id, "Your address is: YOUR_WALLET_ADDRESS")
    elif message.text == 'Balance 💰':
        user_id = message.from_user.id
        balance = user_balances.get(user_id, 0)
        bot.send_message(message.chat.id, f"Your balance is: {balance} UZS")
    elif message.text == 'Help 🛠':
        bot.send_message(message.chat.id, "Send your hamster combat ton jettons to the specified address. Your balance will be updated automatically.")
    elif message.text == 'Support Center 👮‍♂️':
        bot.send_message(message.chat.id, "Write some questions to support center @support")
    elif message.text == 'Withdrawal 📤':
        bot.send_message(message.chat.id, "To Withdrawal send card number")
    else:
        bot.send_message(message.chat.id, "Invalid option. Please choose from Address, Balance, or Help.")

def notify_user(user_id, amount):
    user_balances[user_id] = user_balances.get(user_id, 0) + amount
    bot.send_message(user_id, f"You received {amount} UZS. Your new balance is {user_balances[user_id]} UZS")

# notify_user(123456789, 1000)

bot.polling()

# 1=6, 2=9, 3=5, 4=2, 5=0, 6=8, 7=1, 8=7, 9=4, 0=3



