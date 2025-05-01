# outras bibliotecas
from datetime import date
import mysql.connector

# flask
from flask import render_template, redirect, url_for, request, session
# from flask_wtf.csrf import CSRFProtect

import modulos.admin
from forms import ModCompras

# geral
from geral import Formatadores, AtualizaCodigo, Buscadores, AlertaMsg
import geral

mydb = mysql.connector.connect(
    host="localhost", user="admin2024", password="204619", database="projeto_erp"
)
mycursor = mydb.cursor()

# inicialização de variáveis
total_ordem_compra = 0
contador_item = 0
lista_contador_item_compra = []
lista_ordem_compra = []  # UTILIZADO EM compras/gerar_ordem_compra
total_cadastro_produto = 0
contador_item_cadastro_produto = 0
lista_contador_cadastro_produto = []
lista_cadastro_produto = []
datalista_cadastro_produto = []
result_pesq_forn = None


def cadastrar_fornecedores():
    cod_fornecedor = geral.AtualizaCodigo.cod_fornecedor()
    form_fornecedores = ModCompras.CadFornecedores()
    nome_fantasia = form_fornecedores.nome_fantasia.data
    razao_social = form_fornecedores.razao_social.data
    cnpj = form_fornecedores.cnpj.data
    inscricaoestadual = form_fornecedores.insc_estadual.data
    email = form_fornecedores.email.data
    cep = form_fornecedores.cep.data
    telefone = form_fornecedores.telefone.data
    endereco = form_fornecedores.endereco.data
    municipio = form_fornecedores.municipio.data
    uf = form_fornecedores.uf.data
    data = Formatadores.os_data()

    if "botao_submit_cad_fornecedor" in request.form:
        if geral.Validadores.valida_cnpj(form_fornecedores.cnpj.data) is False:
            alert = geral.AlertaMsg.cnpj_invalido()

        if (geral.Validadores.valida_cnpj(form_fornecedores.cnpj.data) is True and
                Buscadores.buscar_cnpj(form_fornecedores.cnpj.data) is True):
            alert = geral.AlertaMsg.cnpj_ja_existente()

        if (geral.Validadores.valida_cnpj(form_fornecedores.cnpj.data) is True and
                Buscadores.buscar_cnpj(form_fornecedores.cnpj.data) is False):
            print("informações validadas - cadastrar no banco de dados")
            values = (
                f"'{date.strftime(data, '%Y-%m-%d')}',"
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
                f"'{uf}'"
            )
            query = (
                f"INSERT INTO FORNECEDORES "
                f"(DATA, CODIGO, NOMEFANTASIA, RAZAOSOCIAL, CNPJ, INSCRICAOESTADUAL, EMAIL, "
                f"TELEFONE, CEP, ENDERECO, MUNICIPIO, UF) "
                f"VALUES ({values})"
            )
            print(query)
            mycursor.execute(query)
            mycursor.fetchall()
            fechadb = "SET SQL_SAFE_UPDATES = 1"
            mycursor.execute(fechadb)
            mycursor.fetchall()
            mydb.commit()
            alert = geral.AlertaMsg.cad_fornecedor_realizado()
            geral.AtualizaCodigo.cod_fornecedor()
            return redirect(url_for("cadastrar_fornecedores"))

    alert = session.pop("alert", None)

    return render_template(
        "compras/cadastrar_fornecedores.html",
        alert=alert,
        form_fornecedores=form_fornecedores,
        cod_fornecedor=geral.AtualizaCodigo.cod_fornecedor(),
        data=Formatadores.formatar_data(Formatadores.os_data()),
    )


def cadastrar_produtos():
    alert = None

    # global contador_item_cadastro
    global lista_cadastro_produto
    global total_cadastro_produto
    global lista_contador_cadastro_produto

    contador_item_cadastro_produto = 0
    item_cadastro_produto = []
    form_cad_produtos = ModCompras.CadProduto()
    # fornecedores = geral.Buscadores.OrdemCompra.buscar_fornecedor()
    # form_cad_produtos.fornecedor.choices = [
    #     ("Selecionar um fornecedor", "Selecionar um fornecedor")
    # ] + [(f[0], f[0]) for f in fornecedores]
    cod_produto = geral.AtualizaCodigo.cod_produto()
    ean = form_cad_produtos.ean.data
    descricao = form_cad_produtos.descricao.data
    unidade = form_cad_produtos.unidade.data
    valor = form_cad_produtos.valor.data
    categoria = form_cad_produtos.categoria.data
    data = Formatadores.os_data()
    fornecedor = form_cad_produtos.fornecedor.data
    session["fornecedor"] = fornecedor
    usuario = "ADMIN"

    # session['fornecedor'] = fornecedor

    # funções validadoras do item digitado na ordem de compra
    def valida_ean_na_lista():
        print(
            geral.CorFonte.fonte_amarela()
            + "função verifica_ean_na_lista"
            + geral.CorFonte.reset_cor()
        )
        if not lista_cadastro_produto:  # ou if lista_cadastro_produto == []
            print("lista vazia")
            return True
        for i in lista_cadastro_produto:  # verifica se o item ja existe no pedido
            print(f"informações para incluir na tabela\n {i}")
            if i[1][1] == ean:
                print("ean ja existente na lista de itens a cadastrar")
                return False
            else:
                print("ean ainda nao digitado.")
                return True

    def valida_campos():
        print("função valida_campos (verifica se todos os campos foram preenchidos)")
        if (
            fornecedor == "Selecionar um fornecedor"
            or ean == ""
            or ean is None
            or descricao == ""
            or descricao is None
            or unidade == ""
            or unidade is None
            or valor == ""
            or valor is None
            or categoria == ""
            or categoria is None
        ):
            print(">>há um ou mais campos em branco ")
            return False
        else:
            print(">>todos os campos preenchidos")
            return True

    def valida_ean_no_banco():
        print("função valida_ean_no_banco")
        # valida se o ean existe no banco de dados
        if geral.Buscadores.buscar_produto_pelo_ean(ean) is False:
            print(">>ean ja existente no banco de dados")
            return False
        else:
            print(">>ean disponível para cadastro")
            return True

    if request.method == "POST":
        if "botao_baixar_planilha" in request.form:
            print("botao_baixar_planilha pressionado")
            geral.download_planilha()

        # fornecedor = ''
        if "botao_incluir_item" in request.form:  # inclui o item na tabela
            print(
                geral.CorFonte.fonte_amarela()
                + "botao_incluir_item acionado"
                + geral.CorFonte.reset_cor()
            )
            valida_campos = valida_campos()
            valida_ean_na_lista = valida_ean_na_lista()
            valida_ean_no_banco = valida_ean_no_banco()
            print(
                geral.CorFonte.fonte_amarela()
                + "1 - Verifica se os campos estão validados"
                + geral.CorFonte.reset_cor()
            )

            #  *função* que será executada caso todos os campos sejam validados
            try:
                if (
                    valida_campos is True
                    and valida_ean_na_lista is True
                    and valida_ean_no_banco is True
                ):
                    print("Todas as validações foram executadas corretamente")
                    contador_item_cadastro = len(lista_contador_cadastro_produto)
                    contador_item_cadastro_produto += 1
                    lista_contador_cadastro_produto.append(
                        contador_item_cadastro_produto
                    )
                    item_cadastro_produto.append(Formatadores.data_formato_db(data))
                    item_cadastro_produto.append(
                        [fornecedor, ean, descricao, unidade, categoria, valor, usuario]
                    )
                    lista_cadastro_produto.append(item_cadastro_produto[:])
                    item_cadastro_produto.clear()

                    print(f"lista_cadastro_produto {lista_cadastro_produto}")
                    # A LINHA ABAIXO SERVE PARA SALVAR O FORNECEDOR NA SESSÃO E,
                    # MANTÊ-LO NA TELA AO INCLUIR O ITEM NA TABELA
                    #   (obs.: DEVE SER PASSADO NO RENDER TEMPLATE)

                    fornecedor = session.get("fornecedor")
                    alert = geral.AlertaMsg.produto_incluido_na_tabela(ean, descricao)
                    # return redirect(url_for('cadastrar_produtos') + f'?fornecedor={fornecedor}')
                    print(f"fornecedor recuperado no botao incluir item {fornecedor}")
                    return render_template(
                        "compras/cadastrar_produtos.html",
                        fornecedor=fornecedor,
                        form_cad_produtos=form_cad_produtos,
                        data=data,
                        alert=alert,
                    )

                # caso alguma validação falhe

                if valida_campos is False:
                    print("Função valida_campos is False")
                    alert = geral.AlertaMsg.campos_em_branco()
                    return render_template(
                        "compras/cadastrar_produtos.html",
                        fornecedor=fornecedor,
                        form_cad_produtos=form_cad_produtos,
                        data=data,
                        alert=alert,
                    )

                if valida_ean_no_banco is False:
                    print("Função valida_ean_no_banco is False")
                    alert = geral.AlertaMsg.produto_ja_cadastrado(ean)
                    return render_template(
                        "compras/cadastrar_produtos.html",
                        fornecedor=fornecedor,
                        form_cad_produtos=form_cad_produtos,
                        data=data,
                        alert=alert,
                    )

                if valida_ean_na_lista is False:
                    print("Função valida_ean_na_lista is False")
                    alert = geral.AlertaMsg.ean_ja_digitado(ean)
                    return render_template(
                        "compras/cadastrar_produtos.html",
                        fornecedor=fornecedor,
                        form_cad_produtos=form_cad_produtos,
                        data=data,
                        alert=alert,
                    )

            except Exception as e:
                print(e)

            finally:
                return redirect(url_for("cadastrar_produtos"))

        # inclui as linhas da tabela no banco de dados
        if "botao_submit_cad_prod" in request.form:
            print("botao_submit_cad_prod pressionado")
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

                    values = (
                        f"'{date.strftime(data, '%Y-%m-%d')}',"
                        f"'{cod_produto}',"
                        f"'{fornecedor}',"
                        f"'{ean}',"
                        f"'{descricao}',"
                        f"'{unidade}',"
                        f"'{categoria}',"
                        f"'{valor}',"
                        f"'{usuario}'"
                    )
                    query = (
                        f"INSERT INTO PRODUTOS "
                        f"(DATA, CODIGO, FORNECEDOR, "
                        f"EAN, DESCRICAO, UNIDADE, CATEGORIA, VALOR, USUARIO) "
                        f"VALUES ({values})"
                    )

                    print(query)
                    mycursor.execute(query)
                    mycursor.fetchall()
                    fechadb = "SET SQL_SAFE_UPDATES = 1"
                    mycursor.execute(fechadb)
                    mycursor.fetchall()
                    mydb.commit()
                    alert = AlertaMsg.produto_cadastrado_com_sucesso()

                lista_cadastro_produto.clear()
                redirect(url_for("cadastrar_produtos"))
                return render_template(
                    "compras/cadastrar_produtos.html",
                    alert=alert,
                    fornecedor=fornecedor,
                    form_cad_produtos=form_cad_produtos,
                    cod_produto=AtualizaCodigo.cod_produto(),
                    data=Formatadores.formatar_data(Formatadores.os_data()),
                )

            except Exception as e:
                print("erro ao cadastrar")
                print(e)
                AlertaMsg.produto_ja_cadastrado(ean)
                if "alert" in session:
                    alert = session.pop("alert", None)
                    return render_template(
                        "compras/cadastrar_produtos.html",
                        alert=alert,
                        form_cad_produtos=form_cad_produtos,
                        cod_produto=AtualizaCodigo.cod_produto(),
                        data=Formatadores.formatar_data(Formatadores.os_data()),
                    )

        if "botao_cancelar_cad_prod" in request.form:  # limpa os campos do formulário
            print("botao_cancelar_cad_prod pressionado")
            cod_produto = ean = descricao = unidade = categoria = valor = fornecedor = (
                ""
            )
            lista_cadastro_produto.clear()

        if "botao_baixar_planilha" in request.form:
            print("botao_baixar_planilha pressionado")
            print("Criar planilha com pandas")

        if "botao_excluir_cad_prod" in request.form:
            valor_produto = request.form.getlist("valor_produto")
            for i in valor_produto:
                if i != "":
                    valor_produto = i
                    print(f"valor_produto {i}")

            print("---------teste com for simples----------")
            print(f" Itens da lista >>> {len(lista_cadastro_produto)}")

            print(lista_cadastro_produto)
            print(f"Valor produto >>> {valor_produto}")
            for i in lista_cadastro_produto:
                if valor_produto == i[1][1]:
                    lista_cadastro_produto.remove(i)
                    redirect(url_for("cadastrar_produtos"))
            print("---------fim do teste----------")

    # Verifica se o alerta existe na sessão, ou seja,
    # verifica se existe alguma condição para envio de 'alert' ser renderizada
    if "alert" in session:
        alert = session.pop("alert", None)
    return render_template(
        "compras/cadastrar_produtos.html",
        alert=alert,
        fornecedor=fornecedor,
        form_cad_produtos=form_cad_produtos,
        dicionario_cad_produtos=lista_cadastro_produto,  # lista_cadastro_produto_cpp
        cod_produto=AtualizaCodigo.cod_produto(),
        data=Formatadores.formatar_data(Formatadores.os_data()),
    )


def analisar_ordem_de_compra():
    resultado = ""
    ordem_compra = ""
    razao_social = ""
    xml = ""
    itens_xml = ""
    detalhamento_ordem = ""
    form_analisar_ordem_de_compra = ModCompras.AnalisarOrdemCompra()
    nf = form_analisar_ordem_de_compra.nf.data
    ordem_compra = form_analisar_ordem_de_compra.ordem_compra.data
    razao_social = form_analisar_ordem_de_compra.razao_social.data
    pesquisar_nf = form_analisar_ordem_de_compra.pesquisar_nf.data

    if pesquisar_nf:
        form_analisar_ordem_de_compra.ordem_compra.data = ""

    if request.method == "POST":
        try:
            if "botao_pesquisar_notafiscal" in request.form:
                print("botao_pesquisar_notafiscal ACIONADO")
        except Exception as e:
            print("erro ao pesquisar nf")
            print(e)
        try:
            lista_teste = []
            if "botao_pesquisar_ordem_de_compra" in request.form:
                print("botao_pesquisar_ordem_de_compra ACIONADO")
                print(f"Ordem a pesquisar >>> {ordem_compra, razao_social, nf}")
                # faz a busca na base de dados pela ordem de compra, ou pela razao social,  ou por ambos
                resultado = Buscadores.OrdemCompra.buscar_ordem_compra2(ordem_compra, razao_social)
            status_ordem = Buscadores.OrdemCompra.verifica_status_ordem(ordem_compra)
            if ("ordem_para_analise" in request.form):  # retorna a opção selecionada na tela
                print("Ordem_para_analise ACIONADO")

                ordem_para_analise = request.form.get("ordem_para_analise")
                detalhamento_ordem = Buscadores.OrdemCompra.buscar_ordem_compra(
                    ordem_para_analise
                )
                print(f"detalhamento_ordem >>> {detalhamento_ordem}")

                print("------------Teste funçoes validadoras----------")
                print(geral.ValidaStatusPedido.validacao_1(status_ordem))

                nome_arquivo = Buscadores.Xml.buscar_arquivo(nf)
                print(f"nome_arquivo = {nome_arquivo}")
                cnpj = Buscadores.Xml.buscar_cnpj(nome_arquivo)

                print(geral.ValidaStatusPedido.validacao_2(cnpj))
                print(f"cnpj = {cnpj}")
                print(geral.ValidaStatusPedido.validacao_3(status_ordem, ordem_compra))
                print(geral.ValidaStatusPedido.validacao_4(nf, ordem_compra))
                print("---------fim do teste funçoes validadoras------\n")

                print("---------teste valida status pedido------\n")
                geral.Validadores.valida_status_pedido(ordem_compra)

                print("---------fim do teste valida status pedido------\n")

                for i in detalhamento_ordem:  # itens da ordem de compra
                    lista_cadastro_produto.append(i)
                    # print(i[7])
                print(lista_teste)
                itens__nf = geral.Buscadores.Xml.retorna_xml(str(nf))
                xml = Formatadores.formatar_xml(itens__nf)  # retorna o xml
                print(ordem_para_analise)

        except Exception as e:
            print("erro ao pesquisar nf")
            print(e)

        try:
            if "botao_liberar_recebimento" in request.form:
                print("botao_liberar recebimento ACIONADO")

        except Exception as e:
            print("erro ao liberar recebimento")
            print(e)

        try:
            if "botao_recusar_recebimento" in request.form:
                print("botao_recusar_recebimento ACIONADO")
        except Exception as e:
            print("erro ao recusar recebimento")
            print(e)

    return render_template(
        "compras/analisar_ordem_de_compra.html",
        xml=xml,
        itens_xml=itens_xml,
        itens_oc=0,
        retorno_ordem_compra=resultado,
        detalhamento_ordem=detalhamento_ordem,
        data=Formatadores.formatar_data(Formatadores.os_data()),
        form_analisar_ordem_de_compra=form_analisar_ordem_de_compra,
    )


def gerar_ordem_compra():
    print(geral.CorFonte.fonte_amarela() + "Função gerar_ordem_compra" + geral.CorFonte.reset_cor())
    """
    1. USUÁRIO DEFINE O FORNECEDOR E CLICA EM PESQUISAR FORNECEDOR
    2. BACKEND: 
     . result_pesq_forn = Buscadores.OrdemCompra.buscar_pelo_fornecedor(
                    fornecedor
     . RENDERIZA NO HTML OS PRODUTOS DO FORNECEDOR JÁ CADASTRADOS 
    3. O USUÁRIO CLICA EM UM PRODUTO
    4. BACKEND: 
     . item_selecionado = busca_ean_selecionado(item_selecionado)
     . linha_selecionada = formata_linha_para_identificar_posicao(
                item_selecionado, result_pesq_forn
            )
     . linha_selecionada = linha_selecionada[0]
     4.1 RENDERIZA O ITEM NA TELA COM OS CAMPOS QTDE E VALOR
     5. O USUARIO CLICA EM INCLUIR ITEM
     6. BACKEND:
      . VALIDA SE O EAN JÁ FOI DIGITADO NA LISTA FINAL
      . EXECUTA SubFunção "atualizar_lista_ordem_compra"
     7. O USUARIO CLICA EM GERAR ORDEM DE COMPRA
     8. BACKEND:
      . ATUALIZA BANCO DE DADOS, TABELA ORDEM_COMPRA
      * CAMPOS DO BANCO DE DADOS:
        . DATA
        . ORDEM_COMPRA
        . ITEM
        . DESCRICAO
        . UNIDADE
        . CATEGORIA
        . CODIGO
        . EAN    
        . QTDE
        . PRECO
        . TOTAL_ITEM
        . SALDO_QTD
        . SALDO_TOTAL_ITEM
        . STATUS
        . USUARIO
             
    """

    # 1 - Definição das variáveis globais
    global contador_item
    global lista_ordem_compra
    global total_ordem_compra
    global result_pesq_forn

    # 2 - Inicialização das variáveis
    total_ordem_compra = 0
    result_pesq_forn = []
    item_ordem_compra = []
    linha_selecionada = []
    form_gerar_ordem_compra = ModCompras.GerarOrdemCompra()
    data = Formatadores.os_data()
    descricao = form_gerar_ordem_compra.descricao.data
    ordem_compra = form_gerar_ordem_compra.ordem_compra.data
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

    if "total_ordem_compra" not in session:
        session["total_ordem_compra"] = 0
    if "preco_medio" not in session:
        session["preco_medio"] = 0
    if "ultimo_preco" not in session:
        session["ultimo_preco"] = 0
    if "preco_historico" not in session:
        session["preco_historico"] = 0
    if "ordens_em_aberto" not in session:
        session["ordens_em_aberto"] = 0

    try:
        if preco_unitario is not None:
            preco_unitario = preco_unitario.replace(",", ".")
        else:
            pass

        if preco_unitario is None or quantidade is None:
            total_item = 0

        else:
            total_item = quantidade * preco_unitario

    except Exception as e:
        print("total_item = quantidade * preco_unitario")
        print(e)
        total_item = 0

    if preco_medio is None:
        preco_medio = 0
    if preco_historico is None:
        preco_historico = 0
    if ultimo_preco is None:
        ultimo_preco = 0
    resultado = None
    lista_ean_temp = []
    lista_ean = []

    def busca_ean_selecionado(item_selecionado):
        print(
            geral.CorFonte.fonte_amarela()
            + "Função gerar_ordem_compra\n subfunção busca_ean_selecionado"
            + geral.CorFonte.reset_cor()
        )
        print(f"EAN selecionado: {item_selecionado}")
        for i in item_selecionado:
            if i != "":
                item_selecionado = i
        return item_selecionado

    def formata_linha_para_identificar_posicao(item_selecionado, result_pesq_forn):
        print(
            geral.CorFonte.fonte_amarela()
            + "Função gerar_ordem_compra_subfunção formata_linha_para_identificar_posicao"
            + geral.CorFonte.reset_cor()
        )
        conta_linha = 0
        print(f"item_selecionado: {item_selecionado} || ean: {ean}")
        pos_pesquisa = ""
        linha_selecionada = []
        for i in result_pesq_forn:
            if i[3] == item_selecionado:
                print(f"lista_ordem_compra: {lista_ordem_compra}")
                # for i in lista_ordem_compra:
                #     print(f'loop for i: {i}')
                pos_pesquisa = conta_linha
                linha_selecionada.append(i)
                print(f"o item selecionado está na linha {conta_linha}")
                # print(f'linha selecionada >>>{linha_selecionada[0]}')
            conta_linha += 1
        return linha_selecionada

    # 4 - Processamentos
    if request.method == "POST":
        item_ordem_compra.clear()
        result_pesq_forn = ""
        try:
            if "botao_pesquisar_fornecedor" in request.form:
                print("botao_pesquisar_fornecedor ACIONADO")
                fornecedor = form_gerar_ordem_compra.fornecedor.data
                print(f"Fornecedor: {fornecedor}")
                session["fornecedor"] = fornecedor
                result_pesq_forn = Buscadores.OrdemCompra.buscar_pelo_fornecedor(
                    fornecedor
                )
                # print(f'result_pesq_forn SESSION >>> {result_pesq_forn}')
                session["result_pesq_forn"] = result_pesq_forn
        except Exception as e:
            print("erro no botao_pesquisar_fornecedor")
            print(e)

        try:
            if "botao_selecionar_item" in request.form:
                print("botao_selecionar_item ACIONADO")
                result_pesq_forn = session.get("result_pesq_forn")  # Recupera da sessão
                item_selecionado = request.form.getlist("incluir_item")
                item_selecionado = busca_ean_selecionado(item_selecionado)
                print(f"ean do item selecionado: {item_selecionado}")

                fornecedor = session.get("fornecedor")
                # print(f'teste fornecedor após acionamento do botao_selecionar_item {fornecedor}')

            print(
                f"ean do item selecionado para adicionar à ordem de compra: {item_selecionado}"
            )
            # executado após o acionamento de "botao_selecionar_item"
            linha_selecionada = formata_linha_para_identificar_posicao(
                item_selecionado, result_pesq_forn
            )
            linha_selecionada = linha_selecionada[0]
            print(
                f"linha_selecionada para incluir à ordem de compra: {linha_selecionada}"
            )
        except Exception as e:
            print("erro no botao_selecionar_item")
            print(f"linha_selecionada: {linha_selecionada}")
            # print(f'linha_selecionada[0]: {linha_selecionada[0]}')
            print(e)

        try:
            result_pesq_forn = session.get("result_pesq_forn", [])  # Recupera da sessão
            fornecedor = session.get("fornecedor")
            if "botao_incluir_item" in request.form:
                print("botao_incluir_item ACIONADO")

                for i in lista_ordem_compra:
                    print(f"{i[6]} ||| ean a incluir na ordem: {ean}")
                    if i[6] == ean:
                        print(
                            geral.CorFonte.fonte_vermelha()
                            + "item já digitado na ordem de compra"
                            + geral.CorFonte.reset_cor()
                        )
                        break
                    else:
                        try:
                            contador_item = len(lista_contador_item_compra)
                        except Exception as e:
                            print(
                                "erro no contador_item = len(lista_contador_item_compra)"
                            )
                            print(e)
                            contador_item = 0
                        contador_item += 1
                        print(f"Item {contador_item} incluído ")

                def atualizar_lista_ordem_compra():
                    """
                     Atualiza as listas relacionadas à ordem de compra com base nos dados do front-end.

                     1. Adiciona as informações do item atual à lista `item_ordem_compra`.
                     2. Copia o conteúdo de `item_ordem_compra` para a lista `lista_ordem_compra` e a limpa.
                     3. Calcula o total da ordem de compra somando o preço total do item atual.
                    :return: Tupla contendo o total da ordem de compra e a lista `lista_ordem_compra`.
                    """
                    print(
                        geral.CorFonte.fonte_amarela()
                        + f"FUNÇÃO GERAR_ORDEM_COMPRA | SubFunção atualizar_lista_ordem_compra"
                        + geral.CorFonte.reset_cor()
                    )
                    print(
                        f"contador_item: {contador_item} |\n"
                        f"data: {data} |\n"
                        f"ordem_compra: {ordem_compra} |\n"
                        f"descricao: {descricao} |\n"
                        f"unidade: {unidade} |\n"
                        f"categoria: {categoria} |\n"
                        f"codigo: {codigo} |\n"
                        f"ean: {ean} |\n"
                        f"quantidade: {quantidade} |\n"
                        f"preco_unitario: {preco_unitario} |\n"
                    
                        f"total_item: {total_item}"
                    )

                    total_ordem_compra = 0
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
                    # print(lista_ordem_compra)
                    item_ordem_compra.clear()
                    total_ordem_compra += lista_ordem_compra[-1][9]
                    print(f'lista_ordem_compra: {lista_ordem_compra}')
                    return total_ordem_compra, lista_ordem_compra

                total_ordem_compra = atualizar_lista_ordem_compra()

        except Exception as e:
            print("erro no botao_incluir_item")
            print(e)

        try:
            if "botao_consulta" in request.form:
                fornecedor = session.get("fornecedor")
                print(
                    f"teste fornecedor após acionamento do botao_consulta {fornecedor}"
                )
                print("botao_consulta pressionado")

        except Exception as e:
            print("erro no botao_consulta")
            print(e)

        try:
            if "botao_submit_compra" in request.form:
                print("botao_submit_compra ACIONADO")
                cont_temp = 1
                print(f"lista_ordem_compra {lista_ordem_compra}")
                # print(f"len de lista_ordem_compra >>>> {len(lista_ordem_compra)}")
                while cont_temp <= len(lista_ordem_compra):
                    for i in lista_ordem_compra:
                        print(f"i linha {cont_temp} >>>> {i}")
                        values = (
                            f"'{date.strftime(data, '%Y-%m-%d')}',"  # data
                            f"'{i[1]}',"  # ordem
                            f"'{cont_temp}',"  # item
                            f"'{i[2]}',"  # descricao
                            f"'{i[3]}',"  # unidade
                            f"'{i[4]}',"  # categoria
                            f"'{i[5]}',"  # codigo
                            f"'{i[6]}',"  # ean
                            f"'{i[7]}',"  # quantidade
                            f"'{i[8]}',"  # preco
                            f"'{(int(i[7]) * int(i[8]))}',"  # total_item
                            f"'{i[7]}',"
                            f"'{(int(i[7]) * int(i[8]))}',"  # saldo total_item
                            f"'{'PENDENTE'}',"
                            f"'{modulos.admin.usuario}'"
                        )
                        print(f"values >>>> {values}")
                        query = (
                            f"INSERT INTO ORDEM_COMPRA"
                            f"(DATA, ORDEM_COMPRA, ITEM, DESCRICAO, UNIDADE, CATEGORIA, "
                            f"CODIGO, EAN, QUANTIDADE, PRECO, TOTAL_ITEM, SALDO_QTD, SALDO_TOTAL_ITEM, STATUS, USUARIO)"
                            f" VALUES ({values});"
                        )

                        print(f"Query {cont_temp} >>>> {query}")
                        mydb.connect()
                        mycursor.execute(query)
                        mycursor.fetchall()
                        fechadb = "SET SQL_SAFE_UPDATES = 1"
                        mycursor.execute(fechadb)
                        mycursor.fetchall()
                        mydb.commit()
                        mydb.close()
                        cont_temp += 1

                    # alert = AlertaMsg.produto_cadastrado_com_sucesso()
                    # session["alert"] = alert

                    # geral.AtualizaCodigo.ordem_compra()


                    lista_ordem_compra.clear()  # limpa a lista para a proxima ordem de compra

                return redirect(url_for("gerar_ordem_compra"))

        except Exception as e:
            print("erro no botao_submit_compra")
            print(e)

        try:
            if "botao_limpar_ordem" in request.form:
                print("botao_limpar_ordem pressionado")
                lista_ordem_compra.clear()
                total_ordem_compra = 0
                # ultimo_preco = 0
                # preco_medio = 0

                return redirect(url_for("gerar_ordem_compra"))

        except Exception as e:
            print("erro no botao_limpar_ordem")
            print(e)

        alert = session.pop("alert", None)

        if result_pesq_forn is None:
            result_pesq_forn = 0

    return render_template(
        "compras/gerar_ordem_compra.html",
        alert=alert,
        # fornecedor=fornecedor,
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
        data=Formatadores.formatar_data(Formatadores.os_data()),
    )


def editar_ordem_compra():
    print("função editar_ordem_compra")
    form_editar_ordem_compra = ModCompras.EditarOrdemCompra()
    ordem_compra = request.form.get("pesquisar_ordem_compra")
    session["ordem_compra"] = ordem_compra

    ordem_pesquisada = Buscadores.OrdemCompra.buscar_ordem_compra(ordem_compra)
    session["result_ordem_pesquisada"] = ordem_pesquisada
    ordem_pesquisada = ()  # Valor padrão para evitar o erro no primeiro acesso
    if request.method == "POST":
        ean = ""
        quantidade = ""
        val_unitario = ""

        if "botao_pesquisar_ordem_compra" in request.form:
            status = 'PENDENTE'
            print("botao pesquisar ordem_compra acionado")
            if ordem_compra:  # Verifica se o campo 'ordem_compra' está preenchido
                try:
                    ordem_pesquisada = session.get("result_ordem_pesquisada")
                    ordem_compra = request.form.get("pesquisar_ordem_compra")
                    print(f"ordem_compra: {ordem_compra}")
                    session["ordem_compra"] = ordem_compra
                    print(f"ordem_pesquisada antes da modificação: {ordem_pesquisada}")
                    # ✅ Inicializa `nova_ordem_pesquisada` como uma lista vazia para evitar erro
                    nova_ordem_pesquisada = []
                    if ordem_pesquisada:
                        # Criar uma nova lista de tuplas com o status incluído
                        nova_ordem_pesquisada = [i + (status,) for i in ordem_pesquisada]
                        print(f"ordem_pesquisada modificada: {nova_ordem_pesquisada}")

                        # Atualiza a session com os novos valores
                        session["ordem_pesquisada"] = nova_ordem_pesquisada
                    for i in nova_ordem_pesquisada:
                        print(i)
                except Exception as e:
                    print(f"Erro ao buscar ordem de compra: {e}")

            else:
                print("Nenhuma ordem de compra informada para a pesquisa.")

            return render_template(
                "compras/editar_ordem_compra.html",
                ordem_compra=ordem_compra,
                ordem_pesquisada=nova_ordem_pesquisada,
                form_editar_ordem_compra=form_editar_ordem_compra,
                linha_para_editar="",
                data=Formatadores.formatar_data(Formatadores.os_data()),
            )

        if "botao_editar_item" in request.form:
            print("botao_editar_item acionado")
            ordem_pesquisada = session.get("ordem_pesquisada")
            ordem_compra = session.get("ordem_compra")
            item_selecionado = request.form.getlist("editar__item")
            item_selecionado = item_selecionado[0]
            linha_para_editar = []
            for i in ordem_pesquisada:
                if i[7] == item_selecionado:
                    linha_para_editar.append(i)
                    print(i)
                    session["linha_para_editar"] = linha_para_editar

            if linha_para_editar:
                ean = linha_para_editar[0][7]  #
                form_editar_ordem_compra.ean.data = (
                    ean  # Define o valor no campo 'ean' do formulário
                )
                session["ean"] = ean
                quantidade = linha_para_editar[0][8]
                form_editar_ordem_compra.quantidade.data = quantidade
                session["quantidade"] = quantidade

                val_unitario = linha_para_editar[0][9]
                form_editar_ordem_compra.val_unitario.data = val_unitario
                session["valor_unitario"] = val_unitario

                ordem_compra = linha_para_editar[0][1]
                session["ordem_compra"] = ordem_compra
                form_editar_ordem_compra.descricao.data = linha_para_editar[0][3]

            print(f"linha_para_editar {linha_para_editar}")
            print(f"ordem_pesquisada: {ordem_pesquisada}")
            session["ordem_pesquisada"] = ordem_pesquisada
            session["ordem_compra"] = ordem_compra
            # print(f'item_selecionado: {item_selecionado}')
            return render_template(
                "compras/editar_ordem_compra.html",
                ordem_compra=ordem_compra,
                quantidade=quantidade,
                val_unitario=val_unitario,
                linha_para_editar=linha_para_editar,
                ordem_pesquisada=ordem_pesquisada,
                form_editar_ordem_compra=form_editar_ordem_compra,
                data=Formatadores.formatar_data(Formatadores.os_data()),
            )

        if "botao_salvar_alteracoes" in request.form:
            nova_qtde = form_editar_ordem_compra.quantidade.data
            print(f"nova_qtde = {nova_qtde}")
            preco_novo = form_editar_ordem_compra.val_unitario.data
            print(f"preco_novo= {preco_novo}")

            try:
                linha_para_editar = session.get("linha_para_editar")
                valor_unitario = session.get("valor_unitario")
                print(f"linha_para_editar {linha_para_editar}")
                nova_qtde = form_editar_ordem_compra.quantidade.data
                preco_novo = form_editar_ordem_compra.val_unitario.data
                print("botao_salvar_alteracoes acionado")
                total_item_novo = nova_qtde * preco_novo
                saldo_total_item_novo = nova_qtde * preco_novo
                query = (
                    f"UPDATE ORDEM_COMPRA\n"
                    f"SET\n "
                    f"QUANTIDADE = '{nova_qtde}',\n"
                    f"PRECO = '{preco_novo}',\n"
                    f"TOTAL_ITEM = '{total_item_novo}',\n"
                    f"SALDO_TOTAL_ITEM = '{saldo_total_item_novo}',\n"
                    f"SALDO_QTD = '{nova_qtde}'\n"
                    f"WHERE EAN = '{linha_para_editar[0][7]}'\n "
                    f"and ORDEM_COMPRA = '{linha_para_editar[0][1]}';"
                )
                # print(f"query {query}")

                mydb.connect()
                mycursor.execute(query)
                mycursor.fetchall()
                fechadb = "SET SQL_SAFE_UPDATES = 1"
                mycursor.execute(fechadb)
                mycursor.fetchall()
                mydb.commit()
                mydb.close()

                ordem_compra = session.get("ordem_compra")
                print(f"ordem_compra recuperado no session {ordem_compra}")
                ordem_pesquisada = session.get("result_ordem_pesquisada")
                # linha_para_editar = list(linha_para_editar)
                linha_para_editar = linha_para_editar.clear()
                print(f"linha_para_editar antes do redirect {linha_para_editar}")
                form_editar_ordem_compra.ean.data = ""
                form_editar_ordem_compra.descricao.data = ""
                form_editar_ordem_compra.quantidade.data = ""
                form_editar_ordem_compra.val_unitario.data = ""

                def script():
                    html = """
                    <!DOCTYPE html>
                        <html>
                        <head><title>Executar JS</title></head>
                        <body>
                            <h1>Executando JavaScript do Backend</h1>
                            <script>
                                function limparCampos() {
                                setTimeout(() => {
                                    document.getElementById("quantidade").value = '';
                                    document.getElementById("val_unitario").value = '';
                                    document.getElementById("descricao").value = '';
                                }, 5); // Delay para permitir que o formulário seja enviado primeiro
                                }
                                alert('Este script foi enviado pelo backend!');
                            </script>
                        </body>
                        </html>
                                """

                return redirect(url_for("editar_ordem_compra"))

            except Exception as e:
                print(e)

            finally:
                # atualiza os campos da linha que está sendo editada
                ## passar esta instrução para o script js no html
                form_editar_ordem_compra.ean.data = ""
                form_editar_ordem_compra.descricao.data = ""
                form_editar_ordem_compra.quantidade.data = ""
                form_editar_ordem_compra.val_unitario.data = ""

                # retornar a lista ordem pesquisada com os valores já editados.

                print(f"ordem_pesquisada = {ordem_pesquisada}")
                # print(f'linha_para_editar: {linha_para_editar}')
                return render_template(
                    "compras/editar_ordem_compra.html",
                    script=script(),
                    ordem_compra=ordem_compra,
                    ordem_pesquisada=ordem_pesquisada,
                    form_editar_ordem_compra=form_editar_ordem_compra,
                    data=Formatadores.formatar_data(Formatadores.os_data()),
                )

        if "botao_excluir_item" in request.form:
            try:
                print("botao_excluir_item_acionado")
                ordem_compra = session.get("ordem_compra")
                ordem_pesquisada = session.get("ordem_pesquisada")
                session["ordem_pesquisada"] = ordem_pesquisada
                session["ordem_compra"] = ordem_compra
                ordem_pesquisada = ordem_pesquisada[0][1]
                print(f"ordem_pesquisada: {ordem_pesquisada}")
                item_selecionado = request.form.getlist("excluir__item")
                item_selecionado = item_selecionado[0]
                print(f"item_selecionado: {item_selecionado}")
                query = f"DELETE FROM ORDEM_COMPRA WHERE ORDEM_COMPRA={ordem_pesquisada} and EAN = {item_selecionado};"

                mydb.connect()
                mycursor.execute(query)
                mycursor.fetchall()
                fechadb = "SET SQL_SAFE_UPDATES = 1"
                mycursor.execute(fechadb)
                mycursor.fetchall()
                mydb.commit()
                mydb.close()
                ordem_compra = session.get("ordem_compra")
                ordem_pesquisada = session.get("ordem_pesquisada")
                print(f"ordem_pesquisada: {ordem_pesquisada}")

                print(f"ordem_pesquisada: {ordem_pesquisada}")
                ordem_compra = ordem_pesquisada[0][1]

                query_atualizada = (
                    f"SELECT * FROM ORDEM_COMPRA WHERE ORDEM_COMPRA = {ordem_compra}"
                )
                mydb.connect()
                mycursor.execute(query_atualizada)
                mycursor.fetchall()
                fechadb = "SET SQL_SAFE_UPDATES = 1"
                mycursor.execute(fechadb)
                mycursor.fetchall()
                mydb.commit()
                mydb.close()
                ordem_pesquisada = Buscadores.OrdemCompra.buscar_ordem_compra(
                    ordem_compra
                )
                session["ordem_pesquisada"] = ordem_pesquisada
                print("teste ordem_pesquisada")
                print()
                for i in ordem_pesquisada:
                    print(i)
                # return redirect(url_for("adicionar_item_ordem_compra"))  # teste
            except:
                pass

            finally:
                ordem_compra = ordem_pesquisada[0][1]
                fornecedor = session.get("fornecedor")
                ordem_pesquisada = session.get("ordem_pesquisada")
                return render_template(
                    "compras/editar_ordem_compra.html",
                    ordem_compra=ordem_compra,
                    ordem_pesquisada=ordem_pesquisada,
                    form_editar_ordem_compra=form_editar_ordem_compra,
                    linha_para_editar="",
                    data=Formatadores.formatar_data(Formatadores.os_data()),
                )

        if "botao_adicionar_item" in request.form and ordem_pesquisada is not None:
            print("Botao_adicionar_item ACIONADO")
            print(f"Ordem pesquisada: {ordem_pesquisada}")
            while ordem_pesquisada is None:
                break
            return redirect(url_for("adicionar_item_ordem_compra"))

    return render_template(
        "compras/editar_ordem_compra.html",
        ordem_compra=ordem_compra,
        ordem_pesquisada=ordem_pesquisada,
        form_editar_ordem_compra=form_editar_ordem_compra,
        data=Formatadores.formatar_data(Formatadores.os_data()),
    )


def adicionar_item_ordem_compra():
    print(
        geral.CorFonte.fonte_verde()
        + "FUNÇÃO adicionar_item_ordem_compra"
        + geral.CorFonte.reset_cor()
    )
    form_adicionar_item_ordem_compra = ModCompras.AdicionarItemOrdemCompra()
    # alert = geral.AlertaMsg.cad_fornecedor_realizado()
    form_editar_ordem_compra = ModCompras.EditarOrdemCompra()

    data = Formatadores.os_data()
    ordem_compra = session.get("ordem_compra")
    print(f"ordem_compra: {ordem_compra}")

    ordem_pesquisada = session.get("result_ordem_pesquisada")
    print(f"Ordem Pesquisada: {ordem_pesquisada}")
    fornecedor = Buscadores.OrdemCompra.buscar_ordem_compra2(ordem_compra, "")
    item_ordem_compra = []
    lista_ordem_compra_com_item_add = []
    fornecedor = fornecedor[0][2]
    session["fornecedor"] = fornecedor
    print(f"fornecedor: {fornecedor}")
    result_pesq_forn = Buscadores.OrdemCompra.buscar_pelo_fornecedor(fornecedor)
    session["result_pesq_forn"] = result_pesq_forn
    # print(f'result_pesq_forn: {result_pesq_forn}')
    descricao = form_adicionar_item_ordem_compra.descricao.data
    unidade = form_adicionar_item_ordem_compra.unidade.data
    categoria = form_adicionar_item_ordem_compra.categoria.data
    codigo = form_adicionar_item_ordem_compra.codigo.data
    ean = form_adicionar_item_ordem_compra.ean.data
    quantidade = form_adicionar_item_ordem_compra.quantidade.data
    preco_unitario = form_adicionar_item_ordem_compra.preco_unitario.data

    def busca_ean_selecionado(item_selecionado):
        print(
            geral.CorFonte.fonte_amarela()
            + "SubFunção busca_ean_selecionado"
            + geral.CorFonte.reset_cor()
        )
        print(f"item_selecionado: {item_selecionado}")
        for i in item_selecionado:
            if i != "":
                item_selecionado = i
        print(f"EAN selecionado: {item_selecionado}")
        return item_selecionado

    def formata_linha_para_identificar_posicao(item_selecionado, result_pesq_forn):
        print(
            geral.CorFonte.fonte_amarela()
            + "SubFunção formata_linha_para_identificar_posicao"
            + geral.CorFonte.reset_cor()
        )
        conta_linha = 0

        pos_pesquisa = ""
        linha_selecionada = []
        for i in result_pesq_forn:
            if i[3] == item_selecionado:
                print(f"lista_ordem_compra: {lista_ordem_compra}")
                # for i in lista_ordem_compra:
                #     print(f'loop for i: {i}')
                pos_pesquisa = conta_linha
                linha_selecionada.append(i)
                print(f"o item selecionado está na linha {conta_linha}")
                # print(f'linha selecionada >>>{linha_selecionada[0]}')
            conta_linha += 1
        return linha_selecionada

    def atualizar_lista_ordem_compra():
        print(
            geral.CorFonte.fonte_amarela()
            + "FUNÇÃO ADICIONAR_ITEM_ORDEM_COMPRA | SubFunção atualizar_lista_ordem_compra"
            + geral.CorFonte.reset_cor()
        )

        total_ordem_compra = 0
        try:
            if preco_unitario is None or quantidade is None:
                total_item = 0
            else:
                total_item = quantidade * preco_unitario

        except Exception as e:
            print("total_item = quantidade * preco_unitario")
            print(e)
            total_item = 0
        print(f"linha selecionada completa:{linha_selecionada_copia}")
        item_ordem_compra.append(linha_selecionada_copia[0])  # 0 - data -  ok
        item_ordem_compra.append(ordem_compra)  # 1 - ordem_compra =  ok
        lista_contador_item_compra.append(contador_item)  # 2 - contador item - ok
        item_ordem_compra.append("0")  # --- sem uso
        item_ordem_compra.append(descricao)  # - 3 - descricao - ok
        item_ordem_compra.append(linha_selecionada_copia[5])  # - 6 - codigo - ok
        item_ordem_compra.append(linha_selecionada_copia[6])  # - 7 - categoria - ok
        item_ordem_compra.append(linha_selecionada_copia[1])  # - 8 - codigo
        item_ordem_compra.append(linha_selecionada_copia[3])  # - 4 - ean - ok
        item_ordem_compra.append(quantidade)  # - 9 - valor_unit - ok
        item_ordem_compra.append(preco_unitario)  # - 10 - valor_total
        item_ordem_compra.append(total_item)  # - 11 - valor_total - ok
        item_ordem_compra_ajustado = tuple(item_ordem_compra)
        ordem_pesquisada_ = session.get("result_ordem_pesquisada")
        ordem_pesquisada_.append(item_ordem_compra_ajustado)
        lista_ordem_compra.append(item_ordem_compra[:])
        item_ordem_compra.clear()
        return i

    # botao_selecionar_item
    try:
        if "botao_selecionar_item" in request.form:
            print(
                "================================================================================================================================="
            )
            print("<botao_selecionar_item ACIONADO>")
            #  SELECIONA LINHA DA TABELA DE ITENS CADASTRADOS NO FORNECEDOR
            result_pesq_forn = session.get("result_pesq_forn")  # Recupera da sessão
            item_selecionado = request.form.getlist("incluir_item")
            item_selecionado = busca_ean_selecionado(item_selecionado)
            print(f"ean do item selecionado: {item_selecionado}")
            linha_selecionada = formata_linha_para_identificar_posicao(
                item_selecionado, result_pesq_forn
            )
            linha_selecionada = linha_selecionada[0]
            print(f"linha_selecionada:>> {linha_selecionada}")

            linha_selecionada_copia = tuple(linha_selecionada)
            print(f"linha_selecionada_copia: {linha_selecionada_copia}")

            session["linha_selecionada_copia"] = linha_selecionada_copia
            session["linha_selecionada"] = linha_selecionada
            linha_selecionada = ()
    except Exception as e:
        print("erro no botao_selecionar_item")
        print(e)

    linha_selecionada_copia = session.get("linha_selecionada_copia")
    # botao_incluir_item
    try:
        if "botao_incluir_item" in request.form:
            print(
                "================================================================================================================================="
            )
            print("botao_incluir_item ACIONADO.....")

            print(f"linha_selecionada_copia: {linha_selecionada_copia}")

            #         # IDENTIFICA O PEDIDO DE COMPRA
            ordem_pesquisada_ = session.get("result_ordem_pesquisada")
            print("ordem_pesquisada_")
            for i in ordem_pesquisada_:
                print(i)
            print(
                f"linha_selecionada_copia\n dentro do incluir_item: {linha_selecionada_copia}"
            )
            # VALIDA O EAN QUE ESTÁ PARA SER INCLUÍDO
            for i in ordem_pesquisada_:
                if i[7] == ean:  # funcionando
                    print(
                        geral.CorFonte.fonte_vermelha()
                        + "item já digitado na ordem de compra"
                        + geral.CorFonte.reset_cor()
                    )
                    break
                else:
                    continue

            atualizar_lista_ordem_compra()  # executa a função
            linha_selecionada_copia = ()

    except Exception as e:
        print("erro no botao_incluir_item ( função adicionar_item_ordem_compra() ")
        print(e)

    cont_temp = 1

    try:
        if "botao_submit_ordem_alterada" in request.form:
            print("botao_submit_ordem_alterada ACIONADO")
            ordem_pesquisada_copia = ordem_pesquisada[:]  # copia
            print(f"ordem_pesquisada_copia: {ordem_pesquisada_copia}")
            try:
                mydb.connect()
                print("Deletando a ordem_compra antiga")
                query_01 = f"DELETE FROM ORDEM_COMPRA WHERE ORDEM_COMPRA={ordem_compra}"
                print(query_01)
                mycursor.execute(query_01)
                mycursor.fetchall()
                mydb.commit()
                print(f"ordem_pesquisada: {ordem_pesquisada}")
                print("Incluindo a ordem_compra atualizada")
                print(f"ordem_compra atualizada:")

                for i in ordem_pesquisada_copia:
                    print()
                    values = (
                        f"'{date.strftime(data, '%Y-%m-%d')}',"
                        f"'{i[1]}',"  # oc
                        f"'{i[2]}',"  # item
                        f"'{i[3]}',"  # descricao
                        f"'{i[4]}',"  #  unidade
                        f"'{i[5]}',"  # categoria
                        f"'{i[6]}',"  # codigo
                        f"'{i[7]}',"  # ean
                        f"'{i[8]}',"  # quantidade
                        f"'{i[9]}',"  # preco
                        f"'{i[9]}',"  # total_item
                        f"'{i[8]}',"  # saldo-qtd
                        f"'{i[9]}',"  # saldo_total
                        f"'{modulos.admin.usuario}'"
                    )
                    query_02 = f"INSERT INTO ORDEM_COMPRA (DATA, ORDEM_COMPRA, ITEM, DESCRICAO, UNIDADE, CATEGORIA, CODIGO, EAN, QUANTIDADE, PRECO, TOTAL_ITEM, SALDO_QTD, SALDO_TOTAL_ITEM, USUARIO) VALUES ({values});"
                    print(query_02)
                    mycursor.execute(query_02)
                    mycursor.fetchall()
                    mydb.commit()
                fechadb = "SET SQL_SAFE_UPDATES = 1"
                mycursor.execute(fechadb)
                mycursor.fetchall()
                mydb.close()
                # linha_selecionada.clear()
                ordem_pesquisada_copia.clear()

                return redirect(url_for("adicionar_item_ordem_compra"))
            except Exception as e:
                print(e)
            cont_temp += 1

    except Exception as e:
        print(e)

    try:
        if "botao_cancelar_alteracao_ordem" in request.form:
            print("botao_cancelar_alteracao_ordem ACIONADO")
            linha_selecionada = []
            return redirect(url_for("adicionar_item_ordem_compra"))

            # ordem_pesquisada = []
            # result_pesq_forn = []
            # ordem_compra = []
    except Exception as e:
        print(e)

    return render_template(
        "compras/adicionar_item_ordem_compra.html",
        ordem_compra=ordem_compra,
        dicionario_ordem_compra=lista_ordem_compra_com_item_add,
        linha_selecionada=linha_selecionada_copia,
        result_pesq_forn=result_pesq_forn,
        data=Formatadores.formatar_data(Formatadores.os_data()),
        form_editar_ordem_compra=form_editar_ordem_compra,
        form_adicionar_item_ordem_compra=form_adicionar_item_ordem_compra,
        # renderiza os forms na pagina html
        ordem_pesquisada=ordem_pesquisada,
    )
