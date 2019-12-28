from .base import *  # noqa
from .base import ALLOWED_HOSTS, DATABASES

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "!ws5-pn3ggc3niw_69hxxbz**f%twy7!facs9ffhl2i$==lch*"

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

ALLOWED_HOSTS += ["*"]

DATABASES["default"].update(
    {
        "HOST": "deadlift.cmsiwsufhcwm.ap-northeast-2.rds.amazonaws.com",
        "PORT": "5432",
        "USER": "postgres",
        "PASSWORD": "8GbgKTirA0KMaZJlQwNk",
    }
)

OAUTH_ACCESS_TOKEN = (
    "xoxp-3524262641-428073641093-890438398646-3da9bd75a14f56fd34d1a965a836c968"
)
BOTUSER_OAUTH_ACCESS_TOKEN = "xoxb-3524262641-888144356261-kuWe6Lfx4FmL9Ix0rDQIfVhX"
SIG_HEALTH_CHANNEL = "CRR629M3L"
