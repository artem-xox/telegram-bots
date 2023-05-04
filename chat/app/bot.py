import logging

import telebot
import openai

from app.cache import SimpleCache
from app.content.responses import Reply, print_error
from app.content.prompts import PromptsMap, prompt_markup
from app.messages import Chat, Message, Role, ActiveModels, model_markup
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


@bot.message_handler(commands=['prompt'])
def prompt(message):
    bot.send_message(message.chat.id, Reply.prompt, reply_markup=prompt_markup())


@bot.message_handler(commands=['model'])
def prompt(message):
    bot.send_message(message.chat.id, Reply.model, reply_markup=model_markup())


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    
    history = cache.get(call.message.chat.id)
    if history is None:
        history = Chat()
    
    if call.data in PromptsMap:
        prompt = PromptsMap[call.data]
        history.set_prompt(prompt)
        bot.send_message(call.message.chat.id, prompt.message)
    elif call.data in ActiveModels:
        history.model = call.data
        bot.send_message(call.message.chat.id, Reply.ok)
    else:
        pass
    
    cache.set(call.message.chat.id, history)

@bot.message_handler(func=lambda message: True)
def chat(message):
    
    history = cache.get(message.chat.id)
    if history is None:
        history = Chat()
    
    history.add(Message(role=Role.USER, text=message.text))

    try:        
        response = openai.ChatCompletion.create(
            model=history.model,
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
