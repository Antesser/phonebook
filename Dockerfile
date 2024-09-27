FROM python:3.12

RUN mkdir -p /phonebook

WORKDIR /phonebook

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .
