import telebot
import requests
import time
from telebot import types
from telebot.apihelper import ApiException
from core import server_conn
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
            pass
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


# @bot.message_handler(content_types=['text'])
# def reply(message):
#     bot.reply_to(message, 'Das is text')





# {'content_type': 'text',
#  'message_id': 8,
#  'from_user':
#      {'id': 278810318,
#       'is_bot': False,
#       'first_name': 'Stanislav',
#       'username': 'JustStas',
#       'last_name': None,
#       'language_code': 'ru'},
#  'date': 1591723973,
#  'chat': {'type': 'private',
#           'last_name': None,
#           'first_name': 'Stanislav',
#           'username': 'JustStas',
#           'id': 278810318,
#           'title': None,
#           'all_members_are_administrators': None,
#           'photo': None,
#           'description': None,
#           'invite_link': None,
#           'pinned_message': None,
#           'sticker_set_name': None,
#           'can_set_sticker_set': None},
#  'forward_from': None,
#  'forward_from_chat': None,
#  'forward_from_message_id': None,
#  'forward_signature': None,
#  'forward_date': None,
#  'reply_to_message': None,
#  'edit_date': None,
#  'media_group_id': None,
#  'author_signature': None,
#  'text': 'Олег 🐔',
#  'entities': None,
#  'caption_entities': None,
#  'audio': None,
#  'document': None,
#  'photo': None,
#  'sticker': None,
#  'video': None,
#  'video_note': None,
#  'voice': None,
#  'caption': None,
#  'contact': None,
#  'location': None,
#  'venue': None,
#  'animation': None,
#  'dice': None,
#  'new_chat_member': None,
#  'new_chat_members': None,
#  'left_chat_member': None,
#  'new_chat_title': None,
#  'new_chat_photo': None,
#  'delete_chat_photo': None,
#  'group_chat_created': None,
#  'supergroup_chat_created': None,
#  'channel_chat_created': None,
#  'migrate_to_chat_id': None,
#  'migrate_from_chat_id': None,
#  'pinned_message': None,
#  'invoice': None,
#  'successful_payment': None,
#  'connected_website': None,
#  'json': {'message_id': 8,
#           'from': {'id': 278810318,
#                    'is_bot': False,
#                    'first_name': 'Stanislav',
#                    'username': 'JustStas',
#                    'language_code': 'ru'},
#           'chat': {'id': 278810318,
#                    'first_name': 'Stanislav',
#                    'username': 'JustStas',
#                    'type': 'private'},
#           'date': 1591723973,
#           'text': 'Олег 🐔',
#           'entities': [{'offset': 0,
#                         'length': 7,
#                         'type': 'text_mention',
#                         'user': {'id': 327154479,
#                                  'is_bot': False,
#                                  'first_name': 'Oleg',
#                                  'last_name': 'Dylevich'}}]}}


while True:
    try:
        bot.polling()
    except Exception as e:
        print(e)
        print('Error!!! Falling to sleep for 15 seconds...')
        time.sleep(15)
