import json
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime

API_TOKEN = '7325245420:AAGZ25uiN9wNkb34unMV_6ePGMDyZh-4M8k'
bot = telebot.TeleBot(API_TOKEN)

def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def format_transaction(transaction):
    date_obj = datetime.strptime(transaction['date'], '%Y-%m-%dT%H:%M:%SZ')
    formatted_date = date_obj.strftime('%Y-%m-%d %H:%M:%S')
    
    transaction_details = (
        f"Tranzaksiya ID: {transaction['transaction_id']}\n\n"
        f"Sana: {formatted_date}\n"
        f"Summa: ${transaction['amount']:,.2f} {transaction['currency']}\n"
        f"Turi: {'Debet' if transaction['type'] == 'debit' else 'Kredit'}\n"
        f"Tavsif: {transaction['description']}\n"
        f"Kategoriya: {transaction['category']}\n"
        f"Hisob: {transaction['account']['account_name']} (ID: {transaction['account']['account_id']})\n"
        f"Holati: {'Bajarildi' if transaction['status'] == 'completed' else 'Kutilmoqda'}\n"
    )
    return transaction_details

def create_markup(index, total):
    markup = InlineKeyboardMarkup()
    markup.row_width = 3

    if index > 1:
        markup.add(InlineKeyboardButton("Orqaga", callback_data=f"previous:{index}"))

    markup.add(InlineKeyboardButton(f"{index}/{total}", callback_data="empty_button"))
    
    if index < total:
        markup.add(InlineKeyboardButton("Keyingisi", callback_data=f"next:{index}"))
    
    markup.add(
        InlineKeyboardButton("Tasdiqlash", callback_data="confirm"),
        InlineKeyboardButton("Shikoyat qilish", callback_data="report")
        )

    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    json_file_path = 'validators.json'
    
    data = read_json_file(json_file_path)
    
    current_index = 1
    total_transactions = len(data['transactions'])
    current_transaction = data['transactions'][current_index - 1]
    bot.send_message(message.chat.id, format_transaction(current_transaction), reply_markup=create_markup(current_index, total_transactions))

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data.startswith("confirm"):
        bot.answer_callback_query(call.id, "Siz barcha tranzaksiyalarni tasdiqladingiz.")
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)

    elif call.data.startswith("report"):
        bot.answer_callback_query(call.id, "Siz barcha tranzaksiyalarni shikoyat qildingiz.")
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
        
    if call.data.startswith("empty_button"):
        return

    try:
        index = int(call.data.split(':')[1])
    except IndexError:
        return
    data = read_json_file('validators.json')
    total_transactions = len(data['transactions'])
    
    if call.data.startswith("previous") and index > 1:
        index -= 1
    elif call.data.startswith("next") and index < total_transactions:
        index += 1
    
    current_transaction = data['transactions'][index - 1]
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=format_transaction(current_transaction), reply_markup=create_markup(index, total_transactions))

if __name__ == '__main__':
    bot.polling(none_stop=True)