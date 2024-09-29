ARG TAG=latest
FROM python:$TAG

RUN groupadd --gid 1000 app \
    && useradd --uid 1000 --gid 1000 --shell /bin/bash --create-home app

RUN mkdir /opt/app/ \
    && chown app:app /opt/app/

WORKDIR /opt/app/
COPY ./requirements.txt .

USER app

RUN python3 -m venv .venv \
    && ./.venv/bin/python3 -m pip install -r ./requirements.txt

COPY . .

ENTRYPOINT ["./.venv/bin/python3", "./main.py"]
