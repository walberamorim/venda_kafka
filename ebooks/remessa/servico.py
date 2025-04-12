from flask_apscheduler import APScheduler
from time import sleep
from kafka import KafkaProducer, KafkaClient, KafkaConsumer, TopicPartition
import random
import json

PROCESSO = 'estoque'
PROCESSO_ANTERIOR = 'ebook'

def iniciar():
    iniciado = False

    try:
        cliente = KafkaClient(bootstrap_servers=["kafka:29092"], api_version=(0, 10, 1))
        cliente.add_topic(PROCESSO)
        cliente.close()
        iniciado = True

    except Exception as e:
        print(f"Erro iniciando/configurando o kafka: {e}")
    return iniciado


def validar_dados(dados):
    ...
offset = 0
def executar():
    consumidor = KafkaConsumer(bootstrap_servers=["kafka:29092"],
        api_version=(0, 10, 1), 
        auto_offset_reset="earliest", 
        consumer_timeout_ms=1000)
    topico = TopicPartition(PROCESSO_ANTERIOR, 0)
    consumidor.assign([topico])
    consumidor.seek(topico, offset)

    
    produtor = KafkaProducer(bootstrap_servers=["kafka:29092"],
        api_version=(0, 10, 1))

    for dados in consumidor:
        offset = dados.offset + 1
        validos, mensagem = validar_dados(dados)
        #simulando um processo de estoque
        sleep(2)

        if validos:
            dados['sucesso'] = 1
        else:
            dados['sucesso'] = 0
        dados['mensagem'] = mensagem

        produtor.send(topic=PROCESSO, value=json.dumps(dados).encode('utf-8'))
    produtor.flush()
    produtor.close()

if __name__ == "__main__":
    if iniciar():
        servico = APScheduler()
        servico.add_job(id=PROCESSO, func=executar, trigger="interval", seconds=4)
        servico.start()

        while True:
            sleep(60)