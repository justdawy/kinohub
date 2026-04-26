from decouple import Csv

from core.settings.base import *

DEBUG = TEMPLATE_DEBUG = False

DATABASE_CONN_MAX_AGE = 600
DATABASES["default"]["CONN_MAX_AGE"] = DATABASE_CONN_MAX_AGE

SECRET_KEY = config("SECRET_KEY")

ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())

PROXY_URL = config("PROXY_URL")
MEDIAFILES_LOCATION = "media"
