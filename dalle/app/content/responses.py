
class Emoji:
    cross = '\U00002716'
    check = '\U00002714'
    red_cross = '\U0000274C'
    sparkles = '\U00002728'


class Reply:
    welcome = f'{Emoji.sparkles} Hello there'
    ok = f'{Emoji.check} Done'
    help = f'{Emoji.cross} There is no help, lol'
    model = f' {Emoji.check} Select one of available dall-e models:'
    # size = f' {Emoji.check} Select one of available sizes for image generating:'
    size = f' {Emoji.cross} Not ready yet'
    restriction = f'{Emoji.cross} Hi! It looks like you are not allowed to use this bot! Have a nice day :)'


def print_error(text_error: str) -> str:
    return f'{Emoji.red_cross} Error: {text_error}'

def print_model(model: str) -> str:
    return f'{Emoji.check} Your current model is *{model}*'
