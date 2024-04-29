# ACOMPANHA O CONTROLE DE CONTAS A RECEBER
"""
DATA DA VENDA
COD CLIENTE
NOME FANTASIA
RAZAO SOCIAL
VALOR DA VENDA
BOTAO ENVIAR NOTIFICAÇÃO VIA WTSP

"""
# ACOMPANHA O CONTROLE DE CONTAS A PAGAR
"""
DATA DA COMPRA
COD FORNECEDOR
NOME FANTASIA
RAZAO SOCIAL
VALOR DA COMPRA

"""

class Contas_a_pagar:
    def __init__(self, data, codfornecedor, nomefantasia, razao, valor):
        self.data = data
        self.codfornecedor = codfornecedor
        self.nomefantasia = nomefantasia
        self.razao = razao
        self.valor = valor

class Contas_a_receber:
    def __init__(self, data, codcliente, nomefantasia, razao, valor):
        self.data = data
        self.codcli = codcliente
        self.nomefantasia = nomefantasia
        self.razao = razao
        self.valor = valor