import logging

import telebot
import openai

from cache import SimpleCache
from content.responses import Reply, print_error
from content.prompts import SystemPrompt
from messages import Chat, Message, Role
import settings


logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

bot = telebot.TeleBot(settings.BOT_API_KEY)
openai.api_key = settings.OPENAI_API_KEY


# cache = SimpleCache
cache = {

}


# todo: this
@bot.message_handler(commands=['status'])
def status(message):
    bot.send_message(message.chat.id, text="dialog status will be here")


# todo: style changing
@bot.message_handler(commands=['style'])
def status(message):
    bot.send_message(message.chat.id, text="dialog style changing will be here")


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, text=Reply.help)


@bot.message_handler(commands=['clear'])
def clear(message):
    chat_id = message.chat.id
    if chat_id in cache:
        cache.pop(message.chat.id)
        bot.send_message(message.chat.id, text=Reply.clear_dialog)
    else:
        bot.send_message(message.chat.id, text=Reply.empty_dialog)


@bot.message_handler(func=lambda message: True)
def chat(message):
    
    history = cache.get(message.chat.id)
    if history is None:
        history = Chat()
        history.set_system_message(SystemPrompt.default)
    
    history.add_message(Message(role=Role.USER, text=message.text))

    try:        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=history.list
        )
        response_text = response["choices"][0]["message"]["content"]
        
        history.add_message(Message(role=Role.ASSISTANT, text=response_text))
        bot.reply_to(message, text=response_text, parse_mode="Markdown")
        cache.update({message.chat.id: history})

    except Exception as error:
        logger.error(error)
        bot.reply_to(message, text=print_error(error.args[0]))


bot.infinity_polling()
