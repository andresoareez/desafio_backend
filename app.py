import pymongo
from flask import Flask, request, jsonify, redirect
import flask
from functions import Calculadora
from pymongo import MongoClient
from JsonEncoder import JSONEncoder

app = Flask(__name__)

client = pymongo.MongoClient(
    "mongodb+srv://DbTesteUser:01139746eE@cluster1.bwmed.mongodb.net/testemongo?retryWrites=true&w=majority")
db = client.testemongo


# Rota para obtencao de CPF e CELULAR
@app.route('/', methods=['GET', 'POST'])
def Index():
    data = request.get_json()
    cpf = data[str("cpf")]
    celular = data[str("celular")]
    db.dadosrecebidos.remove()
    db.dadosrecebidos.insert_one({"cpf": cpf, "celular": celular})
    return jsonify({"CPF": cpf,
                    "celular": celular})


# rota para calculo do emprestimo
@app.route('/calculadora', methods=['GET', 'POST'])
def CalculadoraEmprestimo():
    dados = request.get_json()
    CpfList = []
    DadosCadastro = []
    taxasquery = []
    parcelasdefinidas = [6, 12, 18, 24, 36]  # Parcelas permitidas por regra inicial
    querycpf = db.dadosrecebidos.find()  # Obtendo CPF inserido
    if querycpf is not None:
        for i in querycpf:
            CpfList.append(i)
        if CpfList:
            cpfresultado = CpfList[0]
        else:
            cpfresultado = CpfList
    if cpfresultado:
        cpf = cpfresultado["cpf"]
        celular = cpfresultado["celular"]
    valor = dados[str('valor')]  # recebendo valor
    parcelas = int(dados["parcelas"])  # recebendo quantidade de parcelas
    # Check de parcelas validas
    if parcelas not in parcelasdefinidas:
        raise ValueError("Insira um valor de parcelas válidos. As nossas opções são 6, 12, 18, 24 ou 36 parcelas")

    usuarios = db.clientes.find({"cpf": cpf})  # check de cpf com cpfs pre cadastrados
    if usuarios is not None:
        for i in usuarios:
            DadosCadastro.append(i)
        if DadosCadastro:
            CadastroUnpack = DadosCadastro[0]
        else:
            CadastroUnpack = DadosCadastro

    # Lacos para definicao de status e taxas de acordo com o perfil do cliente

    if CadastroUnpack:
        cpfquery = CadastroUnpack["cpf"]
        statusquery = CadastroUnpack["negativado"]
        scorequery = CadastroUnpack["score"]
        if statusquery:
            taxa = db.taxas.find({"tipo": "NEGATIVADO"})
            for i in taxa:
                taxasquery.append(i)
            taxas = taxasquery[0]
        elif statusquery is False and scorequery > 500:
            taxa = db.taxas.find({"tipo": "SCORE_ALTO"})
            for i in taxa:
                taxasquery.append(i)
            taxas = taxasquery[0]
        else:
            taxa = db.taxas.find({"tipo": "SCORE_BAIXO"})
            for i in taxa:
                taxasquery.append(i)
            taxas = taxasquery[0]
    else:
        cpfquery = cpf
        scorequery = 0
        statusquery = False
        taxa = db.taxas.find({"tipo": "SCORE_BAIXO"})
        for i in taxa:
            taxasquery.append(i)
        taxas = taxasquery[0]
    taxaemprestimo = taxas["taxas"]  # obtencao da taxa para o cliente
    taxasobtidas = taxaemprestimo[parcelas]
    ResultadoEmprestimo = Calculadora(valor, taxasobtidas, parcelas)  # retorno do resultado pela calculadora
    return ResultadoEmprestimo


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
