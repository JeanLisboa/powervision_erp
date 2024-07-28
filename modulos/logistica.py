from flask import Flask, render_template, redirect, url_for, request, session
import modulos.admin
from forms import ModCompras, Mod_Comercial, Mod_Pricing, Mod_Logistica
from geral import Validadores, Formatadores, AtualizaCodigo, Buscadores, AlertaMsg
import geral

def entrada_ordem_compra():
    validacao_1 = ""
    validacao_2 = ""
    validacao_3 = ""
    validacao_4 = ""
    lst_nf = []

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

    # processamento do botão pesquisar ordem de compra
    if request.method == 'POST':
        try:
            if 'botao_pesquisar_ordem_compra' in request.form:
                print('botao_pesquisar_ordem ACIONADO')

            # pesquisa a ordem de compra no banco de dados
            if nf is not None:
                nome_arquivo = Buscadores.Xml.buscar_arquivo(nf)
                cnpj = Buscadores.Xml.buscar_cnpj(nome_arquivo)
                razao_social = Buscadores.Xml.buscar_razao_social(nome_arquivo)
                print('------------------------------------------------------------')
                print('------VALIDAÇÃO 1: VERIFICAR SE O XML ESTÁ NO SERVIDOR------')
                print('------------------------------------------------------------')
                # busca o pedido no xml
                pedido = Buscadores.Xml.buscar_pedido(nome_arquivo)
                print(f'pedido identificado no xml: {pedido}')
                lst_nf = [cnpj, razao_social, nf, pedido]
                print(f'a lst_nf será renderizada: {lst_nf}')
                # busca o pedido no banco de dados
                Validadores.valida_pedido_recebido(pedido)
                print(f'pasta_xml: {geral.pasta_xml}')
                print(f'{form_entrada_ordem_compra.nf.data}')

                if Buscadores.OrdemCompra.verifica_status_ordem(lst_nf[3]) is True:
                    validacao_1 = True

                else:
                    print('xml não encontrado')
                # ainda falta extrair os itens do xml para comparar com a ordem de compra
                # print(f'chave nf >>> {geral.Buscadores.OrdemCompra.buscar_nf(geral.pasta_xml, nome_arquivo, str(nf))}')
                # def buscar_nf(pasta_xml, chave_nf, nf):
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
    if validacao_1 and validacao_2 and validacao_3 and validacao_4:
        print('pedido validado')
        lst_nf.append('LIBERADO')
        print(lst_nf)
    if validacao_1 is False:
        lst_nf.append('NOTA FISCAL NÃO ENCONTRADA')
    if validacao_2 is False:
        lst_nf.append('FORNECEDOR NÃO CADASTRADO')
    if validacao_3 is False:
        lst_nf.append('PEDIDO NÃO ABERTO')
    if validacao_4 is False:
        lst_nf.append('PREÇO FORA DA POLÍTICA')

    return render_template('logistica/entrada_ordem_compra.html',
                           form_entrada_ordem_compra=form_entrada_ordem_compra, lst_nf=lst_nf,
                           data=Formatadores.formatar_data(Formatadores.os_data()))


def realizar_conferencia():
    form_pesquisar_ordem_compra = Mod_Logistica.Realizar_conferencia()
    ordem_compra = form_pesquisar_ordem_compra.data
    razao_social = form_pesquisar_ordem_compra.fornecedor.data

    if request.method == 'POST':
        if 'botao_pesquisar_ordem_compra' in request.form:
            print('botao_pesquisar_ordem ACIONADO')
            # ESTA INFORMAÇÃO DEVE VIR DA TELA ENTRADA DE ORDEM DE COMPRA.
            # A NF DEVE VIR DESTA TELA

    return render_template('logistica/realizar_conferencia.html',
                           form_pesquisar_ordem_compra=form_pesquisar_ordem_compra,
                           ordem_compra=ordem_compra,
                           razao_social=razao_social)

