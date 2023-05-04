
class Emoji:
    cross = '\U00002716'
    check = '\U00002714'
    red_cross = '\U0000274C'


class Reply:
    ok = f'{Emoji.check} Done {Emoji.check}'
    help = f'{Emoji.cross} There is no help, lol {Emoji.cross}'
    prompt = 'Select one of available system prompts:'
    model = 'Select one of available gpt models:'
    clear_dialog = f'{Emoji.check} Your current dialog has been cleared {Emoji.check}'
    empty_dialog = f'{Emoji.check} Your have no active dialog {Emoji.check}'


def print_error(text_error: str) -> str:
    return f'{Emoji.red_cross} Error: {text_error} {Emoji.red_cross}'
