import datetime
import logging
from datetime import date
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

        try:
            if 'botao_pesquisar' in request.form:
                logging.info('Botão pesquisar pressionado')
                try:
                    fornecedor = form_precificacao.fornecedor.data or ''
                    relatorio_precificacao = Pricing.relato_custos(ean, fornecedor, unidade, descricao)
                    relato_pesquisa = Pricing.relato_bd_precificacao(ean)
                    session['relatorio_precificacao'] = relatorio_precificacao
                    relatorio_temp = []
                    for i in relatorio_precificacao:
                        logging.debug(f'relatorio_precificacao: {i}')
                        for ean_ in relato_pesquisa:
                            if ean_[1] == i[3]:
                                temp = (i, ean_[3], ean_[4], ean_[5], ean_[6], ean_[7])
                                relatorio_temp.append(temp[:])
                                break  # achou, não precisa verificar mais
                        else:
                            temp = (i, 0.0, 0.0, 0.0, 0.0, 0.0)
                            relatorio_temp.append(temp[:])
                    relatorio_precificacao = relatorio_temp
                    session['relatorio_temp'] = relatorio_temp
                    session['relatorio_precificacao'] = relatorio_precificacao
                    relatorio_precificacao_ajustado = [i[0] + i[1:] for i in relatorio_precificacao]
                    relatorio_precificacao = relatorio_precificacao_ajustado  #organiza a tupla
                    return render_template('pricing/precificacao.html',form_precificacao=form_precificacao,
                                           relatorio_precificacao=relatorio_precificacao)

                except Exception as e:
                    logging.error(f'Erro ',e)

        except Exception as e:
            logging.error(f'Erro ',e)

        try:
            if 'botao_salvar' in request.form:
                logging.info('Botão salvar pressionado')
                relatorio_precificacao = session.get('relatorio_precificacao')
                for i in relatorio_precificacao:
                    try:
                        logging.info('Pricing.salvar_precificacao(relatorio_precificacao,usuario)')
                        Pricing.salvar_precificacao(relatorio_precificacao,usuario)

                    except Exception as e:
                        logging.info(f'Erro no if botao_salvar ',e)

        except Exception as e:
            logging.info(f'Erro no try do botao_salvar ',e)


        try:
            if 'botao_calcular' in request.form:
                # FIXME: CORRIGIR BOTAO CALCULAR. A TABELA SOME DA TELA, AO CLICAR NO BOTAO CALCULAR PELA SEGUNDA VEZ
                relatorio_precificacao = session.get('relatorio_precificacao')
                relatorio_temp = session.get('relatorio_temp')

                for i in relatorio_precificacao:
                    logging.debug(f'relatorio_precificacao: {i}')

                logging.info(CorFonte.fonte_verde()+
                             'Botão calcular pressionado' + CorFonte.reset_cor())
                try:
                    item_selecionado = request.form.getlist("incluir_item")
                    logging.debug(f'item_selecionado >>> {item_selecionado}')
                    lista_final = []
                    lista_temp = []
                    margens = []
                    custos = []
                    precos = []
                    acrescimo = []
                    desconto = []

                    # prepara os dados para o calculo
                    num_linhas = len(relatorio_precificacao)
                    for i in range(num_linhas):
                        margem = request.form.get(f"margem_{i}")
                        if margem == '' or margem is None:
                            margem = 0.0
                        custo_total = request.form.get(f"custo_total_{i}")
                        if custo_total == '' or custo_total is None:
                            custo_total = 0.0
                        preco_final = request.form.get(f"preco_final_{i}")
                        if preco_final == '' or preco_final is None:
                            preco_final = 0.0

                        margens.append(margem)
                        custos.append(custo_total)
                        precos.append(preco_final)
                        acrescimo.append(request.form.get(f"acrescimo_{i}"))
                        if acrescimo[i] == '' or acrescimo[i] is None:
                            acrescimo[i] = 0.0
                            # print(f'acrescimo: {acrescimo[i]}')
                        desconto.append(request.form.get(f"desconto_{i}"))
                        if desconto[i] == '' or desconto[i] is None:
                            desconto[i] = 0.0
                    # recebe os dados dos inputs
                    for m, c, p, a, d in zip(margens, custos, precos, acrescimo, desconto):
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
                    print('for i in relatorio_precificacao:')
                    # FIXME: LOCALIZAR ERRO NO FOR, POIS ESTÁ DANDO ERRO NO CÁLCULO
                    for i in relatorio_precificacao:
                        print(i)
                        m = lista_final[cont][0]  # converte a margem para decimal
                        # print(f'm: {m}')
                        # print(f'custo variável: {relatorio_precificacao[cont][0][7]}')
                        # print(f'custo fixo: {lista_final[cont][1]}')
                        c = lista_final[cont][1] + relatorio_precificacao[cont][0][7]  # soma o custo do produto ao custo variável

                        a = lista_final[cont][2] / 100  # converte o acrescimo para decimal
                        d = lista_final[cont][3] / 100  # converte o desconto para decimal
                        p = c / (1 - (m/100))
                        p = p + (p * a) - (p * d)
                        # m = m * 100 # converte a margem para porcentagem para enviar para o template
                        a = a * 100 # converte o acrescimo para porcentagem para enviar para o template
                        c = lista_final[cont][1] # retorna o custo conforme informado pelo usuario
                        d = d * 100 # converte o desconto para porcentagem para enviar para o template
                        i = i[0] + (round(m, 1),round(c, 2) , round(a, 1), round(d, 1), round(p, 2))  # casas decimais

                        relatorio_precificacao_novo.append(i[:])  # adiciona o novo item ao relatorio
                        # print('relatorio_precificacao_novo, após o append')
                        # print(relatorio_precificacao_novo)
                        cont += 1
                    # logging.info('relatorio_precificacao_novo')
                    relatorio_precificacao = relatorio_precificacao_novo  # renomeia a lista para a lista original, depois do calculo, com o valor preco_final

                    for i in relatorio_precificacao:
                        data_str = i[0]
                        data_formatada = datetime.datetime.strptime(data_str, '%a, %d %b %Y %H:%M:%S %Z').date()

                        # Substitui a data na tupla (cria nova tupla com a data convertida)
                        i_ajustado = (data_formatada, *i[1:])
                        # print(i_ajustado)
                    logging.debug('relatorio_precificacao')
                    logging.debug(relatorio_precificacao)
                    session['relatorio_precificacao'] = relatorio_precificacao  # salva o relatorio para salvar
                    return render_template('pricing/precificacao.html',
                                           form_precificacao=form_precificacao,
                                           relatorio_precificacao=relatorio_precificacao)

                except Exception as e:
                    pass
                    # logging.error(f'Erro no try dentro da função calcular ',e)

        except Exception as e:
            logging.error(f'erro for do try da função calcular ',e)

        try:
            if 'botao_cancelar' in request.form:
                logging.info('Botão cancelar pressionado')
                return render_template('pricing/precificacao.html', form_precificacao=form_precificacao)
        except Exception as e:
            logging.error(f'Erro',e)

    relatorio_precificacao = session.get('relatorio_precificacao')
    return render_template(
        "pricing/precificacao.html",
        data=Formatadores.formatar_data(Formatadores.os_data()),
        form_precificacao=form_precificacao,

        # relatorio_precificao=relatorio_precificacao,
    )

