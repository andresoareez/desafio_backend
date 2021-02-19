FROM python:3-alpine
MAINTAINER andresoareez

WORKDIR /app
COPY . /app

RUN pip install dnspython
RUN pip install -r requirements.txt

EXPOSE 5000