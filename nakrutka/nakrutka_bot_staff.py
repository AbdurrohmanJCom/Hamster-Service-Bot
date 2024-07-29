import telebot
from db_manage import add_user, get_users, get_user, delete_user, update_user

API_TOKEN = '7017269336:AAGgq3V8EJ6F4s180UchUCnI-LzR87iVJt8'

bot = telebot.TeleBot(API_TOKEN)

user_data = {}

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    help_text = (
        "Добро пожаловать в бот управления пользователями!\n"
        "Вот доступные команды:\n"
        "/add_user - Добавить нового пользователя\n"
        "/get_users - Получить всех пользователей\n"
        "/get_user - Получить пользователя по ID\n"
        "/delete_user - Удалить пользователя по ID\n"
        "/update_user - Обновить данные пользователя\n"
        "/help - Показать это сообщение"
    )
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['add_user'])
def add_user_start(message):
    chat_id = message.chat.id
    user_data[chat_id] = {}
    msg = bot.send_message(chat_id, "Пожалуйста, введите ID пользователя:")
    bot.register_next_step_handler(msg, process_user_id)

def process_user_id(message):
    chat_id = message.chat.id
    user_id = message.text
    user_data[chat_id]['user_id'] = user_id
    msg = bot.send_message(chat_id, "Пожалуйста, введите заголовок авторизации:")
    bot.register_next_step_handler(msg, process_auth_header)

def process_auth_header(message):
    chat_id = message.chat.id
    auth_header = message.text
    user_data[chat_id]['authorization_header'] = auth_header
    add_user(user_data[chat_id]['user_id'], user_data[chat_id]['authorization_header'])
    bot.send_message(chat_id, "Пользователь успешно добавлен!")

@bot.message_handler(commands=['get_users'])
def handle_get_users(message):
    users = get_users()
    if users:
        response = "\n".join([f"ID пользователя: {user[0]}, Заголовок авторизации: {user[1]}" for user in users])
    else:
        response = "Пользователи не найдены."
    bot.send_message(message.chat.id, response)

@bot.message_handler(commands=['get_user'])
def get_user_start(message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, "Пожалуйста, введите ID пользователя:")
    bot.register_next_step_handler(msg, process_get_user_id)

def process_get_user_id(message):
    chat_id = message.chat.id
    user_id = message.text
    user = get_user(user_id=user_id)
    if user:
        response = f"ID пользователя: {user[0]}, Заголовок авторизации: {user[1]}"
    else:
        response = "Пользователь не найден."
    bot.send_message(chat_id, response)

@bot.message_handler(commands=['delete_user'])
def delete_user_start(message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, "Пожалуйста, введите ID пользователя:")
    bot.register_next_step_handler(msg, process_delete_user_id)

def process_delete_user_id(message):
    chat_id = message.chat.id
    user_id = message.text
    delete_user(user_id=user_id)
    bot.send_message(chat_id, "Пользователь успешно удален!")

@bot.message_handler(commands=['update_user'])
def update_user_start(message):
    chat_id = message.chat.id
    user_data[chat_id] = {}
    msg = bot.send_message(chat_id, "Пожалуйста, введите текущий ID пользователя:")
    bot.register_next_step_handler(msg, process_current_user_id)

def process_current_user_id(message):
    chat_id = message.chat.id
    user_id = message.text
    user_data[chat_id]['current_user_id'] = user_id
    msg = bot.send_message(chat_id, "Пожалуйста, введите новый ID пользователя (или 'пропустить', чтобы оставить текущий):")
    bot.register_next_step_handler(msg, process_new_user_id)

def process_new_user_id(message):
    chat_id = message.chat.id
    new_user_id = message.text
    if new_user_id.lower() != 'пропустить':
        user_data[chat_id]['new_user_id'] = new_user_id
    else:
        user_data[chat_id]['new_user_id'] = None
    msg = bot.send_message(chat_id, "Пожалуйста, введите новый заголовок авторизации (или 'пропустить', чтобы оставить текущий):")
    bot.register_next_step_handler(msg, process_new_auth_header)

def process_new_auth_header(message):
    chat_id = message.chat.id
    new_auth_header = message.text
    if new_auth_header.lower() != 'пропустить':
        user_data[chat_id]['new_auth_header'] = new_auth_header
    else:
        user_data[chat_id]['new_auth_header'] = None
    update_user(
        user_data[chat_id]['current_user_id'],
        new_user_id=user_data[chat_id]['new_user_id'],
        new_authorization_header=user_data[chat_id]['new_auth_header']
    )
    bot.send_message(chat_id, "Пользователь успешно обновлен!")

if __name__ == '__main__':
    bot.polling()
