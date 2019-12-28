FROM python:3.8 as base

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.0.0

ENV DJANGO_SETTINGS_MODULE=django_project.settings.live

RUN pip install "poetry==$POETRY_VERSION"
RUN python -m venv /venv

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
  && poetry install --no-dev --no-interaction --no-ansi

COPY docker-entrypoint.sh ./
COPY django_project django_project/
COPY apps apps/
COPY manage.py manage.py

ARG SECRET_KEY
ARG DATABASE_HOST
ARG DATABASE_PORT
ARG DATABASE_USER
ARG DATABASE_PASSWORD

RUN python manage.py check --deploy
RUN ["chmod", "+x", "./docker-entrypoint.sh"]
EXPOSE 8000
ENTRYPOINT ["./docker-entrypoint.sh"]