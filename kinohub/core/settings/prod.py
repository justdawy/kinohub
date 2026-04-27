from decouple import Csv

from .base import *

DEBUG = TEMPLATE_DEBUG = False

DATABASE_CONN_MAX_AGE = 600
DATABASES["default"]["CONN_MAX_AGE"] = DATABASE_CONN_MAX_AGE

SECRET_KEY = config("SECRET_KEY")

ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())

PROXY_URL = config("PROXY_URL")
MEDIAFILES_LOCATION = "media"

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

CSRF_TRUSTED_ORIGINS = ["http://127.0.0.1:1337"]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "mediafiles"
