import logging
from functools import wraps

import telebot
from telebot.types import InputMediaPhoto
from openai import OpenAI

from app.content.responses import Reply, print_error
from app.client import OpenAIClient, RequestPayload
from app import settings


logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

bot = telebot.TeleBot(settings.BOT_API_KEY)

# https://platform.openai.com/docs/guides/images
# response = client.images.generate(
#     prompt=message.text,
#     size=settings.RESOLUTION_LOW,
#     n=1,
# )
client = OpenAI(api_key=settings.OPENAI_API_KEY)
custom_client = OpenAIClient(api_key=settings.OPENAI_API_KEY)


def send_action(action):
    def decorator(func):
        @wraps(func)
        def command_func(message, *args, **kwargs):
            bot.send_chat_action(chat_id=message.chat.id, action=action)
            return func(message,  *args, **kwargs)
        return command_func
    return decorator


def restrict(func):
    @wraps(func)
    def wrapped(message, *args, **kwargs):
        username = message.chat.username
        if username not in settings.WHITELIST:
            bot.send_message(message.chat.id, text=Reply.restriction)
            return
        return func(message, *args, **kwargs)
    return wrapped


@bot.message_handler(commands=['start'])
@restrict
def start(message):
	bot.send_message(message.chat.id, Reply.welcome)


@bot.message_handler(commands=['help'])
@restrict
def help(message):
    bot.send_message(message.chat.id, text=Reply.help)


@bot.message_handler(commands=['size'])
@restrict
def size(message):
    bot.send_message(message.chat.id, text=Reply.size)


# todo: https://platform.openai.com/docs/guides/rate-limits/rate-limits
@bot.message_handler(func=lambda message: True)
@restrict
@send_action('typing')
def dalle(message):
    try:
        request = RequestPayload(
            model=settings.DALLE_3_MODEL,
            prompt=message.text,
            size=settings.RESOLUTION_LOW
        )
        response = custom_client.generate_image(
            request
        )

        media = [InputMediaPhoto(image) for image in response.urls]
        bot.send_media_group(chat_id=message.chat.id, media=media)
    
    except Exception as error:
        logger.error(error.args[0])
        bot.reply_to(message, text=print_error(error.args[0]))


bot.infinity_polling()
