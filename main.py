from datetime import date
import mysql.connector
from flask import Flask, render_template, redirect, url_for, request, session
import geral
from flask_wtf.csrf import CSRFProtect
from forms import ModCompras, Mod_Comercial, Mod_Pricing, Mod_Logistica
from geral import buscar_cnpj

from geral import Validadores, Formatadores, AtualizaCodigo, Buscadores, AlertaMsg
usuario = 'ADMIN'
global alert
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

# as 4 linhas abaixo são utilizadas na ordem de compra
total_ordem_compra = 0
contador_item = 0
lista_contador_item_compra = []
lista_ordem_compra = []  # UTILIZADO EM compras/gerar_ordem_compra


total_cadastro_produto = 0
contador_item_cadastro_produto = 0
lista_contador_cadastro_produto = []
lista_cadastro_produto = []


@app.route('/')
def main():
    return render_template('homepage.html')


@app.route('/admin', methods=['POST', 'GET'])
def admin():
    return render_template('admin.html')


class Compras:

    @staticmethod
    def analisar_nf_pedido_recebido():
        # chamar a função visualizar xml
        # chamar a ordem de compra
        # realizar a análise
        pass

    @staticmethod
    @app.route('/cadastrar_fornecedores', methods=['POST', 'GET'])
    def cadastrar_fornecedores():
        cod_fornecedor = geral.AtualizaCodigo.cod_fornecedor()
        form_fornecedores = ModCompras.CadFornecedores()
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
        alert = None
        # global contador_item_cadastro
        global lista_cadastro_produto
        global total_cadastro_produto
        global lista_contador_cadastro_produto
        contador_item_cadastro_produto = 0
        item_cadastro_produto = []
        form_cad_produtos = ModCompras.CadProduto()
        fornecedores = geral.Buscadores.OrdemCompra.buscar_fornecedor()
        form_cad_produtos.fornecedor.choices = [('Selecionar um fornecedor', 'Selecionar um fornecedor')] + [
            (f[0], f[0]) for f in fornecedores]
        cod_produto = geral.AtualizaCodigo.cod_produto()
        ean = form_cad_produtos.ean.data
        descricao = form_cad_produtos.descricao.data
        unidade = form_cad_produtos.unidade.data
        valor = form_cad_produtos.valor.data
        categoria = form_cad_produtos.categoria.data
        data = Formatadores.os_data()
        fornecedor = form_cad_produtos.fornecedor.data
        usuario = "ADMIN"
        if request.method == 'POST':
            fornecedor = ''
            if 'botao_incluir_item' in request.form: # inclui o item na tabela
                print('botao_incluir_item pressionado')
                fornecedor = request.form.get('fornecedor')  # retorna o fornecedor selecionado e instacia na variável
                try:

                    print(lista_cadastro_produto)

                    def valida_ean_na_lista():
                        print('def verifica_ean_na_lista')
                        if not lista_cadastro_produto: # ou if lista_cadastro_produto == []
                            print('lista vazia')
                            return True
                        for i in lista_cadastro_produto:  # verifica se o item ja existe no pedido
                            print(f'for lista_cadastro_produto {i}')
                            if i[1][1] == ean:
                                print('ean ja existente na lista de itens a cadastrar')
                                return False
                            else:
                                print('ean ainda nao digitado.')
                                return True

                    def valida_campos():
                        print('função valida_campos (verifica se todos os campos foram preenchidos)')
                        if (fornecedor == 'Selecionar um fornecedor'
                                or ean == '' or ean is None
                                or descricao == '' or descricao is None
                                or unidade == '' or unidade is None
                                or valor == '' or valor is None
                                or categoria == '' or categoria is None):
                                alert = geral.AlertaMsg.campos_em_branco()
                                print('>>há um ou mais campos em branco ')
                                return False
                        else:
                            print('>>todos os campos preenchidos')
                            return True

                    def valida_ean_no_banco():
                        print('função valida_ean_no_banco')
                        # valida se o ean existe no banco de dados
                        if geral.Buscadores.buscar_produto_pelo_ean(ean) is False:
                            alert = geral.AlertaMsg.produto_ja_cadastrado(ean)
                            print('>>ean ja existente no banco de dados')
                            return False
                        else:
                            print('>>ean disponível para cadastro')
                            return True
                    print('----------------------')
                    valida_campos = valida_campos()
                    print('----------------------')
                    valida_ean_na_lista = valida_ean_na_lista()
                    print('----------------------')
                    valida_ean_no_banco = valida_ean_no_banco()

                    if valida_campos is True and valida_ean_na_lista is True and valida_ean_no_banco is True:
                        print('Todas as validações foram executadas corretamente')
                        contador_item_cadastro = len(lista_contador_cadastro_produto)
                        contador_item_cadastro_produto += 1
                        lista_contador_cadastro_produto.append(contador_item_cadastro_produto)
                        item_cadastro_produto.append(Formatadores.data_formato_db(data))
                        item_cadastro_produto.append([fornecedor, ean, descricao, unidade, categoria, valor, usuario])
                        lista_cadastro_produto.append(item_cadastro_produto[:])
                        item_cadastro_produto.clear()

                        print(f'lista_cadastro_produto {lista_cadastro_produto}')
                        # A LINHA ABAIXO SERVE PARA SALVAR O FORNECEDOR NA SESSÃO E,
                        # MANTÊ-LO NA TELA AO INCLUIR O ITEM NA TABELA
                        #   (obs.: DEVE SER PASSADO NO RENDER TEMPLATE)
                        session['fornecedor'] = fornecedor
                        alert = geral.AlertaMsg.produto_incluido_na_tabela(ean,descricao)
                        return redirect(url_for('cadastrar_produtos', session=session))
                #
                except Exception as e:
                    print(e)


            if 'botao_submit_cad_prod' in request.form: # inclui as linhas da tabela no banco de dados
                print('botao_submit_cad_prod pressionado')
                try:
                    for i in lista_cadastro_produto:
                        print(i[1][0])
                        print(i[1][1])
                        print(i[1][2])
                        print(i[1][3])
                        print(i[1][4])
                        print(i[1][5])
                        print(i[1][6])
                        data = data
                        # codigo = cod_produto
                        fornecedor = i[1][0]
                        ean = i[1][1]
                        descricao = i[1][2]
                        unidade = i[1][3]
                        categoria = i[1][4]
                        valor = i[1][5]
                        usuario = i[1][6]

                        values = (f"'{date.strftime(data, '%Y-%m-%d')}',"
                                  f"'{cod_produto}',"
                                  f"'{fornecedor}',"
                                  f"'{ean}',"
                                  f"'{descricao}',"
                                  f"'{unidade}',"
                                  f"'{categoria}',"
                                  f"'{valor}',"
                                  f"'{usuario}'")
                        query = (f'INSERT INTO PRODUTOS '
                                 f'(DATA, CODIGO, FORNECEDOR, '
                                 f'EAN, DESCRICAO, UNIDADE, CATEGORIA, VALOR, USUARIO) '
                                 f'VALUES ({values})')

                        print(query)
                        mycursor.execute(query)
                        mycursor.fetchall()
                        fechadb = 'SET SQL_SAFE_UPDATES = 1'
                        mycursor.execute(fechadb)
                        mycursor.fetchall()
                        mydb.commit()
                        alert = AlertaMsg.produto_cadastrado_com_sucesso()

                    lista_cadastro_produto.clear()
                    redirect(url_for('cadastrar_produtos'))
                    return render_template('compras/cadastrar_produtos.html',
                                           alert=alert,
                                           fornecedor=fornecedor,
                                           form_cad_produtos=form_cad_produtos,
                                           cod_produto=AtualizaCodigo.cod_produto(),
                                           data=Formatadores.formatar_data(Formatadores.os_data()))

                except Exception as e:
                    print(e)

                except Exception as e:
                    print('erro ao cadastrar')
                    print(e)
                    AlertaMsg.produto_ja_cadastrado(ean)
                    if 'alert' in session:
                        alert = session.pop('alert', None)
                        return render_template('compras/cadastrar_produtos.html',
                                               alert=alert,
                                               form_cad_produtos=form_cad_produtos,
                                               cod_produto=AtualizaCodigo.cod_produto(),
                                               data=Formatadores.formatar_data(Formatadores.os_data()))

            if 'botao_cancelar_cad_prod' in request.form: # limpa os campos do formulário
                print('botao_cancelar_cad_prod pressionado')
                cod_produto = ean = descricao = unidade = categoria = valor = fornecedor = ''
                lista_cadastro_produto.clear()

            if 'botao_excluir_cad_prod' in request.form:
                valor_produto = request.form.getlist('valor_produto')
                for i in valor_produto:
                    if i != '':
                        valor_produto = i
                        print(f'valor_produto {i}')

                print('---------teste com for simples----------')
                print(f' Itens da lista >>> {len(lista_cadastro_produto)}')

                print(lista_cadastro_produto)
                print(f'Valor produto >>> {valor_produto}')
                for i in lista_cadastro_produto:
                    if valor_produto == i[1][1]:

                        lista_cadastro_produto.remove(i)
                        redirect(url_for('cadastrar_produtos'))
                print('---------fim do teste----------')

        if 'alert' in session:  # Verifica se o alerta existe na sessão, ou seja, verifica se existe alguma condição para envio de 'alert' ser renderizada
            alert = session.pop('alert', None)
        return render_template('compras/cadastrar_produtos.html',
                               alert=alert,
                               fornecedor=fornecedor,
                               form_cad_produtos=form_cad_produtos,
                               dicionario_cad_produtos=lista_cadastro_produto,  # lista_cadastro_produto_cpp
                               cod_produto=AtualizaCodigo.cod_produto(),
                               data=Formatadores.formatar_data(Formatadores.os_data()))

    @staticmethod
    @app.route('/analisar_ordem_de_compra', methods=['POST', 'GET'])
    def analisar_ordem_de_compra():
        resultado = ''
        ordem_compra = ''
        razao_social = ''
        xml = ''
        detalhamento_ordem = ''
        form_analisar_ordem_de_compra = ModCompras.AnalisarOrdemCompra()
        ordem_compra = form_analisar_ordem_de_compra.ordem_compra.data
        razao_social = form_analisar_ordem_de_compra.razao_social.data
        pesquisar_nf = form_analisar_ordem_de_compra.pesquisar_nf.data

        if pesquisar_nf:
            form_analisar_ordem_de_compra.ordem_compra.data = ''

        if request.method == 'POST':
            try:
                if 'botao_pesquisar_notafiscal' in request.form:
                    print('botao_pesquisar_notafiscal ACIONADO')
                    xml = Formatadores.formatar_xml('25240543587344000909550040000020461934533155-nfe')
                    # executar função xml
            except Exception as e:
                print(e)
            try:
                if 'botao_pesquisar_ordem_de_compra' in request.form:
                    print('botao_pesquisar_ordem_de_compra ACIONADO')
                    print(f'Ordem a pesquisar >>> {ordem_compra, razao_social}')
                    resultado = Buscadores.OrdemCompra.buscar_ordem_compra2(ordem_compra, razao_social)

                if 'ordem_para_analise' in request.form: # retorna a opção selecionada na tela
                    ordem_para_analise = request.form.get('ordem_para_analise')
                    detalhamento_ordem = Buscadores.OrdemCompra.buscar_ordem_compra(ordem_para_analise)
                    xml = Formatadores.formatar_xml('25240543587344000909550040000020461934533155-nfe')
                    print(ordem_para_analise)


            except Exception as e:
                print(e)

            try:
                if 'botao_liberar_recebimento' in request.form:
                    print('botao_liberar recebimento ACIONADO')

            except Exception as e:
                print(e)

            try:
                if 'botao_recusar_recebimento' in request.form:
                    print('botao_recusar_recebimento ACIONADO')
            except Exception as e:
                print(e)

        return render_template('compras/analisar_ordem_de_compra.html',
                               xml=xml,
                               retorno_ordem_compra=resultado,
                               detalhamento_ordem=detalhamento_ordem,
                               data=Formatadores.formatar_data(Formatadores.os_data()),
                               form_analisar_ordem_de_compra=form_analisar_ordem_de_compra
                               )

    @staticmethod
    @app.route('/gerar_ordem_compra', methods=['POST', 'GET'])
    def gerar_ordem_compra():

        global contador_item
        global lista_ordem_compra
        global total_ordem_compra
        global result_pesq_forn
        # formatação dos campos

        result_pesq_forn = []
        item_ordem_compra = []
        linha_selecionada = []
        form_gerar_ordem_compra = ModCompras.GerarOrdemCompra()
        data = Formatadores.os_data()
        descricao = form_gerar_ordem_compra.descricao.data
        ordem_compra = form_gerar_ordem_compra.ordem_compra.data
        # fornecedor = form_gerar_ordem_compra.fornecedor.data
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
        if 'ordens_em_aberto' not in session:
            session['ordens_em_aberto'] = 0
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
            result_pesq_forn = ''
            try:

                if 'botao_pesquisar_fornecedor' in request.form:
                    print('botao_pesquisar_fornecedor ACIONADO')
                    fornecedor = form_gerar_ordem_compra.fornecedor.data
                    result_pesq_forn = Buscadores.OrdemCompra.buscar_pelo_fornecedor(fornecedor)
                    print(f'result_pesq_forn SESSION >>> {result_pesq_forn}')
                    session['result_pesq_forn'] = result_pesq_forn
            except Exception as e:
                print(e)

            try:
                if 'botao_selecionar_item' in request.form:

                    result_pesq_forn = session.get('result_pesq_forn', [])  # Recupera da sessão
                    print('botao_selecionar_item ACIONADO')
                    print(f'result_pesq_forn recuperado do botão pesquisar fornecedor {result_pesq_forn}' )

                print('------------------busca ean selecionado-------------------')
                item_selecionado = request.form.getlist('incluir_item')
                for i in item_selecionado:
                    if i != '':
                        item_selecionado = i
                print(item_selecionado)
                print('--------------------xxxxxxxxxxxx--------------------------')
                print('-------FORMATA LINHAS PARA IDENTIFICAR A POSIÇÃO----------')
                conta_linha = 0
                pos_pesquisa = ''
                linha_selecionada = []
                print(result_pesq_forn)
                for i in result_pesq_forn:
                    # print(item_selecionado, i)
                    if i[3] == item_selecionado:
                        # print(i[3])
                        pos_pesquisa = conta_linha
                        linha_selecionada.append(i)
                        print(f'o item selecionado está na linha {conta_linha}')
                        print(f'linha selecionada >>>{linha_selecionada[0]}')
                    conta_linha += 1
                # # print(f'o item está na linha {pos_pesquisa}')
                # print(f'lista_itens >>> {item_selecionado}')
                print('--------------------xxxxxxxxxxxx--------------------------')
                print('------RETORNAR INFORMAÇÕES SELECIONADAS PARA O HTML-------')
                linha_selecionada = linha_selecionada[0]
                print(linha_selecionada)


            except Exception as e:
                print(e)
            # pesquisar item pelo código. no momento está sem uso
            try:
                result_pesq_forn = session.get('result_pesq_forn', [])  # Recupera da sessão
                if 'botao_pesquisar_item' in request.form:
                    print('botao_pesquisar_item ACIONADO')
                    if descricao == '' and ean == '':
                        resultado = Buscadores.buscar_produto_pelo_codigo(codigo)
                        resultado = resultado[0]
                    if codigo == '' and descricao == '':
                        resultado = Buscadores.buscar_produto_pelo_ean(ean)
                        resultado = resultado[0]
                    if resultado is None:
                        pass
                    print(resultado)

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

            # inclui o item pesquisado na tabela que conterá os itens da ordem de compra
            try:
                result_pesq_forn = session.get('result_pesq_forn', [])  # Recupera da sessão
                if 'botao_incluir_item' in request.form:
                    print('botao_incluir_item ACIONADO')
                    try:

                        # Formatadores.preparar_item_ordem_compra()
                        print('teste')
                        contador_item = len(lista_contador_item_compra)
                        print(f'max lista contador item {max(lista_contador_item_compra)}')

                    except Exception as e:
                        print(e)
                        contador_item = 0
                    #  TRANSFORMAR EM FUNÇÃO
                    contador_item += 1
                    print(contador_item)
                    lista_contador_item_compra.append(contador_item)
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
                if 'botao_consulta' in request.form:
                    print('botao_consulta pressionado')

            except Exception as e:
                print(e)

            try:
                if 'botao_submit_compra' in request.form:
                    print('botao_submit_compra pressionado')
                    cont_temp = 1
                    while cont_temp <= len(lista_ordem_compra):
                        print(f' len de lista_ordem_compra >>>> {len(lista_ordem_compra)}')
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
                            mydb.connect()
                            mycursor.execute(query)
                            mycursor.fetchall()
                            fechadb = 'SET SQL_SAFE_UPDATES = 1'
                            mycursor.execute(fechadb)
                            mycursor.fetchall()
                            mydb.commit()
                            mydb.close()
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

            if result_pesq_forn is None:
                result_pesq_forn = 0


        return render_template('compras/gerar_ordem_compra.html',
                               alert=alert,
                               linha_selecionada=linha_selecionada,
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
                               result_pesq_forn=result_pesq_forn,
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


class Logistica:
    @staticmethod
    @app.route('/entrada_ordem_compra', methods=['POST', 'GET'])
    def entrada_ordem_compra():

        form_entrada_ordem_compra = Mod_Logistica.EntradaOrdemCompra()
        nome_fantasia = form_entrada_ordem_compra.nome_fantasia.data
        ordem_compra = form_entrada_ordem_compra.ordem_compra.data




        return render_template('logistica/entrada_ordem_compra.html',
                               form_entrada_ordem_compra=form_entrada_ordem_compra,
                               nome_fantasia=nome_fantasia,
                               ordem_compra=ordem_compra,
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


@app.route('/financeiro', methods=['POST', 'GET'])
def financeiro():
    return render_template('financeiro.html', data=Formatadores.formatar_data(Formatadores.os_data()))


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
