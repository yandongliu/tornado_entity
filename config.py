
_obj = {
    'database.username': 'tornado_entity_user',
    'database.password': 'qwerty',
    'database.database': 'tornado_entity',
    'database.url': 'postgresql://tornado_entity_user:qwerty@localhost:5432/tornado_entity',
}

def load():
    pass

def get(key):
    return _obj.get(key)
