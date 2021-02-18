from flask import jsonify
from validate_docbr import CPF


class Cpf:
    def __init__(self, doccpf):
        doccpf = str(doccpf)
        if self.CpfValido(doccpf):
            self.cpf = doccpf
        else:
            raise ValueError('CPF Inválido')

    def CpfValido(self, cpf):
        if len(cpf) == 11:
            validador = CPF()
            return validador.validate(cpf)
        else:
            raise ValueError('Quantidade de Dígitos inválida, o Cpf precisa ter 11 dígitos')


class Cel:
    def __init__(self, celular):
        if self.ValidaCelular(celular):
            self.celularvalido = celular
        else:
            raise ValueError('O número de celular precisa ter 11 digitos!')

    @staticmethod
    def ValidaCelular(celular):
        if len(celular) == 11:
            return True
        else:
            False


def Calculadora(valor, taxa, parcelas):
    valortaxa = valor * taxa / 100
    valorfinal = valortaxa * parcelas + valor
    valorparcela = valorfinal / parcelas
    formatvalorparcela = round(valorparcela, 2)

    return 'O valor final do empréstimo é de R${} e cada parcela ficará R${}, com uma taxa de {}% ao mês'\
        .format(valorfinal, formatvalorparcela, taxa)


# def SalvarDados(cpf, celular):
#     cpfsalvo = cpf
#     celularsalvo = celular
#
#     return jsonify({"Cpf": cpfsalvo, {"Celular": celularsalvo})