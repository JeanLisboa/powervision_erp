from datetime import date
import mysql.connector
from flask import Flask, render_template, redirect, url_for, request, session
import geral
from flask_wtf.csrf import CSRFProtect
from forms import Mod_Compras, Mod_Comercial, Mod_Pricing

from geral import buscar_cnpj
from geral import Validadores, Formatadores, AtualizaCodigo, Buscadores

app = Flask(__name__)
app.config['SECRET_KEY'] = "f92ed5835155e99cc60e328de2cce349830e28984c160jj3gg2"
csrf = CSRFProtect(app)

mydb = mysql.connector.connect(
  host="localhost",
  user="admin2024",
  password="204619",
  database="projeto_erp"
)
mycursor = mydb.cursor()

@app.route('/')
def main():
    return render_template('homepage.html')


@app.route('/admin', methods=['POST', 'GET'])
def admin():
    return render_template('admin.html')


class Compras:
    @staticmethod
    @app.route('/cadastrar_fornecedores', methods=['POST', 'GET'])
    def cadastrar_fornecedores():
        cod_fornecedor = geral.AtualizaCodigo.cod_fornecedor()
        form_fornecedores = Mod_Compras.CadFornecedores()
        razao_social = form_fornecedores.razao_social.data
        nome_fantasia = form_fornecedores.nome_fantasia.data
        cnpj = form_fornecedores.cnpj.data
        inscricaoestadual = form_fornecedores.insc_estadual.data
        email = form_fornecedores.email.data
        cep = form_fornecedores.cep.data
        telefone = form_fornecedores.telefone.data
        endereco = form_fornecedores.endereco.data
        municipio = form_fornecedores.municipio.data
        uf = form_fornecedores.uf.data
        data = Formatadores.os_data()

        if 'botao_submit_cad_fornecedor' in request.form:
            if Validadores.valida_cnpj(form_fornecedores.cnpj.data) is False:
                alert = geral.AlertaMsg.cnpj_invalido()

            if Validadores.valida_cnpj(form_fornecedores.cnpj.data) is True and buscar_cnpj(form_fornecedores.cnpj.data) is True:
                alert = geral.AlertaMsg.cnpj_ja_existente()

            if Validadores.valida_cnpj(form_fornecedores.cnpj.data) is True and buscar_cnpj(form_fornecedores.cnpj.data) is False:
                print('informações validadas - cadastrar no banco de dados')
                values = (f"'{date.strftime(data, '%Y-%m-%d')}',"
                          f"'{cod_fornecedor}',"
                          f"'{nome_fantasia}',"
                          f"'{razao_social}',"
                          f"'{cnpj}',"
                          f"'{inscricaoestadual}',"
                          f"'{email}',"
                          f"'{telefone}',"
                          f"'{cep}',"
                          f"'{endereco}',"
                          f"'{municipio}',"
                          f"'{uf}'")
                query = (
                    f'INSERT INTO FORNECEDORES '
                    f'(DATA, CODIGO, NOMEFANTASIA, RAZAOSOCIAL, CNPJ, INSCRICAOESTADUAL, EMAIL, '
                    f'TELEFONE, CEP, ENDERECO, MUNICIPIO, UF) '
                    f'VALUES ({values})')
                mycursor.execute(query)
                mycursor.fetchall()
                fechadb = 'SET SQL_SAFE_UPDATES = 1'
                mycursor.execute(fechadb)
                mycursor.fetchall()
                mydb.commit()
                alert = geral.AlertaMsg.cad_fornecedor_realizado()
                AtualizaCodigo.cod_fornecedor()
                return redirect(url_for('cadastrar_fornecedores'))

        alert = session.pop('alert', None)

        return render_template('compras/cadastrar_fornecedores.html',
                               alert=alert,
                               form_fornecedores=form_fornecedores,
                               cod_fornecedor=AtualizaCodigo.cod_fornecedor(),
                               data=Formatadores.formatar_data(Formatadores.os_data()))

    @staticmethod
    @app.route('/cadastrar_produtos', methods=['POST', 'GET'])
    def cadastrar_produtos():
        form_cad_produtos = Mod_Compras.CadProduto()
        fornecedores = geral.Buscadores.buscar_fornecedor()
        form_cad_produtos.fornecedor.choices = [('Selecionar um fornecedor', 'Selecionar um fornecedor')] + [(f[0], f[0]) for f in fornecedores]
        cod_produto = geral.AtualizaCodigo.cod_produto()
        ean = form_cad_produtos.ean.data
        descricao = form_cad_produtos.descricao.data
        unidade = form_cad_produtos.unidade.data
        categoria = form_cad_produtos.categoria.data
        data = Formatadores.os_data()
        # fornecedor = geral.Buscadores.buscar_fornecedor()



        if 'botao_submit_cad_prod' in request.form and form_cad_produtos.validate_on_submit():
            fornecedor = form_cad_produtos.fornecedor.data

            values = (f"'{date.strftime(data, '%Y-%m-%d')}',"
                      f"'{cod_produto}',"
                      f"'{fornecedor}',"
                      f"'{ean}',"
                      f"'{descricao}',"
                      f"'{unidade}',"
                      f"'{categoria}'")
            query = (f'INSERT INTO PRODUTOS '
                     f'(DATA, CODIGO, FORNECEDOR, '
                     f'EAN, DESCRICAO, UNIDADE, CATEGORIA) '
                     f'VALUES ({values})')
            print(query)
            mycursor.execute(query)
            mycursor.fetchall()
            fechadb = 'SET SQL_SAFE_UPDATES = 1'
            mycursor.execute(fechadb)
            mycursor.fetchall()
            mydb.commit()

            alert = geral.AlertaMsg.cad_fornecedor_realizado()
            # AtualizaCodigo.cod_produto()
            # Buscadores.buscar_fornecedor()
            return redirect(url_for('cadastrar_produtos'))

        alert = session.pop('alert', None)
        return render_template('compras/cadastrar_produtos.html',
                               alert=alert,
                               form_cad_produtos=form_cad_produtos,
                               cod_produto=AtualizaCodigo.cod_produto(),
                               data=Formatadores.formatar_data(Formatadores.os_data()))

    @staticmethod
    @app.route('/gerar_ordem_compra', methods=['POST', 'GET'])
    def gerar_ordem_compra():
        form_gerar_ordem_compra = Mod_Compras.GerarOrdemCompra()
        return render_template('compras/gerar_ordem_compra.html',
                               form_gerar_ordem_compra=form_gerar_ordem_compra,
                               data=Formatadores.formatar_data(Formatadores.os_data()))

    @staticmethod
    @app.route('/relatorios_compras', methods=['POST', 'GET'])
    def relatorios_compras():
        return render_template('compras/relatorios_compras.html',
                               data=Formatadores.formatar_data(Formatadores.os_data()))


class Comercial:
    @staticmethod
    @app.route('/cadastrar_clientes', methods=['POST', 'GET'])
    def cadastrar_clientes():
        form_cad_clientes = Mod_Comercial.CadastrarCliente()
        return render_template('comercial/cadastrar_clientes.html',
                               form_cad_clientes=form_cad_clientes,
                               data=Formatadores.formatar_data(Formatadores.os_data()))

    @staticmethod
    @app.route('/incluir_pedido_venda', methods=['POST', 'GET'])
    def incluir_pedido_venda():
        form_incluir_pedido_venda = Mod_Comercial.IncluirPedidoVenda()
        return render_template('comercial/incluir_pedido_venda.html',
                               form_incluir_pedido_venda=form_incluir_pedido_venda,
                               data=Formatadores.formatar_data(Formatadores.os_data()))


class Pricing:
    @staticmethod
    @app.route('/cadastrar_tabela', methods=['POST', 'GET'])
    def cadastrar_tabela():
        form_cadastrar_tabela = Mod_Pricing.CadastrarTabela()
        return render_template('pricing/cadastrar_tabela.html', form_cadastrar_tabela=form_cadastrar_tabela,
                               data=Formatadores.formatar_data(Formatadores.os_data()))


class Logistica:
    pass


@app.route('/financeiro', methods=['POST', 'GET'])
def financeiro():
    return render_template('financeiro.html', data=Formatadores.formatar_data(Formatadores.os_data()))


@app.route('/logistica', methods=['POST', 'GET'])
def logistica():
    return render_template('logistica.html', data=Formatadores.formatar_data(Formatadores.os_data()))


@app.route('/fiscal', methods=['POST', 'GET'])
def fiscal():
    return render_template('fiscal.html')


@app.route('/ajuda', methods=['POST', 'GET'])
def ajuda():
    return render_template('ajuda.html')


@app.route('/sobre', methods=['POST', 'GET'])
def sobre():
    return render_template('sobre.html')


@app.route('/contato', methods=['POST', 'GET'])
def contato():
    return render_template('contato.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    return render_template('login.html')


@app.route('/teste', methods=['POST', 'GET'])
def teste():
    return render_template('teste.html')


if __name__ == "__main__":
    app.run(debug=True)
