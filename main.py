# outras bibliotecas
import mysql.connector
import webbrowser
from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect
from forms import ModComercial, ModPricing, Mod_Logistica, ModAdmin, ModCompras
from wtforms import (SelectField)
from geral import Formatadores
# modulos
import modulos.admin
import modulos.comercial
import modulos.compras
import modulos.estoque
import modulos.financeiro
import modulos.fiscal
import modulos.logistica
import modulos.pricing
import modulos.sobre
import modulos.precificacao
import os
import logging
log = logging.getLogger('werkzeug')
# log.setLevel(logging.CRITICAL)  # Ou logging.CRITICAL para ocultar tudo

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'


global alert
usuario = 'ADMIN'
app = Flask(__name__)
app.config['SECRET_KEY'] = "f92ed5835155e99cc60e328de2cce349830e28984c160jj3gg2"
csrf = CSRFProtect(app)


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Ma204619@",
    database="projeto_erp"
)
mycursor = mydb.cursor()



@app.route('/')
def main():
    return render_template('/homepage.html')


class Admin:
    @staticmethod
    @app.route('/regra_negocio', methods=['POST', 'GET'])
    def regra_negocio():
        return modulos.admin.regra_negocio()


class Sobre:
    @staticmethod
    @app.route('/ajuda', methods=['POST', 'GET'])
    def ajuda():
        return modulos.sobre.ajuda()

    @staticmethod
    @app.route('/contato', methods=['POST', 'GET'])
    def contato():
        return modulos.sobre.contato()

    @staticmethod
    @app.route('/sobre', methods=['POST', 'GET'])
    def sobre():
        return modulos.sobre.sobre()

    @staticmethod
    @app.route('/estrutura', methods=['POST', 'GET'])
    def estrutura():
        return modulos.sobre.estrutura()

    @staticmethod
    @app.route('/fluxograma', methods=['POST', 'GET'])
    def fluxograma():
        return modulos.sobre.fluxograma()

    @staticmethod
    @app.route('/cronograma', methods=['POST', 'GET'])
    def cronograma():
        return modulos.sobre.cronograma()

    @staticmethod
    @app.route('/backlog', methods=['POST', 'GET'])
    def backlog():
        return modulos.sobre.backlog()

    @staticmethod
    @app.route('/teste', methods=['POST', 'GET'])
    def teste():
        return modulos.sobre.teste()

class Compras:

    @staticmethod
    @app.route('/cadastrar_fornecedores', methods=['POST', 'GET'])
    def cadastrar_fornecedores():
        return modulos.compras.cadastrar_fornecedores()

    @staticmethod
    @app.route('/editar_ordem_compra', methods=['POST', 'GET'])
    def editar_ordem_compra():
        return modulos.compras.editar_ordem_compra()

    @staticmethod
    @app.route('/cadastrar_produtos', methods=['POST', 'GET'])
    def cadastrar_produtos():
        return modulos.compras.cadastrar_produtos()

    @staticmethod
    @app.route('/analisar_ordem_de_compra', methods=['POST', 'GET'])
    def analisar_ordem_de_compra():
        return modulos.compras.analisar_ordem_de_compra()

    @staticmethod
    @app.route('/gerar_ordem_compra', methods=['POST', 'GET'])
    def gerar_ordem_compra():
        return modulos.compras.gerar_ordem_compra()

    @staticmethod
    @app.route('/adicionar_item_ordem_compra', methods=['POST', 'GET'])
    def adicionar_item_ordem_compra():
        return modulos.compras.adicionar_item_ordem_compra()


    @staticmethod
    @app.route('/relatorios_compras', methods=['POST', 'GET'])
    def relatorio_compras():
        return modulos.compras.relatorio_compras()


class Logistica:
    @staticmethod
    @app.route('/realizar_conferencia', methods=['POST', 'GET'])
    def realizar_conferencia():
        return modulos.logistica.realizar_conferencia()

    @staticmethod
    @app.route('/estoque', methods=['POST', 'GET'])
    def estoque():
        return modulos.logistica.estoque()

    @staticmethod
    @app.route('/entrada_ordem_compra_por_nota', methods=['POST', 'GET'])
    def entrada_ordem_compra_por_nota():
        return modulos.logistica.entrada_ordem_compra_por_nota()

    @staticmethod
    @app.route('/entrada_ordem_compra_por_pedido', methods=['POST', 'GET'])
    def entrada_ordem_compra_por_pedido():
        return modulos.logistica.entrada_ordem_compra_por_pedido()

class Comercial:
    @staticmethod
    @app.route('/cadastrar_clientes', methods=['POST', 'GET'])
    def cadastrar_clientes():
       return modulos.comercial.cadastrar_clientes()

    @staticmethod
    @app.route('/gerar_ordem_venda', methods=['POST', 'GET'])
    def gerar_ordem_venda():
        return modulos.comercial.gerar_ordem_venda()

    @staticmethod
    @app.route('/adicionar_item_ordem_venda', methods=['POST', 'GET'])
    def adicionar_item_ordem_venda():
        return modulos.comercial.adicionar_item_ordem_venda()

    @staticmethod
    @app.route('/gestao_carteira', methods=['POST', 'GET'])
    def gestao_carteira():
        return modulos.comercial.gestao_carteira()

    @staticmethod
    @app.route('/relatorio_ordem_venda', methods=['POST', 'GET'])
    def relatorio_ordem_venda():
        return modulos.comercial.relatorio_ordem_venda()

    @staticmethod
    @app.route('/editar_ordem_venda', methods=['POST', 'GET'])
    def editar_ordem_venda():
        return modulos.comercial.editar_ordem_venda()

class Pricing:
    @staticmethod
    @app.route('/cadastrar_tabela', methods=['POST', 'GET'])
    def cadastrar_tabela():
        form_cadastrar_tabela = ModPricing.CadastrarTabela()
        return render_template('pricing/cadastrar_tabela.html', form_cadastrar_tabela=form_cadastrar_tabela,
                               data=Formatadores.formatar_data(Formatadores.os_data()))

    @staticmethod
    @app.route('/precificacao', methods=['POST', 'GET'])
    def precificacao():
        return modulos.precificacao.precificacao()
        # return render_template('pricing/precificacao.html')

@app.route('/financeiro', methods=['POST', 'GET'])
def financeiro():
    return render_template('financeiro.html', data=Formatadores.formatar_data(Formatadores.os_data()))


@app.route('/fiscal', methods=['POST', 'GET'])
def fiscal():
    return render_template('fiscal.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    return render_template('login.html')

import logging
import logging.config
import json

# Lê o arquivo JSON e aplica a configuração
with open("config/logging_config.json", "r", encoding="utf8") as f:
    config = json.load(f)
    logging.config.dictConfig(config)

# Obtém o logger nomeado
logger = logging.getLogger("meuapp")

# Exemplo de uso
# logger.debug("mensagem de debug")
# logger.info("mensagem de info")
# logger.warning("mensagem de aviso")
# logger.error("mensagem de erro")
# logger.critical("mensagem crítica")

if __name__ == "__main__":
    app.run(host='0.0.0.0',  debug=True, port=5000)

    # FIXME: AJUSTAR DIV DE TODAS AS JANELAS PARA QUE APAREÇA A ÁREA RESERVADA PARA ALERTS A EXEMPLO DA TELA GERAR ORDEM DE VENDA
    #