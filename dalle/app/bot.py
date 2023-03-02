import logging

import telebot
import openai

import settings


logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

bot = telebot.TeleBot(settings.BOT_API_KEY)
openai.api_key = settings.OPENAI_API_KEY


@bot.message_handler(func=lambda message: True)
def get_dalle(message):
    
    try:

        response = openai.Image.create(
            prompt=message.text,
            n=1,
            size="1024x1024"
        )
        image_url = response['data'][0]['url']
        bot.send_photo(
            chat_id=message.chat.id, photo=image_url
        )

    except Exception as error:
        logger.error(error.args[0])
        bot.reply_to(
            message, text=f"\U0000274C Error: {error.args[0]} \U0000274C")


bot.infinity_polling()
