from dataclasses import dataclass, field
from typing import List, Dict


class Role:
    USER = "user"
    ASSISTANT = "assistant"


@dataclass
class Message:
    text: str
    role: str

    def __dict__(self) -> Dict:
        return {"role": self.role, "content": self.text}


@dataclass
class Chat:
    messages: List[Message] = field(init=False, default_factory=list)
 
    def add_message(self, message: Message):
        self.messages.append(message)
    
    @property
    def list(self) -> List[Dict]:
        return [message.__dict__() for message in self.messages]

    

