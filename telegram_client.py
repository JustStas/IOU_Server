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
def balance_start(message):
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
def user_load_start(message):
    user_ids = bot.send_message(message.chat.id, 'Who do you want to load?', reply_markup=keyboard_with_users())
    bot.register_next_step_handler(user_ids, load_user)


def load_user(message):
    user = User(username=message.text)
    user.load()
    bot.reply_to(message, user.description, reply_markup=types.ReplyKeyboardRemove())


@bot.message_handler(commands=['link_my_telegram'])
def telegram_link_start(message):
    user_ids = bot.send_message(message.chat.id, 'Who are you?', reply_markup=keyboard_with_users())
    bot.register_next_step_handler(user_ids, link_telegram)


def link_telegram(message):
    username = message.text
    telegram_id = message.from_user.id
    server_conn('link_telegram_id', [username, telegram_id])
    bot.reply_to(message, 'Telegram linked to {}'.format(username), reply_markup=types.ReplyKeyboardRemove())


@bot.message_handler(commands=['new_trx'])
def telegram_link_start(message):
    trx_vol = bot.send_message(message.chat.id, 'How big was the expense?', reply_markup=types.ForceReply(selective=False))
    bot.register_next_step_handler(trx_vol, define_creditor)


def define_creditor(message):
    dic = {'amount': message.text, 'debtors': []}
    user_ids = bot.send_message(message.chat.id, 'Who is the creditor?', reply_markup=keyboard_with_users())
    bot.register_next_step_handler(user_ids, lambda msg: define_split_type(dic, msg))


def define_split_type(dic, message):
    dic['creditor'] = message.text
    keyboard = types.ReplyKeyboardMarkup()
    splits = ['Equal split']
    for split in splits:
        keyboard.add(types.InlineKeyboardButton(split, callback_data=split))
    split_type = bot.send_message(message.chat.id, 'How would you like to split?', reply_markup=keyboard)
    bot.register_next_step_handler(split_type, lambda msg: process_transaction_split(dic, msg))


def process_transaction_split(dic, message):
    print('dic', dic)
    dic['split_type'] = message
    if dic['split_type'].text == 'Equal split':

        keyboard = keyboard_with_users(exclude_users=dic['debtors'], add_nobody=True)
        split_member = bot.send_message(message.chat.id,
                                        'Who would you like to include? Select "Nobody" to end allocation',
                                        reply_markup=keyboard)  # Todo Will need to replace "Nobody" with some shit otherwise such a username will break everything
        bot.register_next_step_handler(split_member, lambda msg: add_member_to_split(dic, msg))


def add_member_to_split(dic, message):
    print('TEXT', message.text)
    if message.text == 'Nobody':
        server_conn('new_trx_with_equal_split', {'amount': dic['amount'],
                                                 'creditor': dic['creditor'],
                                                 'debtors': dic['debtors']})

        bot.send_message(message.chat.id, '''{0}'s transaction of {1} has
                                             been equally split among {2}.'''.format(dic['creditor'],
                                                                                     dic['amount'],
                                                                                     dic['debtors']))
    else:
        print('DIC', dic['debtors'])
        print('TEXT', message.text)
        dic['debtors'].append(message.text)
        print('DIC', dic['debtors'])
        process_transaction_split(dic, dic['split_type'])


def keyboard_with_users(group=None, exclude_users=[], add_nobody=False):
    print('Excl', exclude_users)
    keyboard = types.ReplyKeyboardMarkup()
    usernames = list_users()
    for username in usernames:
        if len(exclude_users) > 0 and username in exclude_users:
            pass
        else:
            keyboard.add(types.InlineKeyboardButton(username, callback_data=username))
    if add_nobody:
        keyboard.add(types.InlineKeyboardButton('Nobody', callback_data='Nobody'))
    return keyboard


while True:
    try:
        bot.polling()
    except Exception as e:
        print(e)
        print('Error!!! Falling to sleep for 60 seconds...')
        time.sleep(60)
