from dataclasses import dataclass, field

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


@dataclass
class Price:
    input: float
    output: float


@dataclass
class Model:
    name: str
    price: Price


GPT_3_5 = Model(
    name="gpt-3.5-turbo", 
    price=Price(
        input=0.0015, 
        output=0.002),
    )

GPT_3_5_16k = Model(
    name="gpt-3.5-turbo-16k", 
    price=Price(
        input=0.003, 
        output=0.004),
    )

GPT_4 = Model(
    name="gpt-4", 
    price=Price(
        input=0.03, 
        output=0.06),
    )

ActiveModels = {
    GPT_3_5.name: GPT_3_5,
    GPT_3_5_16k.name: GPT_3_5_16k,
    GPT_4.name: GPT_4,
}


def model_markup():
    markup = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("GPT-3.5", callback_data=GPT_3_5.name),
            InlineKeyboardButton("GPT-3.5-16k", callback_data=GPT_3_5_16k.name),
        ],
        [
            InlineKeyboardButton("GPT-4", callback_data=GPT_4.name),
        ]
    ])
    return markup