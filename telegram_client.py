import telebot

bot = telebot.TeleBot('1012372350:AAG7N6oZPE5mi9uLSsNwwvN2fZhHEJRlNVk')

print('Bot started')

@bot.message_handler(content_types=['text'])
def reply(message):
    print(message)
    bot.reply_to(message, 'Das is text')

@bot.message_handler(content_types=['contact'])
def reply(message):
    print(message)
    bot.reply_to(message, 'Das is contact')

while True:
    bot.polling()
