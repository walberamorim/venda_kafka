from flask import Flask, Response, request
from kafka import KafkaClient, KafkaProducer
from kafka.errors import KafkaError

from time import sleep
import secrets
import json
import random
import string

PROCESSO = "ebook"
servico = Flask(PROCESSO)

INFO = {
    "descricao": "Serviço de venda de e-books",
    "versao": "0.0.1",
}

def iniciar():
    iniciado = False

    try:
        cliente = KafkaClient(bootstrap_servers=["kafka:9092"], api_version=(0, 10, 1))
        cliente.add_topic(PROCESSO)
        cliente.close()
        iniciado = True

    except Exception as e:
        print(f"Erro iniciando/configurando o kafka: {e}")
    return iniciado

@servico.get("/")
def get_info():
    return Response(json.dumps(INFO), mimetype="application/json", status=200)

@servico.post("/vender")
def vender_ebook():
    sucesso, id, dados = False, secrets.token_hex(16), request.json
    #aqui ficaria a logica de validação de dados e inicio do processamento da venda
    sleep(2)
    try:
        venda = {
            "id": id,
            "sucesso": 1,
            "mensagem": "Venda de e-book iniciada",
            "id_cliente": dados["id_cliente"],
            "id_ebook": dados["id_ebook"],
            "quantidade": dados["quantidade"],
        }

        produtor = KafkaProducer(bootstrap_servers=["kafka:9092"], api_version=(0, 10, 1))
        produtor.send(PROCESSO, json.dumps(venda).encode("utf-8"))
        produtor.flush()
        produtor.close()
        sucesso = True
    except Exception as e:
        print(f"Erro vendendo o ebook: {e}")
    return Response(status=204 if sucesso else 422)

if __name__ == "__main__":
    if iniciar():
        servico.run(host="0.0.0.0", port=5000, debug=True)