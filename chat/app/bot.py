import json
import logging
from functools import wraps

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


@bot.message_handler(commands=['status'])
@restrict
def status(message):
    history = cache.get(message.chat.id)
    if history is None:
        history = Chat()

    history_status_json = json.dumps(history.status, indent=4)
    bot.send_message(message.chat.id, text=history_status_json)


@bot.message_handler(commands=['help'])
@restrict
def help(message):
    bot.send_message(message.chat.id, text=Reply.help)


@bot.message_handler(commands=['clear'])
@restrict
def clear(message):
    res = cache.delete(message.chat.id)
    if res:
        bot.send_message(message.chat.id, text=Reply.clear_dialog)
    else:
        bot.send_message(message.chat.id, text=Reply.empty_dialog)


@bot.message_handler(commands=['prompt'])
@restrict
def prompt(message):
    bot.send_message(message.chat.id, Reply.prompt, reply_markup=prompt_markup())


@bot.message_handler(commands=['model'])
@restrict
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
@restrict
@send_action('typing')
def chat(message):
    
    history = cache.get(message.chat.id)
    if history is None:
        history = Chat()
    
    history.add(Message(role=Role.USER, text=message.text, tokens={}))

    try:        
        response = openai.ChatCompletion.create(
            model=history.model,
            messages=history.list
        )
        response_text = response["choices"][0]["message"]["content"]
        tokens_dict = response["usage"]

        history.add(Message(role=Role.ASSISTANT, text=response_text, tokens=tokens_dict))
        bot.reply_to(message, text=response_text, parse_mode="Markdown")
        cache.set(message.chat.id, history)

    except Exception as error:
        logger.error(error)
        try:
            bot.reply_to(message, text=response_text, parse_mode="HTML")
            cache.set(message.chat.id, history)
        except Exception as error:
            logger.error(error)
            bot.reply_to(message, text=print_error(error.args[0]))


bot.infinity_polling()
