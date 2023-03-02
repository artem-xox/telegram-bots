FROM python:3.9-slim

RUN apt-get clean \
    && apt-get -y update \
    && apt-get -y install pip

COPY poetry.lock pyproject.toml ./
RUN pip install poetry
RUN poetry install --no-dev

WORKDIR /opt
COPY ./app ./app/

CMD ["poetry", "run", "python3", "app/bot.py"]