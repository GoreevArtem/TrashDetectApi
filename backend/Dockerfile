FROM tiangolo/uvicorn-gunicorn:latest

# set work directory
WORKDIR /api

# set .env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

RUN apt-get update && apt-get install -y htop libgl1-mesa-glx libglib2.0-0

# install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

RUN pip install ultralytics

# copy project
COPY . .