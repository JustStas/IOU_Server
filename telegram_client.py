import telebot

bot = telebot.TeleBot('1012372350:AAG7N6oZPE5mi9uLSsNwwvN2fZhHEJRlNVk')

print('Bot started')

@bot.message_handler(content_types=['text'])
def reply(message):
    bot.reply_to(message, 'Das is reply')

while True:
    bot.polling()
