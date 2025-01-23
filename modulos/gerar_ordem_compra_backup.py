def gerar_ordem_compra():
    print(geral.CorFonte.fonte_amarela() + 'Função gerar_ordem_compra' + geral.CorFonte.reset_cor())
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
        if preco_unitario is None or quantidade is None:
            total_item = 0

        else:
            total_item = quantidade * preco_unitario

    except Exception as e:
        print('total_item = quantidade * preco_unitario')
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
    # 3 - funções locais

    def valida_ean_na_lista(ean):
        print(geral.CorFonte.fonte_amarela() + 'funcao verifica_ean_na_lista' + geral.CorFonte.reset_cor())
        print('Verifica se o ean já consta no pedido')
        lista_ean_temp = []
        if len(lista_ean) == 0:  # ou if lista_cadastro_produto == []
            print('lista vazia')
            lista_ean_temp.append(ean)
            lista_ean.append(lista_ean_temp[:])
            lista_ean_temp.clear()

            print(f'lista_ean: {lista_ean}')
            return True
        else:
            for i in lista_ean:  # verifica se o item ja existe no pedido
                print(f'for lista_cadastro_produto {i}')
                if i == ean:
                    print('ean ja existente na lista de itens a cadastrar')
                    return False
                else:
                    print('ean ainda nao digitado.')
                    lista_ean_temp.append(ean)
                    lista_ean.append(lista_ean_temp)
                    lista_ean_temp.clear()

                    print(f'lista_ean: {lista_ean}')
                    return True

    # 4 - Processamentos
    if request.method == 'POST':
        item_ordem_compra.clear()
        result_pesq_forn = ''
        try:
            if 'botao_pesquisar_fornecedor' in request.form:
                print('botao_pesquisar_fornecedor ACIONADO')
                fornecedor = form_gerar_ordem_compra.fornecedor.data
                print(f'Fornecedor: {fornecedor}')
                session['fornecedor'] = fornecedor
                result_pesq_forn = Buscadores.OrdemCompra.buscar_pelo_fornecedor(fornecedor)
                # print(f'result_pesq_forn SESSION >>> {result_pesq_forn}')
                session['result_pesq_forn'] = result_pesq_forn
        except Exception as e:
            print('erro no botao_pesquisar_fornecedor')
            print(e)


        try:
            if 'botao_selecionar_item' in request.form:
                print('botao_selecionar_item ACIONADO')
                result_pesq_forn = session.get('result_pesq_forn')  # Recupera da sessão
                fornecedor = session.get('fornecedor')
                # print(f'teste fornecedor após acionamento do botao_selecionar_item {fornecedor}')

            def busca_ean_selecionado():
                print(geral.CorFonte.fonte_amarela() + 'SubFunção busca_ean_selecionado' + geral.CorFonte.reset_cor())
                item_selecionado = request.form.getlist('incluir_item')
                for i in item_selecionado:
                    if i != '':
                        item_selecionado = i
                # print(f'EAN selecionado: {item_selecionado}')
                return item_selecionado

            item_selecionado = busca_ean_selecionado()
            print(f'ean do item selecionado: {item_selecionado}')

            def formata_linha_para_identificar_posicao(item_selecionado, result_pesq_forn):
                print(geral.CorFonte.fonte_amarela() + 'SubFunção formata_linha_para_identificar_posicao' + geral.CorFonte.reset_cor())
                conta_linha = 0
                pos_pesquisa = ''
                linha_selecionada = []
                for i in result_pesq_forn:
                    if i[3] == item_selecionado:
                        print(f'lista_ordem_compra: {lista_ordem_compra}')
                        pos_pesquisa = conta_linha
                        linha_selecionada.append(i)
                        print(f'o item selecionado está na linha {conta_linha}')
                        print(f'linha selecionada >>>{linha_selecionada[0]}')
                    conta_linha += 1
                return linha_selecionada

            # executado após o acinamento de "botao_selecionar_item"
            linha_selecionada = formata_linha_para_identificar_posicao(item_selecionado, result_pesq_forn)
            linha_selecionada = linha_selecionada[0]
            print(f'linha_selecionada: {linha_selecionada}')
            print(f'linha_selecionada[0]: {linha_selecionada[0]}')

        except Exception as e:
            print('erro no botao_selecionar_item')
            print(f'linha_selecionada: {linha_selecionada}')
            # print(f'linha_selecionada[0]: {linha_selecionada[0]}')
            print(e)
        # pesquisar item pelo código. no momento está sem uso
        # try:
        #     result_pesq_forn = session.get('result_pesq_forn', [])  # Recupera da sessão
        #     if 'botao_pesquisar_item' in request.form:
        #         print('botao_pesquisar_item ACIONADO')
        #         if descricao == '' and ean == '':
        #             resultado = Buscadores.buscar_produto_pelo_codigo(codigo)
        #             resultado = resultado[0]
        #         if codigo == '' and descricao == '':
        #             resultado = Buscadores.buscar_produto_pelo_ean(ean)
        #             resultado = resultado[0]
        #         if resultado is None:
        #             pass
        #         print(resultado)

                # TRANSFORMAR EM FUNÇÃO
        #         preco_medio = Buscadores.OrdemCompra.preco_medio(codigo)
        #         ultimo_preco = Buscadores.OrdemCompra.ultimo_preco(codigo)
        #         print(f'Preço médio >>> {preco_medio}')
        #
        #        # alert = geral.AlertaMsg.cadastro_inexistente()
        #         # return redirect(url_for('gerar_ordem_compra'))
        # except Exception as e:
        #     print(e)
        #     alert = geral.AlertaMsg.cadastro_inexistente()
        #     pass
        #
        # inclui o item pesquisado na tabela que conterá os itens da ordem de compra
        try:
            result_pesq_forn = session.get('result_pesq_forn', [])  # Recupera da sessão
            fornecedor = session.get('fornecedor')
            print(f'teste fornecedor após acionamento do botao_selecionar_item (except) {fornecedor}')
            if 'botao_incluir_item' in request.form:
                print('botao_incluir_item ACIONADO')
                try:
                    contador_item = len(lista_contador_item_compra)
                except Exception as e:
                    print('erro no contador_item = len(lista_contador_item_compra)')
                    print(e)
                    contador_item = 0
                #  TRANSFORMAR EM FUNÇÃO
                contador_item += 1
                print(f'Item {contador_item} incluído ')

                def atualizar_lista_ordem_compra():
                    print(geral.CorFonte.fonte_amarela() + 'SubFunção atualizar_lista_ordem_compra'  + geral.CorFonte.reset_cor())
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
                    return total_ordem_compra, lista_ordem_compra
                print('---------------------------------------------------')
                print(f'ean: {ean}')
                valida_ean_na_lista(ean)
                total_ordem_compra = atualizar_lista_ordem_compra()
                # print(f'ean_selecionado {item_selecionado}')
                print(f'lista_ordem_compra {lista_ordem_compra}')
                for i in lista_ordem_compra:
                    if i[6] == item_selecionado:
                        print(geral.CorFonte.fonte_vermelha() + f'DUPLICADO {i}' + geral.CorFonte.reset_cor())
                    print(f'lista_ordem_compra {i}')
                print(f'total_ordem_compra {total_ordem_compra[0]}')
                print('---------------------------------------------------')
        except Exception as e:
            print('erro no botao_incluir_item')
            print(e)

        try:
            if 'botao_consulta' in request.form:
                fornecedor = session.get('fornecedor')
                print(f'teste fornecedor após acionamento do botao_consulta {fornecedor}')
                print('botao_consulta pressionado')

        except Exception as e:
            print('erro no botao_consulta')
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
                                  f"'{i[8]}',"
                                  f"'{i[9]}',"
                                  f"'{modulos.admin.usuario}'")

                        query = (f'INSERT INTO ORDEM_COMPRA'
                                 f'(DATA, ORDEM_COMPRA, ITEM, DESCRICAO, UNIDADE, CATEGORIA, '
                                 f'CODIGO, EAN, QUANTIDADE, PRECO, TOTAL_ITEM, SALDO_QTD, SALDO_TOTAL_ITEM, USUARIO)'
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
                # lista_ordem_compra.clear()  # limpa a lista para a proxima ordem de compra
                return redirect(url_for('gerar_ordem_compra'))

        except Exception as e:
            print('erro no botao_submit_compra')
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
            print('erro no botao_limpar_ordem')
            print(e)

        alert = session.pop('alert', None)

        if result_pesq_forn is None:
            result_pesq_forn = 0

    return render_template('compras/gerar_ordem_compra.html',
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
                           data=Formatadores.formatar_data(Formatadores.os_data()))
