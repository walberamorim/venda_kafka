from flask_apscheduler import APScheduler
from time import sleep
import json

from kafka import KafkaClient, KafkaConsumer, KafkaProducer, TopicPartition

PROCESSO = "pagamento"
PROCESSO_ANTERIOR = "estoque"

def iniciar():
    global offset
    offset = 0

    iniciado = False

    try:
        cliente = KafkaClient(bootstrap_servers = ["kafka:29092"], api_version=(0, 10, 1))
        cliente.add_topic(PROCESSO)
        cliente.close()

        iniciado = True
    except Exception as e:
        print(f"erro iniciando/configurando o kafka: {str(e)}")

    return iniciado

def validar_dados(dados):
    validos, mensagem = (dados["sucesso"] == 1), "Pagamento confirmado!!",

    sleep(2) # simula um processamento do pagamento

    if validos:
        mensagem = "Pagamento confirmado!!"
    else:
        mensagem = "Erro no pagamento!!"

    return validos, mensagem

def executar():
    global offset

    consumidor = KafkaConsumer(
        bootstrap_servers=["kafka:29092"],
        auto_offset_reset="earliest", 
        consumer_timeout_ms=1000,
        group_id=PROCESSO, 
        api_version=(0, 10, 1))

    topico = TopicPartition(PROCESSO_ANTERIOR, 0)
    consumidor.assign([topico])
    consumidor.seek(topico, offset)

    produtor = KafkaProducer(bootstrap_servers=["kafka:29092"], api_version=(0, 10, 1))

    for dados in consumidor:
        offset = dados.offset + 1

        dados = json.loads(dados.value)
        validos, mensagem = validar_dados(dados)
        if validos:
            dados["sucesso"] = 1
        else:
            dados["sucesso"] = 0
        dados["mensagem"] = mensagem

        produtor.send(topic=PROCESSO, value=json.dumps(dados).encode("utf-8"))

    produtor.flush()
    produtor.close()

    consumidor.close()

if __name__ == "__main__":
    if iniciar():
        servico = APScheduler()
        servico.add_job(id=PROCESSO, func=executar, trigger="interval", seconds = 4)
        servico.start()

        while True:
            sleep(60)

