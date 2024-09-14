FROM python:3.12-slim-bullseye

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .
