import logging

import emoji
import telebot
import openai

import settings


logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)


bot = telebot.TeleBot(settings.BOT_API_KEY)
openai.api_key = settings.OPENAI_API_KEY


@bot.message_handler(func=lambda message: True)
def get_codex(message):
    
    try:
        response = openai.Completion.create(
            engine="code-davinci-001",
            prompt='"""\n{}\n"""'.format(message.text),
            temperature=0,
            max_tokens=1200,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=['"""'])
        
        answer = response["choices"][0]["text"]
        if len(answer) > settings.MAX_LETTERS:
            for x in range(0, len(answer), settings.MAX_LETTERS):
                bot.reply_to(
                    message, 
                    text=f'```python\{answer[x:x+settings.MAX_LETTERS]}```', parse_mode="Markdown")
        else:
            bot.reply_to(
                message, text=f'```python\{answer}\```', parse_mode="Markdown")

    except Exception as error:
        logger.error(error.args[0])
        bot.reply_to(
            message, text=f"\U0000274C Error: {error.args[0]} \U0000274C")


bot.infinity_polling()
