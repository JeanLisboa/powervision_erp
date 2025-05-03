import datetime

from flask import render_template, request, session
import modulos.admin
from forms import Mod_Logistica
from geral import Validadores, Formatadores, Buscadores
import geral

fonte_vermelha = "\033[31m"
fonte_verde = "\033[92m"
fonte_amarela = "\033[93m"
fonte_azul = "\033[34m"
fonte_azul_claro = "\033[36m"
reset_cor = "\033[0m"


def entrada_ordem_compra():
    print("Função entrada_ordem_compra")
    """
    FUNÇÃO EXECUTADA AO CLICAR NO BOTÃO PESQUISAR ORDEM NA TELA ENTRADA ORDEM COMPRA
    ETAPAS:
    1 - USUARIO: DIGITA O NUMERO DA NF E CLICA EM PESQUISAR NOTA FISCAL
    2 - BACKEND:
    2.1 - VALIDA SE O XML NO SISTEMA
    2.2 - VALIDA SE O CNPJ/RAZAO SOCIAL ESTÁ CADASTRADO,  
    2.3 - VALIDA SE A ORDEM DE COMPRA ESTÁ ABERTA
    2.4 - VALIDA OC X NF DE ACORDO COM OS CRITERIOS ( VERIFICAR )
    2.5 - GERA UMA LISTA(lst_nf) COM ESSAS INFORMAÇÕES SE TODAS AS VALIDACOES=TRUE
    2.6 - RENDERIZA A LISTA NO FRONT
    3 - USUARIO: CLICA NO BOTAO LIMPAR
    4 - LIMPA A LISTA E DESABILITA OS BOTOES
    5 - USUARIO: CLICA EM REALIZAR CONFERENCIA
    6: BACKEND
    6.1 - RECUPERA A LISTA lst_nf 
    6.2 - EXECUTA FUNÇÃO buscar_ordem_compra(lst_nf[3]) E RETORNA OS ITENS DA OC (itens_conferencia)
    6.3 - RENDERIZA itens_conferencia NO FRONT
    7 - USUARIO: 
    7.1 - PREENCHE AS QUANTIDADES
    7.2 - CLICA EM ANALISAR CONFERENCIA
    8 - BACKEND:
    8.1 - RECUPERA A LISTA lst_nf
    8.2 - RECUPERA OS ITENS DO PEDIDO  (itens_conferencia)
    8.3 - RECUPERA AS QUANTIDADES DIGITADAS PELO USUARIO (result_conferencia)
    8.4 - CRIA LISTA COM ITENS DA NF E COM ITENS DIGITIDOS
    8.5 - EXECUTA FUNÇÃO 'ANALISA_CRITERIOS_RECEBIMENTO' PARA COMPARAR AS DUAS LISTAS ACIMA
    9 - USUARIO: CLICA EM FINALIZAR CONFERENCIA
    10 - BACKEND:
    10.1 - RECUPERA A LISTA lst_nf
    10.2 - RECUPERA OS ITENS DO PEDIDO  (itens_conferencia)
    10.3 - RECUPERA AS QUANTIDADES DIGITADAS PELO USUARIO (result_conferencia)
    10.4 - COMPARA QUANTIDADE DOS ITENS DO PEDIDO COM AS DIGITADAS PELO USUARIO
    10.5 - CRIA UMA LISTA DOS ITENS QUE SERÃO INTERNALIZADOS
    10.6 - BUSCA CRITÉRIOS PARA ENTRADA ESTOQUE: (PENDENTE)
    10.7 - ATUALIZA STATUS ORDEM COMPRA (TRUE = PEDIDO_ENCERRADO) | QUERY PENDENTE
    10.8 - ATUALIZA SALDO ORDEM COMPRA
    10.9 - ATUALIZA O ESTOQUE
    
    """
    form_entrada_ordem_compra = Mod_Logistica.EntradaOrdemCompra()
    razao_social = form_entrada_ordem_compra.razao_social.data
    cnpj = form_entrada_ordem_compra.cnpj.data
    nf = form_entrada_ordem_compra.nf.data
    pedido = ""
    itens_conferencia = ""
    validacao_1 = ""
    validacao_2 = ""
    validacao_3 = ""
    validacao_4 = ""
    # lst_qtde_pedido = []
    lst_nf = []
    lst_itens_recebidos = []
    result_conferencia = []
    lst_diferenca = []
    # diferenca = 0
    # qtde_pedido = 0
    campo_qtde = 9999

    if cnpj is None:
        cnpj = ""
    if razao_social is None:
        razao_social = ""
    if nf is None:
        nf = ""

    # processamento dos botões
    if request.method == "POST":
        try:
            if "botao_pesquisar_ordem_compra" in request.form:
                print("botao_pesquisar_NF ACIONADO")
            if nf is not None:
                #  redefine as variáveis
                nome_arquivo = Buscadores.Xml.buscar_arquivo(nf)
                cnpj = Buscadores.Xml.buscar_cnpj(nome_arquivo)
                razao_social = Buscadores.Xml.buscar_razao_social(nome_arquivo)
                pedido = Buscadores.Xml.buscar_pedido(
                    nome_arquivo
                )  # busca o pedido no xml
                lst_nf = [
                    cnpj,
                    razao_social,
                    nf,
                    pedido,
                ]  # cria uma lista com os dados que serão renderizados na tela informando o status
                status_ordem = Buscadores.OrdemCompra.verifica_status_ordem(
                    lst_nf[3]
                )  # lst_nf[3] = pedido (ou ordem de compra)
                Validadores.valida_pedido_recebido(
                    pedido
                )  # busca o pedido no banco de dados

                def validacao_1():
                    print('fonte_amarela + \nVALIDaÇÃO 1: VERIFICAR SE O ARQUIVO XML ESTÁ NO SERVIDOR' + reset_cor)
                    if status_ordem is True:  # VERIFICAR SE O XML ESTÁ NO SERVIDOR
                        return True
                    else:  # xml nao localizado
                        return False

                def validacao_2():
                    print(fonte_amarela + '\nVALIDAÇÃO 2: VERIFICAR SE O FORNECEDOR ESTÁ CADASTRADO' + reset_cor)
                    if Buscadores.buscar_cnpj(cnpj) is True:
                        print(fonte_azul + f"cnpj encontrado: {cnpj}" + reset_cor)
                        print(fonte_verde + 'VALIDAÇÃO 2 concluída' + reset_cor)
                        return True
                    else:
                        print("cnpj não encontrado")
                        lst_nf = ['Fornecedor não encontrado']
                        return False

                def validacao_3():
                    print(fonte_amarela + '\nVALIDÇÃO 3: VERIFICAR SE O PEDIDO ESTÁ EM ABERTO' + reset_cor)
                    if status_ordem is True:
                        print(fonte_azul + f"Pedido {lst_nf[3]} aberto" + reset_cor)
                        print(fonte_verde + 'VALIDAÇÃO 3 concluída' + reset_cor)
                        return True
                    else:
                        print(
                            fonte_vermelha + "Pedido encerrado ou cancelado" + reset_cor
                        )
                        return False

                def validacao_4():
                    print(fonte_amarela + '\nVALIDAÇÃO 4: VALIDAR PEDIDO X NF' + reset_cor)
                    itens_nf = Buscadores.Xml.buscar_linhas_nf(str(nf))
                    print(f"itens_nf = {itens_nf}\n")
                    # print(fonte_amarela + '\nVALIDAÇÃO 4: (2) RECEBER OC, CRIAR LISTA DE EAN E PRECO' + reset_cor)
                    itens_oc = Validadores.valida_pedido_recebido(pedido)
                    # print(f"itens_oc = {itens_oc}\n")
                    # print(fonte_amarela + '\nVALIDAÇÃO 4: (3) COMPARAR AS DUAS LISTAS' + reset_cor)
                    maior_dif_permitida = modulos.admin.maior_dif_permitida
                    print(f"maior_dif_permitida = {maior_dif_permitida}")
                    cont_preco_fora_politica = 0

                    print("for ean_oc in itens_oc:")
                    for ean_oc in itens_oc:  # 'oc' = 'ordem de compra'
                        print(f"\nean pesquisado: {ean_oc[0]}")

                        for ean_nf in itens_nf:
                            # print(f"ean_nf = {ean_nf[0]}")
                            if ean_oc[0] == ean_nf[0]:
                                # print(
                                #     fonte_azul
                                #     + f"ean_oc[0] = {ean_oc[0]} || ean_oc[1] = {ean_oc[1]}\n"
                                #     f"ean_nf[0] = {ean_nf[0]} || ean_nf[1] = {ean_nf[1]}"
                                #     + reset_cor
                                # )
                                if (ean_oc[1] - ean_nf[1]) <= maior_dif_permitida:
                                    print(
                                        fonte_verde
                                        + f"preco dentro da politica"
                                        + reset_cor
                                    )
                                else:
                                    print(
                                        fonte_vermelha
                                        + f"preco fora da politica"
                                        + reset_cor
                                    )
                                    cont_preco_fora_politica += 1
                            else:
                                print(
                                    fonte_vermelha
                                    + f"ean_oc[0] != ean_nf[0]"
                                    + reset_cor
                                )
                    if cont_preco_fora_politica == 0:
                        return True
                    else:
                        return False

        except Exception as e:
            print(f"Exception e: {e}")
            lst_nf = ["NOTA FISCAL NAO LOCALIZADA"]
            validacao_final = (
                False  # serve para configurar os botoes na renderização da tela
            )
            # session['validacao_final'] = validacao_final

        def analisa_validacoes():
            print(f"função entrada_ordem_compra | subfuncao analisa_validacoes")
            try:
                if (
                    validacao_1() is True
                    and validacao_2() is True
                    and validacao_3() is True
                    and validacao_4() is True
                ):
                    validacao_final = True
                    session["validacao_final"] = validacao_final
                    print(
                        fonte_amarela
                        + ">VALIDAÇÃO 1: VERIFICAR SE O XML ESTÁ NO SERVIDOR\033[32m"
                        + reset_cor
                    )
                    print(validacao_1)
                    print(fonte_verde + ">VALIDAÇÃO 1 concluída" + reset_cor)

                    print(
                        fonte_amarela
                        + ">VALIDAÇÃO 2: VERIFICAR SE O FORNECEDOR ESTÁ CADASTRADO"
                        + reset_cor
                    )
                    print(validacao_2)
                    print(fonte_verde + ">VALIDAÇÃO 2 concluída" + reset_cor)

                    print(
                        fonte_amarela
                        + ">VALIDAÇÃO 3: VERIFICAR SE O PEDIDO ESTÁ EM ABERTO"
                        + reset_cor
                    )
                    print(validacao_3)
                    print(fonte_verde + ">VALIDAÇÃO 3 concluída" + reset_cor)

                    print(
                        fonte_amarela + ">VALIDAÇÃO 4: VALIDAR PEDIDO X NF" + reset_cor
                    )
                    print(
                        fonte_amarela
                        + ">VALIDAÇÃO 4: (1) RECEBER NF, CRIAR LISTA DE EAN E PRECO"
                        + reset_cor
                    )
                    print(
                        fonte_amarela
                        + ">VALIDAÇÃO 4: (2) RECEBER OC, CRIAR LISTA DE EAN E PRECO"
                        + reset_cor
                    )
                    print(
                        fonte_amarela
                        + ">VALIDAÇÃO 4: (3) COMPARAR AS DUAS LISTAS"
                        + reset_cor
                    )
                    print(validacao_4)
                    print(fonte_verde + ">VALIDAÇÃO 4 concluída" + reset_cor)
                    # print(fonte_verde + 'Pedido Validado' + reset_cor)

                    lst_nf.append("LIBERADO")
                    session["resultado_validacao"] = lst_nf
                    session["validacao_final"] = validacao_final
                    print(fonte_verde + f"lst_nf = {lst_nf}" + reset_cor)

                else:
                    validacao_final = False
                    session["validacao_final"] = validacao_final

                if validacao_1() is False:
                    lst_nf.append("NOTA FISCAL NÃO ENCONTRADA")
                    session["resultado_validacao"] = lst_nf
                    session["validacao_final"] = validacao_final

                if validacao_2() is False:
                    lst_nf.append("FORNECEDOR NÃO CADASTRADO")
                    session["resultado_validacao"] = lst_nf
                    session["validacao_final"] = validacao_final

                if validacao_3() is False:
                    lst_nf.append("PEDIDO NÃO ABERTO")
                    session["resultado_validacao"] = lst_nf
                    session["validacao_final"] = validacao_final

                if validacao_4() is False:
                    lst_nf.append("PREÇO FORA DA POLÍTICA")
                    session["resultado_validacao"] = lst_nf
                    session["validacao_final"] = validacao_final

            except Exception as e:
                print(e)

        def botao_limpar_pesquisa():
            try:
                if "botao_limpar_pesquisa" in request.form:
                    print("\nbotao_limpar_pesquisa ACIONADO")
            except Exception as e:
                print(e)

        analisa_validacoes()
        botao_limpar_pesquisa()

        try:
            if "botao_realizar_conferencia" in request.form:
                print("\nbotao_realizar_conferencia ACIONADO")
                lst_nf = session.get("resultado_validacao")  # recupera as informações da tabela de pesquisa
                if lst_nf != ["NOTA FISCAL NÃO ENCONTRADA"]:
                    print(f"\n lst_nf >> {lst_nf}")
                    itens_conferencia = Buscadores.OrdemCompra.buscar_ordem_compra(
                        lst_nf[3]
                    )  # lista os itens da ordem de compra, localizado no html, à esquerda
                    session["itens_conferencia"] = itens_conferencia

        except Exception as e:
            print(e)

        try:
            if "botao_analisar_conferencia" in request.form:
                print(fonte_azul + "\nbotao_analisar_conferencia ACIONADO" + reset_cor)

                lst_nf = session.get("resultado_validacao")  # recupera as informações da tabela de pesquisa
                print(f"lst_nf >>> {lst_nf}")

                itens_conferencia = session.get("itens_conferencia")  # Recupera as informações da ordem de compra
                print(f"itens_conferencia >>> {itens_conferencia}")

                result_conferencia = request.form.getlist("quantidade")
                print(f"result_conferencia >>> {result_conferencia}")
                session["result_conferencia"] = result_conferencia

                lst_pedido_p_conferencia = []
                lst_diferenca = []
                lst_qtde_pedido = [0]

                # o bloco abaixo cria uma lista de tuplas (ean, quantidade) para fazer a comparação NF X RECEBIDO
                pos = 0
                for i in itens_conferencia:
                    #  formata quantidade da NF e cria uma lista
                    saldo_qtd = int(i[11])
                    print(f'saldo_qtd = {saldo_qtd}')
                    saldo_qtd = str(saldo_qtd)
                    ean_pedido = i[7]
                    zipped = (ean_pedido, saldo_qtd)  # (ean, quantidade nf)
                    lst_pedido_p_conferencia.append(zipped)
                    session["lst_pedido_p_conferencia"] = lst_pedido_p_conferencia

                    #  formata quantidade digitada e cria uma lista
                    zipped_2 = (ean_pedido, result_conferencia[pos])  # (ean, quantidade recebida)
                    lst_itens_recebidos.append(zipped_2)
                    diferenca = int(result_conferencia[pos]) - int(saldo_qtd)
                    analisa_diferenca(diferenca)
                    zipped_3 = (lst_itens_recebidos[pos], diferenca, analisa_diferenca(diferenca))
                    lst_diferenca.append(zipped_3)
                    session["lst_diferenca"] = lst_diferenca
                    pos += 1
                analisa_criterios_recebimento(lst_pedido_p_conferencia, lst_itens_recebidos, lst_diferenca)

        except Exception as e:
            print(e)
        lst_ent_estoque = []
        lst_ent_estoque_temp = []

        try:
            if "botao_alterar" in request.form:
                print("--------------------------------------------")
                print("botao_alterar ACIONADO")

                lst_nf = session.get(
                    "resultado_validacao"
                )  # recupera as informações da tabela de pesquisa
                print(f"lst_nf >>> {lst_nf}")

                itens_conferencia = session.get(
                    "itens_conferencia"
                )  # Recupera as informações da ordem de compra
                print(f"itens_conferencia >>> {itens_conferencia}")

                result_conferencia = session.get("result_conferencia")
                print(f"result_conferencia >>> {result_conferencia}")
                # esta lst é recuperada do acionamento do botao analisar conferencia
                lst_diferenca = session.get("lst_diferenca")

                print(f"lst_diferenca >>> {lst_diferenca}")
                print(f"itens_conferencia >>> {itens_conferencia}")
                print(f"campo_qtde >>> {campo_qtde}")

        except Exception as e:
            print(e)

        try:
            if "botao_finalizar_conferencia" in request.form:
                print(fonte_azul + "\nBotao_finalizar_conferencia ACIONADO" + reset_cor)
                lst_nf = session.get("resultado_validacao")  # recupera as informações da tabela de pesquisa
                print(f"lst_nf: {lst_nf}")
                itens_conferencia = session.get("itens_conferencia", [])  # Recupera as informações da ordem de compra
                print(f'itens_conferencia: {itens_conferencia}')
                result_conferencia = session.get("result_conferencia")
                print(f'result_conferencia: {result_conferencia}')
                lst_pedido_p_conferencia = session.get("lst_pedido_p_conferencia")
                print(f"lst_pedido_p_conferencia >>> {lst_pedido_p_conferencia}")
                print("\n--------------ANALISE ENTRADA ESTOQUE------------------")
                print("1 - COMPARA QUANTIDADE RECEBIDA X SALDO DO PEDIDO *** PENDENTE DE RECEBIMENTO *** ")
                lst_qtde_recebida_a = []
                lst_qtde_pedido_a = []
                lst_an_ent_estoque = []
                lst_auxiliar_temp = []
                lst_auxiliar = []
                for qtde_recebida in result_conferencia:
                    lst_qtde_recebida_a.append(qtde_recebida)

                for qtde_pedido in lst_pedido_p_conferencia:
                    lst_qtde_pedido_a.append(qtde_pedido[1])

                lst_an_ent_estoque.append(lst_qtde_recebida_a)
                lst_an_ent_estoque.append(lst_qtde_pedido_a)
                print(f"lst_an_ent_estoque >>> {lst_an_ent_estoque}")

                print("--------------FINALIZADO------------------\n")
                print("2 - MONTA LISTA DE ITENS QUE SERÃO INTERNALIZADOS")
                print('itens_conferencia')
                print(itens_conferencia)
                for i in itens_conferencia:
                    lst_ent_estoque_temp.append(i[5])  # categoria
                    lst_ent_estoque_temp.append(i[7])  # ean
                    lst_ent_estoque_temp.append(i[6])  # codigo
                    lst_ent_estoque_temp.append(i[3])  # descricao
                    lst_ent_estoque_temp.append(i[9])  # qtde
                    lst_ent_estoque.append(lst_ent_estoque_temp[:])
                    lst_ent_estoque_temp.clear()

                lst_ent_estoque_final = []
                print('================teste de lst_ent_estoque ===================')
                print(f'lst_ent_estoque: {lst_ent_estoque}')
                print(f'lst_qtde_recebida_a: {lst_qtde_recebida_a}')
                print(f'lst_qtde_pedido_a: {lst_qtde_pedido_a}')
                print('=============================================================')
                for a, b, c in zip(
                        lst_ent_estoque, lst_qtde_recebida_a, lst_qtde_pedido_a):
                    a.append(c if int(b) > int(c) else b)  # Adiciona a quantidade à sublista
                    lst_ent_estoque_final.append(a)

                print("3 - BUSCA CRITERIO PARA ENTRADA ESTOQUE (PENDENTE)\n")
                print("4 - ATUALIZA O ESTOQUE OK \n")
                print(f'lst_ent_estoque_final completo\n: {lst_ent_estoque_final}')

                for i in lst_ent_estoque_final:
                    # 1 - recebe as quantidades
                    data = datetime.date.today()
                    data = data.strftime("%Y-%m-%d")
                    tipo_mov = "ENTRADA"
                    ordem_compra = lst_nf[3]
                    nota_fiscal = lst_nf[2]
                    ean = i[1]  # ean
                    codigo = i[2]
                    descricao = i[3]
                    quantidade = i[5]

                    print(f'quantidade >>> {quantidade}')

                    valor = i[4]
                    usuario = 'ADMIN'
                    # 2 - atualiza o estoque
                    geral.Buscadores.OrdemCompra.atualizar_estoque(
                        data,
                        tipo_mov,
                        ordem_compra,
                        nota_fiscal,
                        ean,
                        codigo,
                        descricao,
                        quantidade,
                        valor,
                        usuario)

                    print('3 - ATUALIZA O SALDO DA ORDEM_COMPRA - OK')
                    geral.Buscadores.OrdemCompra.atualizar_saldo_ordem_compra(ordem_compra, ean, quantidade, valor)


                def atualiza_status_ordem_compra(lst_diferenca):
                    print("Função atualiza_status_ordem_compra\n")
                    for i[2] in lst_diferenca:
                        print(i[2])
                        if i[2] == "FALTA":
                            return False
                        else:
                            return True

                print("5 - ATUALIZA O STATUS ORDEM COMPRA")
                if atualiza_status_ordem_compra(lst_diferenca) is True:
                    print("Pedido encerrado")
                else:
                    print("pedido parcialmente recebido")

                print("6 - ATUALIZA SALDO ORDEM COMPRA")


                ordem_compra = lst_nf[3]
                print('FUNÇÃO geral.Buscadores.OrdemCompra.busca_saldo_ordem_compra(ordem_compra)')
                list_temp = []
                ean_saldo = None
                preco = None
                saldo_qtd = None
                for i in geral.Buscadores.OrdemCompra.busca_saldo_ordem_compra(ordem_compra):
                    ean_saldo = i[7]
                    preco = i[9]
                    saldo_qtd = i[12]
                    list_temp.append((ean_saldo, preco, saldo_qtd))


                print('i do lst_nf')
                print('list_temp')

                for a in list_temp:
                    print(a)
                    for i in lst_ent_estoque_final:
                        ean = i[1]
                        quantidade = i[4]
                        quantidade = list(quantidade)
                        if a[0] == ean:
                            list_temp = list_temp + quantidade

                print(list_temp)

        except Exception as e:
            print(e)

    if "NOTA FISCAL NAO LOCALIZADA" in lst_nf:
        validacao_final = False
    else:
        validacao_final = session.get("validacao_final")
    print(f"validação_final antes do render_template = {validacao_final}")
    return render_template(
        "logistica/entrada_ordem_compra.html",
        form_entrada_ordem_compra=form_entrada_ordem_compra,
        validacao_final=validacao_final,
        lst_nf=lst_nf,
        lst_diferenca=lst_diferenca,
        lst_itens_recebidos=lst_itens_recebidos,
        result_conferencia=result_conferencia,
        itens_conferencia=itens_conferencia,
        data=Formatadores.formatar_data(Formatadores.os_data()))


def estoque():
    print("Função estoque")
    form_estoque = Mod_Logistica.Estoque()

    return render_template("logistica/estoque.html", form_estoque=form_estoque)


def analisa_diferenca(diferenca):
    if diferenca > 0:
        status = "SOBRA"
    elif diferenca < 0:
        status = "FALTA"
    else:
        status = "OK"
    return status


def analisa_criterios_recebimento(lst_pedido_p_conferencia,
                                  lst_itens_recebidos,
                                  lst_diferenca):
    print("\nFunção analisa_criterios_recebimento\n")
    print(f"lst_pedido_p_conferencia : {lst_pedido_p_conferencia}")
    print(f"lst_itens_recebidos : {lst_itens_recebidos}")
    print(f"lista_diferenca : {lst_diferenca}")

    print("\nFim da função analisa_criterios_recebimento\n")

