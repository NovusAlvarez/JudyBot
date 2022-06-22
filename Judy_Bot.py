import telebot;
from telebot import types

bot = telebot.TeleBot('no ;)')

name = '';
surname = '';
age = 0;


@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/reg':
        bot.send_message(message.from_user.id, "Так, давай тебя зарегестрируем. Для начала, как тебя зовут?");
        bot.register_next_step_handler(message, get_name);
    else:
        bot.send_message(message.from_user.id, 'Блин, Чумба! Я же регаю тебя, давай по делу. Напиши /reg');


def get_name(message):
    global name;
    name = message.text;
    bot.send_message(message.from_user.id, 'Записала. Какая у тебя фамилия?');
    bot.register_next_step_handler(message, get_surname);


def get_surname(message):
    global surname;
    surname = message.text;
    bot.send_message(message.from_user.id, 'Ага. Сколько тебе лет?');
    bot.register_next_step_handler(message, get_age);


def get_age(message):
    global age;
    while age == 0:
        try:
            age = int(message.text)
        except Exception:
            bot.send_message(message.from_user.id, 'Цифрами, пожалуйста')
    keyboard = types.InlineKeyboardMarkup();
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='no');
    keyboard.add(key_yes);
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no');
    keyboard.add(key_no);
    question = 'Так, вроде это всё, давай проверим: Тебе ' + str(
        age) + ' лет, тебя зовут ' + name + ' ' + surname + '?'
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":
        bot.send_message(call.message.chat.id, 'Супер! Чуть позже отправлю твои данные в систему и будешь ходить там как свой ;)');
    elif call.data == "no":
        bot.polling(none_stop=True, interval=0)


if __name__ == '__main__':
    bot.polling()

