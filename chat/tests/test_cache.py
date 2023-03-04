from app.messages import Chat, Message, Role
from app.cache import SimpleCache


def test_cache():
    
    cache = SimpleCache()

    key = '123'
    message = 'HELLO'

    history = Chat()
    history.add(Message(role=Role.USER, text=message))

    cache.set(key=key, value=history)
    cached_history = cache.get(key=key)

    assert history == cached_history
