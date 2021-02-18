import pymongo
from flask import Flask, request, jsonify, redirect
import flask
from functions import Calculadora, Cpf, Cel
from pymongo import MongoClient
from jsontries import JSONEncoder

app = Flask(__name__)

client = pymongo.MongoClient(
    "mongodb+srv://DbTesteUser:01139746eE@cluster1.bwmed.mongodb.net/testemongo?retryWrites=true&w=majority")
db = client.testemongo

CALCULADORA = "http://127.0.0.1:5000/calculadora"

@app.route('/', methods=['GET', 'POST'])
def Index():
    data = request.get_json()
    # db.dadosrecebidos.insert_one({"cpf": data["cpf"], "celular": data["celular"]})
    cpf = data[str("cpf")]
    celular = data[str("celular")]
    return flask.redirect (CALCULADORA, code=302)



@app.route('/calculadora', methods=['GET', 'POST'])
def CalculadoraEmprestimo():
    dados = request.get_json()
    resultados = []
    taxasresult = []
    #cpf = data[str("cpf")]
    cpf = Index().cpf
    celular = Index().cpf
    valor = dados[str('valor')]
    parcelas = int(dados["parcelas"])
    usuarios = db.clientes.find({"cpf": cpf})
    if usuarios is not None:
        for i in usuarios:
            resultados.append(i)
        if resultados:
            testeresultados = resultados[0]
        else:
            testeresultados = resultados
    if testeresultados:
        cpfquery = testeresultados["cpf"]
        statusquery = testeresultados["negativado"]
        scorequery = testeresultados["score"]
        if statusquery:
            taxa = db.taxas.find({"tipo": "NEGATIVADO"})
            for i in taxa:
                taxasresult.append(i)
            taxas = taxasresult[0]
        elif statusquery is False and scorequery > 500:
            taxa = db.taxas.find({"tipo": "SCORE_ALTO"})
            for i in taxa:
                taxasresult.append(i)
            taxas = taxasresult[0]
        else:
            taxa = db.taxas.find({"tipo": "SCORE_BAIXO"})
            for i in taxa:
                taxasresult.append(i)
            taxas = taxasresult[0]
    else:
        cpfquery = cpf
        scorequery = 0
        statusquery = False
        taxa = db.taxas.find({"tipo": "SCORE_BAIXO"})
        for i in taxa:
            taxasresult.append(i)
        taxas = taxasresult[0]

    taxaemprestimo = taxas["taxas"]
    taxasobtidas = taxaemprestimo[parcelas]
    resultado = Calculadora(valor, taxasobtidas, parcelas)
    return jsonify({"Resultado": resultado})



if __name__ == "__main__":
    app.run(debug=True)
