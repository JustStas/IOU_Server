import telebot

bot = telebot.TeleBot('1012372350:AAG7N6oZPE5mi9uLSsNwwvN2fZhHEJRlNVk')

# proxy
# login = 'olegdylevich'
# pwd = 'W1o7SqQ'
# ip = '89.191.230.201'
# port = '65233'
#
# telebot.apihelper.proxy = {
#     'https': 'https://{}:{}@{}:{}'.format(login, pwd, ip, port)
# }

print('Bot started')


@bot.message_handler(content_types='message')
def echo(message):
    bot.reply_to(message, 'This is a reply')

while True:
    bot.polling()