from dataclasses import dataclass, field

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


@dataclass
class Prompt:
    name: str
    text: str
    message: str = field(init=False)

    def __post_init__(self):
        self.message = f'The model starts with system prompt `{self.text}`'


DefaultPrompt = Prompt(name='prompt_default', text='You are a helpful assistant.')

Prompts = [
    Prompt(name='prompt_default', text='You are a helpful assistant.'),
    Prompt(name='prompt_explain', text='Explain everything in a very simple and accessible way.'),
    Prompt(name='prompt_rephrase', text='Rephrase all my messages into a more appropriate and grammatically correct form. Answer only by paraphrased sentences without any additional information.'),
    Prompt(name='prompt_debug', text='Find all errors and bugs in my code. Attempt to clarify each mistake in a stepwise manner.'),
]

PromptsMap = {
    _.name: _ for _ in Prompts   
}


def prompt_markup():
    markup = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Default", callback_data="prompt_default"),
            InlineKeyboardButton("Explain", callback_data="prompt_explain")
        ],
        [
            InlineKeyboardButton("Rephrase", callback_data="prompt_rephrase"), 
            InlineKeyboardButton("Debug", callback_data="prompt_debug"),
        ]
    ])
    return markup