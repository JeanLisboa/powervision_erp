import datetime
import logging
import ast
from datetime import date, datetime
from modulos.utils.formatadores import Formatadores
from modulos.utils.buscadores import Buscadores
from modulos.admin import usuario
from forms import ModPricing

from flask import render_template, redirect, url_for, request, session
from modulos.utils.buscadores import Pricing
from modulos.utils.console import CorFonte
data = Formatadores.os_data()
data_hoje = date.strftime(data, '%Y-%m-%d')

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
logging.debug('Iniciando o Programa')
logging.disable(logging.CRITICAL)  # comente para habilitar
logging.disable(logging.WARNING)  # comente para habilitar
logging.disable(logging.INFO)  # comente para habilitar
logging.disable(logging.DEBUG)  # comente para habilitar

"""
:return: indicadores por sku:
    precificacao = Precificacao()
    precificacao.margem_lucro_ideal()
    precificacao.margem_lucro_minima()
    precificacao.preco_concorrencia()
    precificacao.valor_percebido()
    precificacao.rateio_custos() # custos fixos ou variaveis
    precificacao.custo_total() # custo_compra + rateio_custos
    precificacao.markup() # preço de venda / custo_total
    precificacao.markup_2() # 1/(1 - margem) para calcular o markup de acordo com a margem desejada.
    exemplo: para um lucro desejado de 30% : 1/(1 - 0.3)
    precificacao.preco_final() # custo_total * markup

"""
def precificacao():
    logging.info(CorFonte.fonte_amarela() + "class Precificacao" + CorFonte.reset_cor())
    data = Formatadores.os_data()
    logging.info(data)
    form_precificacao = ModPricing.Precificacao()
    fornecedor = form_precificacao.fornecedor.data
    ean = form_precificacao.ean.data
    unidade = form_precificacao.unidade.data
    descricao = form_precificacao.descricao.data
    if request.method == 'POST':

        if 'botao_pesquisar' in request.form:
                logging.debug(CorFonte.fonte_verde()+ 'Botão pesquisar pressionado' + CorFonte.reset_cor())
                try:
                    fornecedor = form_precificacao.fornecedor.data or ''

                    # LISTA DE PRODUTOS CADASTRADOS
                    relatorio_precificacao = Pricing.relato_custos(ean, fornecedor, unidade, descricao)
                    logging.debug(f'0 - relatorio_precificacao: {relatorio_precificacao}')

                    # PESQUISA SE O(S) PRODUTO(S) EXISTE NA TABELA PRECIFICAÇÃO
                    relato_pesquisa = Pricing.relato_bd_precificacao(ean)
                    logging.debug(f'1 - relato_pesquisa: {relato_pesquisa}')
                    session['relatorio_precificacao'] = relatorio_precificacao

                    relatorio_temp = []

                    # AJUSTA 'relatorio_precificacao' PARA RENDERiZAR
                    for i in relatorio_precificacao:
                        logging.debug(f'2 - relatorio_precificacao: {i}')
                        i_atualizado = (i[4], i[3], i[5], i[8])
                        i = i_atualizado
                        logging.debug(f'2.1 - i = i_atualizado: {i}')

                        # INCLUI AS INFORMAÇÕES DA TABELA PRECIFICAÇÃO
                        logging.debug(f'3 - relatorio_precificacao_atualizado: {i}')
                        for ean_ in relato_pesquisa:
                            logging.debug(f'4 - dentro do for de relato_pesquisa')
                            logging.debug(f'4.1 - busca {i[1]} na tabela precificação')
                            logging.debug(f'5 - ean_[1]:{ean_[1]} i[3]:{i[1]}')
                            if ean_[1] == i[1]:
                                logging.debug(f'{i[1]} localizado no bd, tabela precificação')
                                try:
                                    logging.debug(f'5.1 dentro do try')
                                    temp = (i, ean_[3], ean_[4], ean_[5], ean_[6], ean_[7])
                                    logging.debug(f'6 - temp: {temp}')
                                except Exception as e:
                                    logging.debug('7 - Erro', e)
                                relatorio_temp.append(temp[:])
                                break  # achou, não precisa verificar mais
                            else:
                                logging.debug(f'ean {i[1]} não localizado no bd')
                        else:
                            # CASO NÃO HAJA INFORMAÇÃO CADASTRADA NA TABELA PRECIFICAÇÃO
                            logging.debug(f'8 - relatorio_precificacao(i): {i}')
                            logging.debug('9 - Ajustando "i" para renderizar')
                            temp = (i, 0.0, 0.0, 0.0, 0.0, 0.0)
                            relatorio_temp.append(temp[:])

                    relatorio_precificacao = relatorio_temp
                    session['relatorio_temp'] = relatorio_temp
                    logging.debug(f'10 - relatorio_temp: {relatorio_temp}')
                    relatorio_precificacao_ajustado = [i[0] + i[1:] for i in relatorio_precificacao]
                    relatorio_precificacao = relatorio_precificacao_ajustado  #organiza a tupla
                    session['relatorio_precificacao'] = relatorio_precificacao
                    logging.debug('11 - relatorio_precificacao_final')
                    logging.debug(relatorio_precificacao)
                    session['relato_pesquisa'] = relato_pesquisa
                    return render_template('pricing/precificacao.html',form_precificacao=form_precificacao,
                                           relatorio_precificacao=relatorio_precificacao)

                except Exception as e:
                    logging.error(f'Erro ',e)

        if 'botao_calcular' in request.form:
                logging.debug(CorFonte.fonte_verde()+'Botão calcular pressionado' + CorFonte.reset_cor())


                # RECUPERA 'relatorio_precificacao' DO ACIONAMENTO DO BOTÃO PESQUISAR
                # relatorio_precificacao = session.get('relatorio_precificacao')
                relatorio_precificacao = Pricing.relato_custos(ean, fornecedor, unidade, descricao)
                relatorio_temp = session.get('relatorio_temp')
                try:
                    item_selecionado = request.form.getlist("incluir_item")
                    logging.debug(f'item_selecionado >>> {item_selecionado}')
                    lista_final = []
                    lista_temp = []
                    margens = []
                    custos = []
                    precos = []
                    acrescimos = []
                    descontos = []
                    m = 0.0
                    c = 0.0
                    a = 0.0
                    d = 0.0
                    p = 0.0

                    # >>> PREPARA OS DADOS PARA O CÁLCULO <<<

                    # IDENTIFICA O NUMERO DE LINHAS ( TUPLAS ) DA LISTA relatorio_precificacao
                    num_linhas = len(relatorio_precificacao)

                    # logging.debug('num_linhas de relatorio_precificacao >>> ', num_linhas)
                    for i in range(num_linhas):
                        # RECUPERA OS INPUTS DO USUARIO

                        margem = request.form.get(f"margem_{i}") # RECUPERA MARGEM
                        if margem == '' or margem is None:
                            margem = 0.0
                        logging.debug(f'margem >>> {margem} | type(margem) >>> {type(margem)}')

                        custo_total = request.form.get(f"custo_total_{i}")
                        if custo_total == '' or custo_total is None:
                            custo_total = 0.0
                        logging.debug(f'custo_total >>> {custo_total} | type(custo_total) >>> {type(custo_total)}')

                        try:
                            logging.debug(f'validacao_preco_final {validacao_preco_final}')
                            if preco_final == validacao_preco_final:
                                logging.debug('preco_final não alterado')
                            else:
                                logging.debug('preco_alterado')


                        except Exception as e:
                            logging.debug(f'Erro na validacao de preco_final ', e)

                        preco_final = request.form.get(f"preco_final_{i}")
                        if preco_final == '' or preco_final is None:
                            preco_final = 0.0
                        logging.debug(f'preco_final >>> {preco_final} | type(preco_final) >>> {type(preco_final)}')

                        validacao_preco_final = preco_final[:]
                        logging.debug(f'validacao_preco_final >>> {validacao_preco_final}')

                        try:
                            logging.debug(f'validacao_preco_final {validacao_preco_final}')
                            if preco_final == validacao_preco_final:
                                logging.debug('preco_final não alterado')
                            else:
                                logging.debug('preco_alterado')


                        except Exception as e:
                            logging.debug(f'Erro na validacao de preco_final ', e)



                        acrescimo = request.form.get(f"acrescimo_{i}")
                        if acrescimo == '' or acrescimo is None:
                            acrescimo = 0.0
                        logging.debug(f'acrescimo: {acrescimo} | type(acrescimo) >>> {type(acrescimo)}')

                        desconto = request.form.get(f"desconto_{i}")
                        if desconto == '' or desconto is None:
                            desconto = 0.0
                        logging.debug(f'desconto: {desconto} | type(desconto) >>> {type(desconto)}')

                        margens.append(float(margem))
                        logging.debug(f'lista margens: {margens}')

                        custos.append(float(custo_total))
                        logging.debug(f'lista custos: {custos}')

                        precos.append(float(preco_final))
                        logging.debug(f'lista precos: {precos}')

                        acrescimos.append(float(acrescimo))
                        logging.debug(f'lista acrescimos: {acrescimos}')

                        descontos.append(float(desconto))
                        logging.debug(f'lista descontos: {descontos}')



                    # recebe os dados dos inputs
                    for m, c, p, a, d in zip(margens, custos, precos, acrescimos, descontos):
                        m = float(m)
                        c = float(c)
                        a = float(a)
                        d = float(d)
                        p = float(p)
                        lista_temp.append(m)
                        lista_temp.append(c)
                        lista_temp.append(a)
                        lista_temp.append(d)
                        lista_temp.append(p)
                        lista_final.append(lista_temp[:])
                        lista_temp.clear()

                    relatorio_precificacao_novo = []

                    # realiza o calculo
                    cont = 0
                    relatorio_temp = session.get('relatorio_temp')

                    logging.debug(f'relatorio_precificacao >>> {relatorio_precificacao}')
                    logging.debug(f'relatorio_temp >>> {relatorio_temp}')
                    logging.debug(f'lista_final >>> {lista_final}')
                    logging.debug('for i in relatorio_precificacao:')
                    for i in relatorio_precificacao:
                        logging.debug(i)
                        m = lista_final[cont][0]  # converte a margem para decimal
                        logging.debug(f'm: {m}')
                        custo_produto = float(lista_final[cont][1])
                        custo_variavel = float(i[8])
                        logging.debug(f'custo_produto >>> {custo_produto} | type {type(custo_produto)}')
                        logging.debug(f'custo_variavel >>> {custo_variavel} | type {type(custo_variavel)}')

                        c = custo_produto + custo_variavel    # soma o custo do produto ao custo variável
                        logging.debug(f'c: {c}')

                        a = lista_final[cont][2] / 100  # converte o acrescimo para decimal
                        logging.debug(f'a: {a}')

                        try:
                            d = lista_final[cont][3] / 100  # converte o desconto para decimal
                            logging.debug(f'd: {d}')
                        except Exception as e:
                            logging.debug('Erro', e)
                            d = 0.0
                        logging.debug(f'p: {p}')
                        try:
                            logging.debug(f'm: {m} >>> {1-m}')
                            logging.debug(f'c: {c}')
                            logging.debug(f'a: {a}')
                            logging.debug(f'd: {d}')
                            logging.debug(f'cálculo do preco_final(p):  {c} / (1 - ({m}/100)) ')
                            p = c / (1 - (m/100))  # PRECO FINAL = CUSTO DO PRODUTO - (MARGEM/100))

                            p = p + (p * a) - (p * d)
                            logging.debug(f'preco_final: {p}')

                        except Exception as e:
                            logging.debug(f'erro, {e}')

                        # converte a margem para porcentagem para enviar para o template
                        logging.debug('Converte a margem para porcentagem para enviar para o template')

                        a = a * 100 # converte o acrescimo para porcentagem para enviar para o template
                        logging.debug(f'a: {a}')

                        c = lista_final[cont][1] # retorna o custo conforme informado pelo usuario
                        logging.debug(f'c: {c}')

                        d = d * 100 # converte o desconto para porcentagem para enviar para o template
                        logging.debug(f'd: {d}')

                        logging.debug(f'i[0]{i[0]}')
                        logging.debug(f'round(m, 1) {round(m, 1)}')
                        logging.debug(f'round(c, 2) {round(c, 2)}')
                        logging.debug(f'round(a, 1) {round(a, 1)}')
                        logging.debug(f'round(d, 1) {round(d, 1)}')
                        logging.debug(f'round(p, 2) {round(p, 2)}')
                        try:
                            calculos = (i[0], round(m, 1),round(c, 2) , round(a, 1), round(d, 1), round(p, 2))  # casas decimais
                            logging.debug(f'calculos: {calculos}')
                        except Exception as e:
                            logging.debug(f'Erro ',e)
                        logging.debug(f'relatorio_precificacao_novo antes do append: {relatorio_precificacao_novo}')
                        try:
                            logging.debug(f'i: {i}')
                            data_retorno = data_hoje
                            ean_retorno = i[3]
                            valor_retorno = i[8]
                            margem_retorno = round(m, 1)
                            custo_retorno = round(c, 2)
                            acrescimo_retorno = round(a, 1)
                            desconto_retorno = round(d, 1)
                            preco_venda_retorno = round(p, 2)
                            usuario_retorno = usuario
                            descricao_retorno = i[4]
                            un_retorno = i[5]
                            linha = [
                                descricao_retorno,
                                ean_retorno,
                                un_retorno,
                                valor_retorno,
                                margem_retorno,
                                custo_retorno,
                                acrescimo_retorno,
                                desconto_retorno,
                                preco_venda_retorno
                            ]
                            relatorio_precificacao_novo.append(linha)
                        except Exception as e:
                            logging.debug(f'Erro ',e)

                        logging.debug('relatorio_precificacao_novo, após o append')
                        logging.debug(relatorio_precificacao_novo)
                        cont += 1
                    relatorio_precificacao = relatorio_precificacao_novo  # renomeia a lista para a lista original, depois do calculo, com o valor preco_final

                    logging.debug('relatorio_precificacao final')
                    logging.debug(relatorio_precificacao)
                    for i in relatorio_precificacao:
                        logging.debug(i)


                    session['relatorio_precificacao'] = relatorio_precificacao  # salva o relatorio
                    return render_template('pricing/precificacao.html',
                                           form_precificacao=form_precificacao,
                                           relatorio_precificacao=relatorio_precificacao)

                except Exception as e:
                    logging.debug(f'Erro ',e)

                    # logging.error(f'Erro no try dentro da função calcular ',e)

        try:
            if 'botao_salvar' in request.form:
                tupla_ean_bd = ()
                logging.debug(CorFonte.fonte_verde() + 'Botão salvar pressionado' + CorFonte.reset_cor())
                relato_pesquisa = session.get('relato_pesquisa')
                logging.debug(f'1 - relato_pesquisa: {relato_pesquisa}')
                logging.debug(f'2 - len(relato_pesquisa): {len(relato_pesquisa)}')
                relatorio_precificacao = session.get('relatorio_precificacao')
                busca_ean_tabela = Pricing.relato_bd_precificacao(ean)
                logging.debug(f'busca_ean_tabela: {busca_ean_tabela}')
                logging.debug('processamento de atualização / salvamento dos registros')
                logging.debug(Pricing.relato_geral_bd_precificacao())
                for i in relatorio_precificacao:
                    if i[1] in Pricing.relato_geral_bd_precificacao():
                        logging.debug(f'ean {i[1]} localizado no bd ATUALIZAR REGISTRO')
                        Pricing.update_precificacao(relatorio_precificacao, usuario)
                    else:
                        logging.debug(f'ean {i[1]} NÃO localizado no bd CRIAR NOVO REGISTRO')
                        Pricing.salvar_precificacao(relatorio_precificacao, usuario)
                    logging.debug('-----------------------------------------------')

        except Exception as e:
            logging.debug(f'Erro no try do botao_salvar ',e)

        try:
            if 'botao_cancelar' in request.form:
                logging.debug('Botão cancelar pressionado')
                return render_template('pricing/precificacao.html', form_precificacao=form_precificacao)
        except Exception as e:
            logging.error(f'Erro',e)

    relatorio_precificacao = session.get('relatorio_precificacao')
    # fixme: AJUSTAR CAMPO PRECO_FINAL PARA QUE POSSIBILITE AO USUARIO ALTERAR O PRECO,
    #  E O CALCULO REVERSO SER EXECUTADO PARA ALTERAR A MARGEM S/ VENDA
    return render_template(
        "pricing/precificacao.html",
        data=Formatadores.formatar_data(Formatadores.os_data()),
        form_precificacao=form_precificacao,

        # relatorio_precificao=relatorio_precificacao,
    )

