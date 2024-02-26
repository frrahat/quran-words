FROM python:3.9-alpine
RUN apk add build-base

WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
