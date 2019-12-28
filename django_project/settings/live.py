import os

from .base import *  # noqa
from .base import ALLOWED_HOSTS, DATABASES

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

SECRET_KEY = os.environ["SECRET_KEY"]
ALLOWED_HOSTS += ["live.zrpamaf6iq.ap-northeast-2.elasticbeanstalk.com"]

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

OAUTH_ACCESS_TOKEN = os.environ["OAUTH_ACCESS_TOKEN"]
BOTUSER_OAUTH_ACCESS_TOKEN = os.environ["BOTUSER_OAUTH_ACCESS_TOKEN"]
