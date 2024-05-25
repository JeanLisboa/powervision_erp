# CADASTRAR FORNECEDOR, PREÇO DE CUSTO E PRODUTOS
# COMPRAR PRODUTOS
from wtforms import StringField, SubmitField, SelectField, IntegerField, DateField
from wtforms.validators import DataRequired, Email, Disabled, Length, ReadOnly, NumberRange
from flask_wtf import FlaskForm
from flask import Flask, render_template, redirect, url_for, request, jsonify, send_file, session, get_flashed_messages, flash
from forms import Mod_Compras






"""
class Compras:
    def cadastrar_fornecedores(self):
        print("class compras | method cadastrar_fornecedores")
        form_fornecedores = Mod_Compras.CadFornecedores()
        cod_fornecedor = Mod_Compras.CadFornecedores()
        nome_fantasia = Mod_Compras.CadFornecedores()
        razao_social = Mod_Compras.CadFornecedores()
        data = Mod_Compras.CadFornecedores()
        cnpj = Mod_Compras.CadFornecedores()
        insc_estadual = Mod_Compras.CadFornecedores()
        email = Mod_Compras.CadFornecedores()
        cep = Mod_Compras.CadFornecedores()
        telefone = Mod_Compras.CadFornecedores()
        endereco = Mod_Compras.CadFornecedores()
        uf = Mod_Compras.CadFornecedores()
        botao_submit_cad_fornecedor = Mod_Compras.CadFornecedores()

        form_fornecedores = form_fornecedores.data
        cod_fornecedor = cod_fornecedor.cod_fornecedor.data
        nome_fantasia = nome_fantasia.nome_fantasia.data
        razao_social = razao_social.razao_social.data
        data = data.data.data
        cnpj = cnpj.cnpj.data
        insc_estadual = insc_estadual.insc_estadual.data
        email = email.email.data
        cep = cep.cep.data
        telefone = telefone.telefone.data
        endereco = endereco.endereco.data
        uf = uf.uf.data
        botao_submit_cad_fornecedor = botao_submit_cad_fornecedor.botao_submit_cad_fornecedor.data


    def cadastrar_produtos(self):
        print("class compras | method comprar_produtos")
        form_cad_produtos = Mod_Compras.CadProduto()
        cod_produto = Mod_Compras.CadProduto()
        data = Mod_Compras.CadProduto()
        ean = Mod_Compras.CadProduto()
        descricao = Mod_Compras.CadProduto()
        fornecedor = Mod_Compras.CadProduto()
        unidade = Mod_Compras.CadProduto()
        categoria = Mod_Compras.CadProduto()
        botao_submit_cad_prod = Mod_Compras.CadProduto()
        form_cad_produtos = form_cad_produtos.data
        cod_produto = cod_produto.data
        data = data.data
        ean = ean.data
        descricao = descricao.data
        fornecedor = fornecedor.data
        unidade = unidade.data
        categoria = categoria.data
        botao_submit_cad_prod = botao_submit_cad_prod.data


    def comprar_produtos(self):
        print("class compras | method comprar_produtos")
        ordem_compra = Mod_Compras.ComprarProduto()
        botao_submit_compra = Mod_Compras.ComprarProduto()

        ordem_compra = ordem_compra.data
        botao_submit_compra = botao_submit_compra.data

    def relatorios_compras(self):
        print("class compras | method relatorios_compras")
        pass

"""