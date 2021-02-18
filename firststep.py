import pymongo
from flask import Flask, request, redirect, jsonify
from functions import Cpf, Cel, Calculadora
from pymongo import MongoClient
from jsontries import JSONEncoder

app = Flask(__name__)

client = pymongo.MongoClient("mongodb+srv://DbTesteUser:01139746eE@cluster1.bwmed.mongodb.net/testemongo?retryWrites=true&w=majority")
db = client.testemongo


@app.route('/start', methods=['POST'])
def EntradaDados():
    resp = request.get_json()
    cpf = resp["cpf"]
    celular = Cel(resp["celular"])

    return jsonify(cpf, celular)#redirect("http://127.0.0.1:5000/calculadora", 302)


def Get_Dados():
    dados = EntradaDados()
    dadoscelular = EntradaDados()
    entradacpf = dadoscpf
    cpf = Cpf(entradacpf)
    telefone = Cel(dadoscelular)


@app.route('/calculadora', methods=['POST'])
def calculaemprestimo():
    resp = request.get_json()
    valor = resp['valor']
    parcelas = resp['parcelas']
    #dados = Get_Dados()
    cpf = resp['cpf']
    celular = resp['celular']
    usuario = db.clients.find_one({"cpf": cpf})
    celusu = db.clients.find_one({"celular": celular})
    if usuario["cpf"] and celusu["celular"] is not None:
        if usuario["negativado"]:
            tipotaxa = db.taxas.find_one({"tipo": "NEGATIVADO"})
            taxa = tipotaxa[parcelas]
        elif usuario["score"] > 500:
            tipotaxa = db.taxas.find_one({"tipo": "SCORE_ALTO"})
            taxa = tipotaxa[parcelas]
        else:
            tipotaxa = db.taxas.find_one({"tipo": "SCORE_BAIXO"})
            taxa = tipotaxa[parcelas]
    else:
        tipotaxa = db.taxas.find_one({"tipo": "SCORE_BAIXO"})
        taxa = tipotaxa[parcelas]
    resultado = Calculadora(valor, taxa, parcelas)
    return jsonify({"Resultado": resultado})


if __name__ == "__main__":
    app.run(debug=True)
