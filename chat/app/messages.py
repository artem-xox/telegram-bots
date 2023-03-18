# Typically, a conversation is formatted with a system message first, 
#   followed by alternating user and assistant messages.
# The system message helps set the behavior of the assistant. 
#   In the example above, the assistant was instructed with “You are a helpful assistant.”
# The user messages help instruct the assistant. 
#   They can be generated by the end users of an application, or set by a developer as an instruction.
# The assistant messages help store prior responses. 
#   They can also be written by a developer to help give examples of desired behavior.

from dataclasses import dataclass, field
from typing import List, Dict

from app.content.prompts import Prompt, DefaultPrompt


class Role:
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


@dataclass
class Message:
    text: str
    role: str

    def __dict__(self) -> Dict:
        return dict(role=self.role, content=self.text)


@dataclass
class Chat:
    messages: List[Message] = field(init=False, default_factory=list)
    prompt: Prompt = field(default=DefaultPrompt)
        
    def add(self, message: Message):
        self.messages.append(message)

    def clean(self):
        self.messages = []
    
    def set_prompt(self, prompt: Prompt):
        self.prompt = prompt
        self.clean()
        self.messages.append(Message(role=Role.SYSTEM, text=prompt.text))

    @property
    def list(self) -> List[Dict]:
        return [message.__dict__() for message in self.messages]

    @property
    def status(self) -> Dict:
        return dict(
            prompt=self.prompt.name, 
            messages=len(self.messages) - 1, 
            first=self.messages[1].text if len(self.messages) > 1 else "")
    
    def __post_init__(self):
        # setting default conversation prompt
        self.messages.append(Message(role=Role.SYSTEM, text=self.prompt.text))