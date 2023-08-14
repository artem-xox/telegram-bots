
class Emoji:
    cross = '\U00002716'
    check = '\U00002714'
    red_cross = '\U0000274C'
    sparkles = '\U00002728'


class Reply:
    welcome = f'{Emoji.sparkles} Hello there {Emoji.sparkles}'
    ok = f'{Emoji.check} Done {Emoji.check}'
    help = f'{Emoji.cross} There is no help, lol {Emoji.cross}'
    prompt = f'{Emoji.check} Select one of available system prompts: {Emoji.check}'
    model = f' {Emoji.check} Select one of available gpt models: {Emoji.check}'
    clear_dialog = f'{Emoji.check} Your current dialog has been cleared {Emoji.check}'
    empty_dialog = f'{Emoji.check} You don\'t have any active dialogs {Emoji.check}'
    restriction = f'{Emoji.cross} Hi! It looks like you are not allowed to use this bot! Have a nice day :) {Emoji.cross}'


def print_error(text_error: str) -> str:
    return f'{Emoji.red_cross} Error: {text_error} {Emoji.red_cross}'
