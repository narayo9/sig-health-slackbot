from .base import *  # noqa
from .base import DATABASES

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "!ws5-pn3ggc3niw_69hxxbz**f%twy7!facs9ffhl2i$==lch*"

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES["default"].update(
    {
        "HOST": "deadlift.cmsiwsufhcwm.ap-northeast-2.rds.amazonaws.com",
        "PORT": "5432",
        "USER": "postgres",
        "PASSWORD": "8GbgKTirA0KMaZJlQwNk",
    }
)
