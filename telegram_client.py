import telebot
import requests
import time
from telebot import types
from telebot.apihelper import ApiException
from core import server_conn, list_users
from classes import User
from support_functions import str_to_list

bot = telebot.TeleBot('1012372350:AAG7N6oZPE5mi9uLSsNwwvN2fZhHEJRlNVk')

print('Bot started')


@bot.message_handler(commands=['balance_overview'])
def balance(message):
    markup = types.ForceReply(selective=False)
    user_ids = bot.send_message(message.chat.id, 'Who do you want the overview for?', reply_markup=markup)
    bot.register_for_reply(user_ids, balance_overview)


def balance_overview(message):
    if message.text == '':
        user_ids = -1
    else:
        user_ids = message.text

    to_print = ''

    try:
        user_ids = int(user_ids)
    except ValueError:
        pass

    if user_ids == -1:
        user_ids = []
    elif isinstance(user_ids, list):
        pass
    elif isinstance(user_ids, int):
        user_ids = [user_ids]
    elif isinstance(user_ids, str):
        try:
            user_ids = str_to_list(user_ids)
            for i in user_ids:
                if not isinstance(i, int):
                    to_print += '\nWrong input'
                    bot.reply_to(message, to_print)
                    return
        except Exception:
            to_print += '\nWrong input'
            bot.reply_to(message, to_print)
            return
    else:
        to_print += '\nWrong input'
        bot.reply_to(message, to_print)
        return
    print('I AM HERE2', message.text)
    users = server_conn('list_users')
    print('I AM HERE3', message.text)
    counterpart_ids = users.to_list()
    if not user_ids:
        user_ids = counterpart_ids

    for user_id in user_ids:
        print('I AM HERE4', message.text)
        to_print += '\n'
        to_print += ('=' * 50)
        user1 = User(user_id=user_id)
        user1.load()
        to_print += '\n'
        to_print += user1.f_name
        user1_balance = user1.balance()
        to_print += '\n'
        to_print += ('Accumulated debt: {0} RUB'.format(user1_balance[0]))
        to_print += '\n'
        to_print += ('Accumulated receivables: {0} RUB'.format(user1_balance[1]))

        remaining_users = [i for i in counterpart_ids if i != user1.user_id]

        for counterpart_id in remaining_users:
            user2 = User(user_id=counterpart_id)
            counterpart_balance = user1.balance(counterpart_id=user2.user_id)
            debt_to_counterpart = counterpart_balance[0]
            receivables_from_counterpart = counterpart_balance[1]
            if debt_to_counterpart != 0 or receivables_from_counterpart != 0:
                user2.load()
                user2.describe()
                to_print += '\n'
                to_print += ('-' * 20)
                to_print += '\n'
                to_print += ('Debt to {0}: {1} RUB:'.format(user2.f_name, debt_to_counterpart))
                to_print += '\n'
                to_print += ('Receivables from {0}: {1} RUB'.format(user2.f_name, receivables_from_counterpart))
    bot.reply_to(message, to_print)


@bot.message_handler(commands=['load_user'])
def balance(message):
    keyboard = types.ReplyKeyboardMarkup()
    user_ids = list_users()
    for id in user_ids:
        keyboard.add(types.InlineKeyboardButton(id, callback_data=id))
    user_ids = bot.send_message(message.chat.id, 'Who do you want to load?', reply_markup=keyboard)
    bot.register_next_step_handler(user_ids, load_user)

def load_user(message):
    user = User(user_id=int(message.text))
    user.load()
    bot.reply_to(message, user.description, reply_markup=types.ReplyKeyboardRemove())


@bot.message_handler(content_types=['text'])
def test(message):
    print(message)

    for ent in message.entities:
        # if ent.type in ['text_mention', 'mention']:
        if True:
            print(ent)
            # print(ent.user.id)
    user_ids = bot.send_message(message.chat.id, 'HI')


while True:
    try:
        bot.polling()
    except Exception as e:
        print(e)
        print('Error!!! Falling to sleep for 15 seconds...')
        time.sleep(15)
