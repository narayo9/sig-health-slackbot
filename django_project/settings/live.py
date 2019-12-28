from .base import *  # noqa
from .base import DATABASES, os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

SECRET_KEY = os.environ["SECRET_KEY"]


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES["default"].update(
    {
        "HOST": os.environ["DATABASE_HOST"],
        "PORT": os.environ["DATABASE_PORT"],
        "USER": os.environ["DATABASE_USER"],
        "PASSWORD": os.environ["DATABASE_PASSWORD"],
    }
)
