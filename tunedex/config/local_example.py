from tunedex.config.settings import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'tunedex',
        'USER': 'you',
        'PASSWORD': 'yourpass',
        'HOST': '127.0.0.1',
        'PORT': '',
    }
}

LIBRARY_PATH = "/Users/you/Music/iTunes/iTunes Music Library.xml"

SECRET_KEY = 'klsdf8**2s9whnsls8*2JHs'
