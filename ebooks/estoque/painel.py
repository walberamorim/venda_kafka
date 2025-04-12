from kafka import KafkaConsumer, TopicPartition
from time import sleep
import json

if __name__ == "__main__":
    painel = KafkaConsumer(bootstrap_servers = ["kafka:29092"], api_version=(0, 10, 1), auto_offset_reset="earliest", consumer_timeout_ms=1000)

    topico = TopicPartition("estoque", 0)
    painel.assign([topico])
    painel.seek(topico, 0)
    
    while True:
        for venda in painel:
            dados = json.loads(venda.value)
            print(f"dados da venda: {dados}")
    
        sleep(5)

