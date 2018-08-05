def get_settings():
    {% if settings == 'dummy' %}return {
        'db': {
            'user': 'root',
            'db': 'yak',
            'host': '127.0.0.1',
            'password': '123',
            'autocommit': True,
            'charset': 'utf8'
        },
        'cors': {
            '*': {
                'allow_credentials': True,
                'expose_headers': "*",
                'allow_headers': "*"
            }
        }
    }{% endif %}
