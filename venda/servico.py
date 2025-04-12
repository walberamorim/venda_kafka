from flask import Flask, Response, request
import requests
import json

servico = Flask("venda")

ROTA_EBOOK = "http://ebook:5000/"
ROTA_GIFTCARD = "http://giftcard:5000/"

INFO = {
    "descricao": "Serviço de vendas de e-books e giftcards",
    "versao": "0.0.1",
}

@servico.route("/", methods=["GET"])
def get_info():
    return Response(json.dumps(INFO), mimetype="application/json", status=200)

@servico.post("/ebook")
def vender_ebook():
    response = requests.post(ROTA_EBOOK, json=request.json)
    return Response(response.content, mimetype="application/json", status=response.status_code)

@servico.post("/giftcard")
def vender_giftcard():
    response = requests.post(ROTA_GIFTCARD, json=request.json)
    return Response(response.content, mimetype="application/json", status=response.status_code)

if __name__ == "__main__":
    servico.run(host="0.0.0.0", port=5000, debug=True)