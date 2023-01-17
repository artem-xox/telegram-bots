import logging

import telebot
import openai

import settings


logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

bot = telebot.TeleBot(settings.BOT_API_KEY)
openai.api_key = settings.OPENAI_API_KEY


bot.infinity_polling()
