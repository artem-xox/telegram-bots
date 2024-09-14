from dataclasses import dataclass

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


@dataclass
class Price:
    input: float
    output: float


@dataclass
class Model:
    name: str
    price: Price


GPT_4o_mini = Model(
    name="gpt-4o-mini",
    price=Price(input=0.03, output=0.06),
)

GPT_4o = Model(
    name="gpt-4o",
    price=Price(input=0.03, output=0.06),
)

GPT_o1_mini = Model(
    name="o1-mini",
    price=Price(input=0.03, output=0.06),
)

GPT_o1_preview = Model(
    name="o1-preview",
    price=Price(input=0.03, output=0.06),
)


ActiveModels = {
    GPT_4o_mini.name: GPT_4o_mini,
    GPT_4o.name: GPT_4o,
    GPT_o1_mini.name: GPT_o1_mini,
    GPT_o1_preview.name: GPT_o1_preview,
}


def model_markup():
    markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(GPT_4o_mini.name, callback_data=GPT_4o_mini.name),
                InlineKeyboardButton(GPT_4o.name, callback_data=GPT_4o.name),
            ],
            [
                InlineKeyboardButton(GPT_o1_mini.name, callback_data=GPT_o1_mini.name),
                InlineKeyboardButton(GPT_o1_preview.name, callback_data=GPT_o1_preview.name),
            ],
        ]
    )
    return markup
