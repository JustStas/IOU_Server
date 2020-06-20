import telebot
import requests
import time
from telebot import types
from telebot.apihelper import ApiException
from core import server_conn, list_users
from classes import User, Trx
from support_functions import str_to_list

bot = telebot.TeleBot('1012372350:AAG7N6oZPE5mi9uLSsNwwvN2fZhHEJRlNVk')

print('Bot started')


@bot.message_handler(commands=['balance_overview'])
def balance_start(message):
    markup = types.ForceReply(selective=False)
    user_ids = bot.send_message(message.chat.id, 'Who do you want the overview for?',
                                reply_markup=keyboard_with_users())
    bot.register_for_reply(user_ids, balance_overview)


def balance_overview(message):  # todo update with a keyboard & usernames

    if message.text == '':
        users = -1
    else:
        users = [message.text]
        print('users', users)

    to_print = ''

    counterparts = server_conn('list_users')
    counterpart_usernames = counterparts
    if users == -1:
        users = counterpart_usernames

    for username in users:
        print('user', username)
        to_print += '\n'
        to_print += ('=' * 50)
        user1 = User(username=username)
        user1.load()
        to_print += '\n'
        to_print += user1.f_name
        user1_balance = user1.balance()
        to_print += '\n'
        to_print += ('Accumulated debt: {0} RUB'.format(user1_balance[0]))
        to_print += '\n'
        to_print += ('Accumulated receivables: {0} RUB'.format(user1_balance[1]))

        remaining_users = [i for i in counterpart_usernames if i != user1.user_id]

        for counterpart_id in remaining_users:
            user2 = User(username=counterpart_id)
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
    bot.send_message(message.chat.id, to_print, reply_markup=types.ReplyKeyboardRemove())


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
    keyboard = keyboard_with_users()
    keyboard.add(
        types.InlineKeyboardButton('New user', callback_data='New'))  # todo: need to replace new with some shit
    user_ids = bot.send_message(message.chat.id, 'Who are you?', reply_markup=keyboard)
    bot.register_next_step_handler(user_ids, link_telegram)


def link_telegram(message):
    username = message.text
    if username == 'New':
        create_new_user(message)
    telegram_id = message.from_user.id
    server_conn('link_telegram_id', [username, telegram_id])
    bot.reply_to(message, 'Telegram linked to {}'.format(username), reply_markup=types.ReplyKeyboardRemove())


@bot.message_handler(commands=['create_new_user'])
def create_new_user(message, first_try=True):
    if first_try:
        request = 'Please enter a username'
    else:
        request = 'Username is taken or not valid. Please try another'
    username = bot.send_message(message.chat.id, request, reply_markup=types.ForceReply(selective=False))
    bot.register_next_step_handler(username, check_username)


def check_username(message):
    username = message.text
    if server_conn('check_user', username) is None or username[:2] == '###':
        get_f_name(message)
    else:
        create_new_user(message, first_try=False)


def get_f_name(message):
    user = User(username=message.text)
    f_name = bot.send_message(message.chat.id, 'What is your first name?',
                              reply_markup=types.ForceReply(selective=False))
    bot.register_next_step_handler(f_name, lambda msg: get_l_name(user, msg))


def get_l_name(user, message):
    user.f_name = message.text
    l_name = bot.send_message(message.chat.id, 'What is your last name?',
                              reply_markup=types.ForceReply(selective=False))
    bot.register_next_step_handler(l_name, lambda msg: finish_user_creation(user, msg))
    pass


def finish_user_creation(user, message):
    user.l_name = message.text
    user.telegram_id = message.from_user.id
    user.write()
    bot.send_message(message.chat.id, 'User {} successfully created'.format(user.username))


@bot.message_handler(commands=['new_trx'])
def telegram_link_start(message):
    trx_vol = bot.send_message(message.chat.id, 'How big was the expense?',
                               reply_markup=types.ForceReply(selective=False))
    bot.register_next_step_handler(trx_vol, define_creditor)


def define_creditor(message):
    try:
        float(message.text)
        trx = Trx(full_amount=message.text, debtors_id=[])
        user_ids = bot.send_message(message.chat.id, 'Who is the creditor?', reply_markup=keyboard_with_users())
        bot.register_next_step_handler(user_ids, lambda msg: define_trx_name(trx, msg))
    except Exception:
        trx_vol = bot.send_message(message.chat.id, 'That is not a valid sum. Please enter a correct one.',
                                   reply_markup=types.ForceReply(selective=False))
        bot.register_next_step_handler(trx_vol, define_creditor)


def define_trx_name(trx, message):
    trx.creditor_id = server_conn('get_id_from_username', message.text)
    trx_name = bot.send_message(message.chat.id, 'What is the transaction about?',
                                reply_markup=types.ForceReply(selective=False))
    bot.register_next_step_handler(trx_name, lambda msg: define_split_type(trx, msg))


def define_split_type(trx, message):
    trx.trx_name = message.text
    keyboard = types.ReplyKeyboardMarkup()
    splits = ['Equal split']
    for split in splits:
        keyboard.add(types.InlineKeyboardButton(split, callback_data=split))
    split_type = bot.send_message(message.chat.id, 'How would you like to split?', reply_markup=keyboard)
    bot.register_next_step_handler(split_type, lambda msg: process_transaction_split(trx, msg))


def process_transaction_split(trx, message, split_type=None):
    # dic['split_type'] = message
    if split_type == 'Equal split' or message.text == 'Equal split':
        keyboard = keyboard_with_users(exclude_users=trx.debtors_id, add_nobody=True)
        split_member = bot.send_message(message.chat.id,
                                        'Who would you like to include? Select "Nobody" to end allocation',
                                        reply_markup=keyboard)  # Todo Will need to replace "Nobody" with some shit otherwise such a username will break everything
        bot.register_next_step_handler(split_member, lambda msg: add_member_to_split(trx, msg))


def add_member_to_split(trx, message):
    print('TEXT', message.text)
    if message.text == '###Nobody':
        server_conn('new_trx_with_equal_split', trx)

        bot.send_message(message.chat.id, '''{0}'s transaction of {1} has been equally split among {2}.'''.format(
            server_conn('get_username_from_id', trx.creditor_id), trx.full_amount,
            ', '.join(server_conn('get_username_from_id', i) for i in trx.debtors_id)),
                         reply_markup=types.ReplyKeyboardRemove())
    else:
        trx.debtors_id = trx.debtors_id.append(message.text)
        process_transaction_split(trx, split_type='Equal split')


def keyboard_with_users(group=None, exclude_users=[], add_nobody=False):  # todo add option to add a transaction name
    keyboard = types.ReplyKeyboardMarkup()
    usernames = list_users()
    for username in usernames:
        if len(exclude_users) > 0 and username in exclude_users:
            pass
        else:
            keyboard.add(types.InlineKeyboardButton(username, callback_data=username))
    if add_nobody:
        keyboard.add(types.InlineKeyboardButton('Nobody', callback_data='###Nobody'))
    return keyboard


while True:
    try:
        bot.polling()
    except Exception as e:
        print(e)
        print('Error!!! Falling to sleep for 60 seconds...')
        time.sleep(60)
