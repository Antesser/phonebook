FROM python:3.12

RUN mkdir -p /phone_data

WORKDIR /phone_data

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .
