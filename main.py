from datetime import date
import mysql.connector
from flask import Flask, render_template, redirect, url_for, request, session
import geral
from flask_wtf.csrf import CSRFProtect
from forms import Mod_Compras, Mod_Comercial, Mod_Pricing
from geral import buscar_cnpj

from geral import Validadores, Formatadores, AtualizaCodigo, Buscadores, Totais
usuario = 'ADMIN'

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

total_ordem_compra = 0
contador_item = 0
lista_contador_item = []
lista_ordem_compra = []  # UTILIZADO EM compras/gerar_ordem_compra


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

            if Validadores.valida_cnpj(form_fornecedores.cnpj.data) is True and buscar_cnpj(
                    form_fornecedores.cnpj.data) is True:
                alert = geral.AlertaMsg.cnpj_ja_existente()

            if Validadores.valida_cnpj(form_fornecedores.cnpj.data) is True and buscar_cnpj(
                    form_fornecedores.cnpj.data) is False:
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
        form_cad_produtos.fornecedor.choices = [('Selecionar um fornecedor', 'Selecionar um fornecedor')] + [
            (f[0], f[0]) for f in fornecedores]
        cod_produto = geral.AtualizaCodigo.cod_produto()
        ean = form_cad_produtos.ean.data
        descricao = form_cad_produtos.descricao.data
        unidade = form_cad_produtos.unidade.data
        categoria = form_cad_produtos.categoria.data
        data = Formatadores.os_data()

        if 'botao_submit_cad_prod' in request.form:
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
        global contador_item
        global lista_ordem_compra
        global total_ordem_compra

        item_ordem_compra = []
        form_gerar_ordem_compra = Mod_Compras.GerarOrdemCompra()
        data = Formatadores.os_data()
        ordem_compra = geral.AtualizaCodigo.ordem_compra()
        descricao = form_gerar_ordem_compra.descricao.data
        fornecedor = form_gerar_ordem_compra.fornecedor.data
        unidade = form_gerar_ordem_compra.unidade.data
        categoria = form_gerar_ordem_compra.categoria.data
        codigo = form_gerar_ordem_compra.codigo.data
        ean = form_gerar_ordem_compra.ean.data
        quantidade = form_gerar_ordem_compra.quantidade.data
        preco_unitario = form_gerar_ordem_compra.preco_unitario.data
        preco_historico = form_gerar_ordem_compra.preco_historico.data
        preco_medio = form_gerar_ordem_compra.preco_medio.data
        ultimo_preco = form_gerar_ordem_compra.ultimo_preco.data

        alert = geral.AlertaMsg.cad_fornecedor_realizado()

        if 'total_ordem_compra' not in session:
            session['total_ordem_compra'] = 0
        if 'preco_medio' not in session:
            session['preco_medio'] = 0
        if 'ultimo_preco' not in session:
            session['ultimo_preco'] = 0
        if 'preco_historico' not in session:
            session['preco_historico'] = 0

        try:
            total_item = quantidade * preco_unitario
        except:
            total_item = 0

        if preco_medio is None:
            preco_medio = 0
        if preco_historico is None:
            preco_historico = 0
        if ultimo_preco is None:
            ultimo_preco = 0

        resultado = None
        if request.method == 'POST':
            item_ordem_compra.clear()
            try:
                if 'botao_pesquisar_item' in request.form:
                    if descricao == '' and ean == '':
                        resultado = Buscadores.buscar_produto_pelo_codigo(codigo)
                        resultado = resultado[0]
                    if codigo == '' and descricao == '':
                        resultado = Buscadores.buscar_produto_pelo_ean(ean)
                        resultado = resultado[0]
                    if resultado is None:
                        pass

                    # TRANSFORMAR EM FUNÇÃO
                    preco_medio = Buscadores.OrdemCompra.preco_medio(codigo)
                    ultimo_preco = Buscadores.OrdemCompra.ultimo_preco(codigo)
                    print(f'Preço médio >>> {preco_medio}')

                    # alert = geral.AlertaMsg.cadastro_inexistente()
                    # return redirect(url_for('gerar_ordem_compra'))
            except:
                print('except')
                alert = geral.AlertaMsg.cadastro_inexistente()
                pass

            try:
                if 'botao_incluir_item' in request.form:
                    try:
                        Formatadores.preparar_item_ordem_compra()
                        # print('teste')

                        contador_item = len(lista_contador_item)
                        print(f'max lista contador item {max(lista_contador_item)}')

                    except:
                        contador_item = 0

                    #  TRANSFORMAR EM FUNÇÃO

                    contador_item += 1
                    print(contador_item)
                    lista_contador_item.append(contador_item)
                    # item_ordem_compra.append(Formatadores.formatar_data(data))
                    item_ordem_compra.append(Formatadores.data_formato_db(data))
                    item_ordem_compra.append(ordem_compra)
                    item_ordem_compra.append(descricao)
                    item_ordem_compra.append(unidade)
                    item_ordem_compra.append(categoria)
                    item_ordem_compra.append(codigo)
                    item_ordem_compra.append(ean)
                    item_ordem_compra.append(quantidade)
                    item_ordem_compra.append(preco_unitario)
                    item_ordem_compra.append(total_item)
                    # item_ordem_compra.append(ultimo_preco)
                    # item_ordem_compra.append(preco_historico)
                    # item_ordem_compra.append(preco_medio)
                    lista_ordem_compra.append(item_ordem_compra[:])
                    print(lista_ordem_compra)
                    item_ordem_compra.clear()
                    total_ordem_compra += lista_ordem_compra[-1][9]
            except Exception as e:
                print(e)

            try:
                if 'botao_submit_compra' in request.form:
                    print('botao_submit_compra pressionado')
                    cont_temp = 1
                    while cont_temp <= len(lista_ordem_compra):
                        for i in lista_ordem_compra:
                            print(f'i  linha {cont_temp} >>>> {i}')
                            values = (f"'{date.strftime(data, '%Y-%m-%d')}',"
                                      f"'{i[1]}',"
                                      f"'{cont_temp}',"
                                      f"'{i[2]}',"
                                      f"'{i[3]}',"
                                      f"'{i[4]}',"
                                      f"'{i[5]}',"
                                      f"'{i[6]}',"
                                      f"'{i[7]}',"
                                      f"'{i[8]}',"
                                      f"'{i[9]}',"
                                      f"'{usuario}'")

                            query = (f'INSERT INTO ORDEM_COMPRA'
                                     f'(DATA, ORDEM_COMPRA, ITEM, DESCRICAO, UNIDADE, CATEGORIA, CODIGO, EAN, QUANTIDADE, PRECO, TOTAL_ITEM, USUARIO)'
                                     f' VALUES ({values});')
                            print(f'Query {cont_temp} >>>> {query}')
                            mycursor.execute(query)
                            mycursor.fetchall()
                            fechadb = 'SET SQL_SAFE_UPDATES = 1'
                            mycursor.execute(fechadb)
                            mycursor.fetchall()
                            mydb.commit()
                            cont_temp += 1
                    lista_ordem_compra.clear() # limpa a lista para a proxima ordem de compra

            except Exception as e:
                print(e)

            try:
                if 'botao_limpar_ordem' in request.form:
                    print('botao_limpar_ordem pressionado')
                    lista_ordem_compra.clear()
                    total_ordem_compra = 0
                    # ultimo_preco = 0
                    # preco_medio = 0

                    return redirect(url_for('gerar_ordem_compra'))

            except Exception as e:
                print(e)


            alert = session.pop('alert', None)

        return render_template('compras/gerar_ordem_compra.html',
                               alert=alert,
                               total_ordem_compra=total_ordem_compra,
                               preco_medio=preco_medio,
                               ultimo_preco=ultimo_preco,
                               preco_historico=preco_historico,
                               contador_item=contador_item,  # informa o proximo item a ser incluido=
                               dicionario_ordem_compra=lista_ordem_compra,
                               ordens_em_aberto=Buscadores.OrdemCompra.ordem_compra_em_aberto(codigo),
                               # informa os itens na ordem de compra para renderizar na tabela
                               relatorio_produtos=Buscadores.mostrar_tabela_produtos(),
                               # serve para mostrar os produtos na tela popup
                               resultado_pesquisa=resultado,  # informa no html o resultado da busca pelo código
                               form_gerar_ordem_compra=form_gerar_ordem_compra,  # renderiza os forms na pagina html
                               cod_produto=AtualizaCodigo.cod_produto(),  # informa o proximo codigo do produto
                               ordem_compra=AtualizaCodigo.ordem_compra(),
                               # informa o proximo numero da ordem de compra
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
