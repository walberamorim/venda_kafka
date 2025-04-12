From python:latest

RUN mkdir /servicos
WORKDIR /servicos
COPY requirements.txt /servicos

RUN pip install -r /servicos/requirements.txt

RUN pip install flask flask_apscheduler Kafka-python faker requests