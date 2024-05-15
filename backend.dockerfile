FROM python:3.10-slim as base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY . .

RUN pip3 install poetry
RUN poetry export --without-hashes --format=requirements.txt > requirements.txt
RUN pip3 install -r requirements.txt

EXPOSE 8000
