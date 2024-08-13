from flask import Flask, render_template, redirect, url_for, request, session
import modulos.admin
from forms import ModCompras, Mod_Comercial, Mod_Pricing, Mod_Logistica
from geral import Validadores, Formatadores, AtualizaCodigo, Buscadores, AlertaMsg
import geral


def entrada_ordem_compra():
    pedido = ""
    itens_conferencia = ""
    validacao_1 = ""
    validacao_2 = ""
    validacao_3 = ""
    validacao_4 = ""
    lst_nf = []
    lst_itens_recebidos = []
    quantidade = 0
    result_conferencia = []
    form_entrada_ordem_compra = Mod_Logistica.EntradaOrdemCompra()
    razao_social = form_entrada_ordem_compra.razao_social.data
    cnpj = form_entrada_ordem_compra.cnpj.data
    nf = form_entrada_ordem_compra.nf.data

    if cnpj is None:
        cnpj = ''
    if razao_social is None:
        razao_social = ''
    if nf is None:
        nf = ''

    lst_diferenca = []

    # processamento do botão pesquisar ordem de compra
    if request.method == 'POST':
        try:
            if 'botao_pesquisar_ordem_compra' in request.form:
                print('botao_pesquisar_ordem ACIONADO')
            if nf is not None:  # pesquisa a ordem de compra no banco de dados
                nome_arquivo = Buscadores.Xml.buscar_arquivo(nf)
                cnpj = Buscadores.Xml.buscar_cnpj(nome_arquivo)
                razao_social = Buscadores.Xml.buscar_razao_social(nome_arquivo)
                print('------------------------------------------------------------')
                print('------VALIDAÇÃO 1: VERIFICAR SE O XML ESTÁ NO SERVIDOR------')
                print('------------------------------------------------------------')
                pedido = Buscadores.Xml.buscar_pedido(nome_arquivo)  # busca o pedido no xml
                print(f'pedido identificado no xml: {pedido}')
                lst_nf = [cnpj, razao_social, nf, pedido]
                print(f'a lst_nf será renderizada: {lst_nf}')
                Validadores.valida_pedido_recebido(pedido) # busca o pedido no banco de dados
                print(f'pasta_xml: {geral.pasta_xml}')
                print(f'{form_entrada_ordem_compra.nf.data}')

                if Buscadores.OrdemCompra.verifica_status_ordem(lst_nf[3]) is True:
                    validacao_1 = True
                else:
                    print('xml não encontrado')

                print('------------------------------------------------------------')
                print('---VALIDAÇÃO 2: VERIFICAR SE O FORNECEDOR ESTÁ CADASTRADO---')
                print('------------------------------------------------------------')
                if Buscadores.buscar_cnpj(cnpj) is True:
                    print(f'cnpj encontrado: {cnpj}')
                    validacao_2 = True
                else:
                    print('cnpj não encontrado')
                    lst_nf = ['Fornecedor não encontrado']
                print('------------------------------------------------------------')
                print('------VALIDAÇÃO 3: VERIFICAR SE O PEDIDO ESTÁ EM ABERTO-----')
                print('------------------------------------------------------------')
                if Buscadores.OrdemCompra.verifica_status_ordem(lst_nf[3]) is True:
                    print('Pedido aberto')
                    validacao_3 = True
                else:
                    print('Pedido encerrado ou cancelado')
                print('--------------------------------------------------------------')
                print('--------------VALIDAÇÃO 4: VALIDAR PEDIDO X NF----------------')
                print('--------------------------------------------------------------')
                print('---VALIDAÇÃO 4: (1) RECEBER NF, CRIAR LISTA DE EAN E PRECO----')
                itens_nf = Buscadores.Xml.buscar_linhas_nf(str(nf))
                print('---VALIDAÇÃO 4: (2) RECEBER OC, CRIAR LISTA DE EAN E PRECO----')
                itens_oc = Validadores.valida_pedido_recebido(pedido)
                print('--------------------------------------------------------------')
                print('---VALIDAÇÃO 4: (3) COMPARAR AS DUAS LISTAS-------------------')
                maior_dif_permitida = modulos.admin.maior_dif_permitida
                cont_fora = 0

                for ean_oc in itens_oc:
                    for ean_nf in itens_nf:
                        if ean_oc[0] == ean_nf[0]: # valida se o ean da oc está na nf
                            if (ean_nf[1] - ean_oc[1]) > maior_dif_permitida:
                                print(f'{ean_oc[0]} | {ean_nf[1]} | {ean_nf[1]}-{ean_oc[1]} {(ean_oc[1]) - (ean_nf[1])} | preço fora da politica')
                                cont_fora += 1
                            else:
                                pass

                print('---------------------------------------------------------------')
                if cont_fora == 0:
                    validacao_4 = True
                else:
                    validacao_4 = False
        except Exception as e:
            lst_nf = ['NOTA FISCAL NAO LOCALIZADA']

        # se der erro, verificar a identação
        if validacao_1 and validacao_2 and validacao_3 and validacao_4:
            print('pedido validado')
            lst_nf.append('LIBERADO')
            session['resultado_validacao'] = lst_nf
            print(lst_nf)
        if validacao_1 is False:
            lst_nf.append('NOTA FISCAL NÃO ENCONTRADA')
        if validacao_2 is False:
            lst_nf.append('FORNECEDOR NÃO CADASTRADO')
        if validacao_3 is False:
            lst_nf.append('PEDIDO NÃO ABERTO')
        if validacao_4 is False:
            lst_nf.append('PREÇO FORA DA POLÍTICA')

        try:
            if 'botao_realizar_conferencia' in request.form:
                lst_nf = session.get('resultado_validacao') # recupera as informações da tabela de pesquisa
                nf = lst_nf[2]
                print('botao_realizar_conferencia ACIONADO')
                print(f' lst_nf >> {lst_nf}')
                itens_conferencia = Buscadores.OrdemCompra.buscar_ordem_compra(lst_nf[3])
                session['itens_conferencia'] = itens_conferencia
                print(f'itens conferencia >>> {itens_conferencia}')
        except Exception as e:
            print(e)

        try:
            if 'botao_limpar_pesquisa' in request.form:
                print('botao_limpar_pesquisa ACIONADO')
        except Exception as e:
            print(e)

        try:
            if 'botao_analisar_conferencia' in request.form:
                itens_conferencia = session.get('itens_conferencia', []) # Recupera as informações da ordem de compra
                print(itens_conferencia)
                print('botao_analisar_conferencia ACIONADO')
                result_conferencia = request.form.getlist('quantidade') # lista a quantidade dos itens conferidos
                print('--------------------------------------------')

                lst_pedido_p_conferencia = []
                lst_itens_recebidos = []
                lst_diferenca = []

                # o bloco abaixo cria uma lista de tuplas (ean, quantidade) para fazer a comparação NF X RECEBIDO
                pos = 0
                for i in itens_conferencia: # origem: nota fiscal
                    qtde_pedido = int(i[8])
                    qtde_pedido = str(qtde_pedido)
                    ean_pedido = i[7]
                    zipped = (ean_pedido, qtde_pedido)  # (ean, quantidade nf)
                    lst_pedido_p_conferencia.append(zipped)
                    zipped_2 = (ean_pedido, result_conferencia[pos])  # (ean, quantidade recebida)
                    lst_itens_recebidos.append(zipped_2)
                    zipped_3 = (int(result_conferencia[pos]) - int(qtde_pedido))
                    lst_diferenca.append(zipped_3)
                    pos += 1

                print(f'lst_pedido_p_conferencia : {lst_pedido_p_conferencia}')
                print(f'lst_itens_recebidos : {lst_itens_recebidos}')
                print(f'lista_diferenca : {lst_diferenca}')
                for a, b in zip(lst_itens_recebidos, lst_pedido_p_conferencia):
                    print(f'{b[0]} | {a[1]}, {b[1]} | dif= { int(a[1]) - int(b[1])}')

        except Exception as e:
            print(e)

    return render_template('logistica/entrada_ordem_compra.html',
                           form_entrada_ordem_compra=form_entrada_ordem_compra,
                           lst_nf=lst_nf,
                           lst_diferenca=lst_diferenca,
                           lst_itens_recebidos=lst_itens_recebidos,
                           result_conferencia=result_conferencia,
                           itens_conferencia=itens_conferencia,
                           data=Formatadores.formatar_data(Formatadores.os_data()))
