from dataclasses import dataclass


@dataclass
class StylePrompt:
    name: str
    text: str


DefaultStyle = StylePrompt(name='default', text='You are a helpful assistant.')
SimpleStyle = StylePrompt(name='simple', text='Explain everything as if to a child.')
