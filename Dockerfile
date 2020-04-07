FROM python:3

MAINTAINER Your Name "youremail@example.com"

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN apt update -y && apt install -y argus-client

RUN pip install -r requirements.txt

COPY . /app

CMD gunicorn --bind 0.0.0.0:$PORT app:app
