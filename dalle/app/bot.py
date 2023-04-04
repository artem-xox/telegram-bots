import logging

import telebot
from telebot.types import InputMediaPhoto
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
            n=settings.MEDIA_SIZE,
            size=settings.RESOLUTION_HIGH
        )
        image_urls = [response['data'][i]['url'] for i in range(settings.MEDIA_SIZE)]
        media = [InputMediaPhoto(image) for image in image_urls]
        bot.send_media_group(chat_id=message.chat.id, media=media)
    
    except Exception as error:
        logger.error(error.args[0])
        bot.reply_to(
            message, text=f"\U0000274C Error: {error.args[0]} \U0000274C")


bot.infinity_polling()
