from kafka import TopicPartition, KafkaConsumer
from time import sleep
import json

PROCESSO = "ebook"

if __name__ == "__main__":
    painel = KafkaConsumer(
        bootstrap_servers=["kafka:29092"],
        api_version=(0, 10, 1),
        auto_offset_reset="earliest",
        consumer_timeout_ms=1000)
    
    topico = TopicPartition(PROCESSO, 0)
    painel.assign([topico])
    painel.seek_to_beginning(topico)

    print("Iniciando o painel..." + str(painel.assignment()))

    while True:
        for venda in painel:
            dados = json.loads(venda.value.decode("utf-8"))
            print(f"Dados da venda: {dados}")
        sleep(5)