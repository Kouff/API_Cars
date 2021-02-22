FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /api_cars

COPY . /api_cars
RUN pip install -r /api_cars/requirements.txt