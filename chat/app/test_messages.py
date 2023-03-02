from app.messages import Chat, Message, Role


def test_chat():
    
    init_message = 'HELLO'
    answ_message = 'THERE'

    history = Chat()
    history.add_message(Message(role=Role.USER, text=init_message))
    history.add_message(Message(role=Role.ASSISTANT, text=answ_message))

    assert history.list == [{"role": "user", "content": "HELLO"}, {"role": "assistant", "content": "THERE"}]
