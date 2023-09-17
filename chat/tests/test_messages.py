from app.messages import Chat, Message, Model, Role


def test_empty_chat():
    
    history = Chat()
    assert history.status['messages'] == 0
    assert history.status['prompt'] == 'prompt_default'


def test_chat():
    
    init_message = 'HELLO'
    answ_message = 'THERE'
    tokens = {"total_token": 100}

    history = Chat()
    history.add(Message(role=Role.USER, text=init_message, tokens={}))
    history.add(Message(role=Role.ASSISTANT, text=answ_message, tokens=tokens))

    assert history.list[1:] == [{"role": "user", "content": "HELLO"}, {"role": "assistant", "content": "THERE"}]
    assert history.status['messages'] == 2
    assert history.status['first'] == init_message
    assert history.status['prompt'] == 'prompt_default'
    assert history.status['model'] == Model.GPT_3_5
    assert history.status['tokens'] == tokens
