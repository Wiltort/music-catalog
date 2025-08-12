FROM python:3.12-slim

WORKDIR /code

COPY requirements.txt /code/

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . /code/

EXPOSE 8000