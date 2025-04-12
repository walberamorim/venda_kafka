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

@servico.post("/ebook/vender")
def vender_ebook():
    response = requests.post(f"{ROTA_EBOOK}/vender", json=request.json)
    return Response(status=response.status_code)

@servico.post("/giftcard/vender")
def vender_giftcard():
    response = requests.post(ROTA_GIFTCARD+"/vender", json=request.json)
    return Response(status=response.status_code)

if __name__ == "__main__":
    servico.run(host="0.0.0.0", port=5000, debug=True)