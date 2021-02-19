def Calculadora(valor, taxa, parcelas):
    valortaxa = valor * taxa / 100
    valorfinal = valortaxa * parcelas + valor
    valorparcela = valorfinal / parcelas
    formatvalorparcela = round(valorparcela, 2)
    return 'O valor final do empréstimo é de R${} e cada parcela ficará R${}, com uma taxa de {}% ao mês' \
        .format(valorfinal, formatvalorparcela, taxa)