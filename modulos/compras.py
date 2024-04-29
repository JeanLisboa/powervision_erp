# CADASTRAR FORNECEDOR, PREÇO DE CUSTO E PRODUTOS
# COMPRAR PRODUTOS
from wtforms import StringField, SubmitField, SelectField, IntegerField, DateField
from wtforms.validators import DataRequired, Email, Disabled, Length, ReadOnly, NumberRange
from flask_wtf import FlaskForm



from datetime import date
os_date = date.today()

class Compras:
    def __init__(self):
        pass

    def cadastrar_fornecedores(self):
        print("class compras | method cadastrar_fornecedores")
        pass

    def comprar_produtos(self):
        print("class compras | method comprar_produtos")
        pass

    def relatorios_compras(self):
        print("class compras | method relatorios_compras")
        pass


class Cadastrar_Fornecedor:
    def __init__(self, nome, tipo_pessoa, nome_fantasia, cep, uf, email, telefone, observacoes, ativo):
        self.nome = nome
        self.tipo_pessoa = tipo_pessoa
        self.nome_fantasia = nome_fantasia
        self.cep = cep
        self.uf = uf
        self.email = email
        self.telefone = telefone
        self.observacoes = observacoes
        self.ativo = ativo



class Cadastrar_Produtos:
    def __init__(self, codigo, descricao, unidade, preco_custo, ean, data_compra, ativo):
        self.codigo = codigo
        self.descricao = descricao
        self.unidade = unidade
        self.preco_custo = preco_custo
        self.ean = ean
        self.data_compra = data_compra
        self.ativo = ativo