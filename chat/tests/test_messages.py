from app.messages import Chat, Message, Model, Role
from app.models import Model, GPT_3_5


def test_empty_chat():
    
    history = Chat()
    assert history.status['messages'] == 0
    assert history.status['prompt'] == 'default'


def test_chat():
    
    init_message = 'HELLO'
    answ_message = 'THERE'
    tokens = {"total_tokens": 200, "prompt_tokens": 100}
    expected_price = 0.0003

    history = Chat()
    history.add(Message(role=Role.USER, text=init_message, tokens={}))
    history.add(Message(role=Role.ASSISTANT, text=answ_message, tokens=tokens))

    assert history.list[1:] == [{"role": "user", "content": "HELLO"}, {"role": "assistant", "content": "THERE"}]
    assert history.status['messages'] == 2
    assert history.status['first'] == init_message
    assert history.status['prompt'] == 'default'
    assert history.status['model'] == GPT_3_5.name
    assert history.status['tokens'] == tokens
    assert history.status['price'] == expected_price
