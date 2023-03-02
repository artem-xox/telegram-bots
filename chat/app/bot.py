import logging

import telebot
import openai

import settings


logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

bot = telebot.TeleBot(settings.BOT_API_KEY)
openai.api_key = settings.OPENAI_API_KEY


@bot.message_handler(func=lambda message: True)
def get_chat(message):
    
    try:        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": message.text}
            ]
        )
        logger.info(response)
        bot.reply_to(message, text=response["choices"][0]["message"]["content"], parse_mode="Markdown")
    
    except Exception as error:
        logger.error(error.args[0])
        bot.reply_to(
            message, text=f"\U0000274C Error: {error.args[0]} \U0000274C")


bot.infinity_polling()
