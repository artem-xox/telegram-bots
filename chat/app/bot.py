import logging

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import openai

from app.cache import SimpleCache
from app.content.responses import Reply, print_error
from app.content.prompts import DefaultStyle, SimpleStyle
from app.messages import Chat, Message, Role
from app import settings


logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

bot = telebot.TeleBot(settings.BOT_API_KEY)
openai.api_key = settings.OPENAI_API_KEY


cache = SimpleCache()


@bot.message_handler(commands=['status'])
def status(message):
    history = cache.get(message.chat.id)
    if history:
        bot.send_message(message.chat.id, text=str(history.status))
    else:
        bot.send_message(message.chat.id, text=Reply.empty_dialog)


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, text=Reply.help)


@bot.message_handler(commands=['clear'])
def clear(message):
    res = cache.delete(message.chat.id)
    if res:
        bot.send_message(message.chat.id, text=Reply.clear_dialog)
    else:
        bot.send_message(message.chat.id, text=Reply.empty_dialog)


def style_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("Default", callback_data="default_style"),
        InlineKeyboardButton("Simple", callback_data="simple_style"))
    return markup


@bot.message_handler(commands=['style'])
def style(message):
    bot.send_message(message.chat.id, "What style of conversation do you prefer?", reply_markup=style_markup())


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    
    history = cache.get(call.message.chat.id)
    if history is None:
        history = Chat()
    
    if call.data == "default_style":
        bot.send_message(call.message.chat.id, Reply.set_style_default)
        history.set_style(DefaultStyle)
    elif call.data == "simple_style":
        history.set_style(SimpleStyle)
        bot.send_message(call.message.chat.id, Reply.set_style_simple)
    
    cache.set(call.message.chat.id, history)

@bot.message_handler(func=lambda message: True)
def chat(message):
    
    history = cache.get(message.chat.id)
    if history is None:
        history = Chat()
    
    history.add(Message(role=Role.USER, text=message.text))

    try:        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=history.list
        )
        response_text = response["choices"][0]["message"]["content"]
        
        history.add(Message(role=Role.ASSISTANT, text=response_text))
        bot.reply_to(message, text=response_text, parse_mode="Markdown")
        cache.set(message.chat.id, history)

    except Exception as error:
        logger.error(error)
        bot.reply_to(message, text=print_error(error.args[0]))


bot.infinity_polling()
