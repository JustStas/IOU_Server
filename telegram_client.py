import telebot

bot = telebot.TeleBot('1012372350:AAG7N6oZPE5mi9uLSsNwwvN2fZhHEJRlNVk')

print('Bot started')

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    print('Incoming')
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(content_types=['text'])
def reply(message):
    print(message)
    bot.reply_to(message, 'Das is text')





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



bot.polling()
