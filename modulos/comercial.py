# CADASTRA CLIENTE
# ABA_1 - DADOS CADASTRAIS
# CODIGO CLIENTE: INCREMENTAL
#  NOME DO CLIENTE
# PES FIS/JUR
# N FANTASIA
# CEP
# ENDERECO
# NUMERO
# COMPLEMENTO
# BAIRRO
# CIDADE
# COD MUNICIPIO
# ESTADO
# TELEFONES
# EMAIL
# OBSERVACOES
# ATIVO (S/N)
# OBSERVAÇÃO

# ABA_2 ADM/FIN
# TIPO FRETE (CIF/FOB)
# VENDEDOR
# BANCO (FINANCEIRO)
# MAIOR COMPRA
# MAIOR, MENOR E MÉDIA (ATRASO, VALOR NF)
# NUMERO DE COMPRAS
# OBSERVAÇÃO

# ABA_3 VENDAS
# COND_PAGAMENTO (FINANCEIRO)
# LEADTIME (LOGISTICA)
# TRANSPORTADOR (LOGISTICA)
# OBSERVAÇÃO

# INSERE PEDIDO DE VENDAS
#
# RELATORIO DE PEDIDOS DE VENDAS. COM POSSIBILIDADE DE EDITAR, CASO O PEDIDO AINDA NÃO TENHA SIDO SEPARADO

class Comercial:
    def __init__(self, banco, prazo_pagamento,  nome, tipo_pessoa, nome_fantasia, cep, endereco, numero, complemento, bairro, cidade, codmunicipio, estado, telefone, email, observacoes, ativo):
        self.banco = banco
        self.prazo = prazo_pagamento
        self.nome = nome
        self.tipo_pessoa = tipo_pessoa
        self.nome_fantasia = nome_fantasia
        self.cep = cep
        self.endereco = endereco
        self.numero = numero
        self.complemento = complemento
        self.bairro = bairro
        self.cidade = cidade
        self.codmunicipio = codmunicipio
        self.estado = estado
        self.telefone = telefone
        self.email = email
        self.observacoes = observacoes
        self.ativo = ativo