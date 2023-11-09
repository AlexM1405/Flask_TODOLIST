from os import urandom

class config():
    SECRET_KEY = urandom(16)
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    MONGO_URI = "mongodb://localhost:27017/platzi_flask"