import logging

import telebot
import openai

import settings
from messages import Chat, Message, Role


logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

bot = telebot.TeleBot(settings.BOT_API_KEY)
openai.api_key = settings.OPENAI_API_KEY


# todo: write cache class
cache = {

}


# todo: moved replics and emojis in one place
@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, text='\U00002716 There is no help, lol \U00002716')


@bot.message_handler(commands=['clear'])
def clear(message):
    chat_id = message.chat.id
    if chat_id in cache:
        cache.pop(message.chat.id)
        bot.send_message(message.chat.id, text='\U00002714 Your current dialog has been cleared \U00002714')
    else:
        bot.send_message(message.chat.id, text='\U00002714 Your have no active dialog \U00002714')


@bot.message_handler(func=lambda message: True)
def chat(message):
    
    history = cache.get(message.chat.id)
    if history is None:
        history = Chat()
    
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
        logger.error(error.args[0])
        bot.reply_to(
            message, text=f"\U0000274C Error: {error.args[0]} \U0000274C")


bot.infinity_polling()
