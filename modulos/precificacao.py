from pyautogui import printInfo

from forms import ModPricing
from flask import render_template, redirect, url_for, request, session
from modulos.utils.formatadores import Formatadores
from modulos.utils.atualizadores import AtualizaCodigo
from modulos.utils.buscadores import Pricing
from modulos.utils.alertas import AlertaMsg
from modulos.utils.validadores import Validadores, ValidaStatusPedido, ValidacoesCadastroProduto
from modulos.utils.console import CorFonte


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
    print(CorFonte.fonte_amarela() + "class Precificacao" + CorFonte.reset_cor())
    data = Formatadores.os_data()
    form_precificacao = ModPricing.Precificacao()
    fornecedor = form_precificacao.fornecedor.data
    ean = form_precificacao.ean.data
    unidade = form_precificacao.unidade.data
    descricao = form_precificacao.descricao.data

    # margem_lucro = fornecedor.margem_lucro.data
    # custo_total = form_precificacao.custo_total.data
    # preco_final = form_precificacao.preco_final.data
    # markup = form_precificacao.markup.data
    # desconto = form_precificacao.desconto.data
    # acrescimo = form_precificacao.acrescimo.data
    relatorio_precificacao = []

    """
    sugestao de encapsulamento das funções dos calculos de margem
    class PrecificacaoService:
    def __init__(self, custo, margem):
        self.custo = custo
        self.margem = margem

    def markup(self):
        return 1 / (1 - self.margem)

    def preco_final(self):
        return self.custo * self.markup()
    ===================================================================
    if form_precificacao.botao_salvar.data:
    custo = form_precificacao.custo_total.data
    margem = form_precificacao.margem_lucro.data
    service = PrecificacaoService(custo, margem)
    preco_final = service.preco_final()
    form_precificacao.preco_final.data = preco_final
    """
    if request.method == 'POST':
        try:
            if 'botao_pesquisar' in request.form:
                print('Botão pesquisar pressionado')
                try:
                    if form_precificacao.fornecedor.data is None:
                        fornecedor = ''
                    relatorio_precificacao = Pricing.precificacao(ean, fornecedor, unidade, descricao)
                    session['relatorio_precificacao'] = relatorio_precificacao
                    print(relatorio_precificacao)




                    return render_template('pricing/precificacao.html',form_precificacao=form_precificacao,
                                           relatorio_precificacao=relatorio_precificacao)

                except Exception as e:
                    print(f'Erro ',e)

        except Exception as e:
            print(f'Erro ',e)

        try:
            if 'botao_salvar' in request.form:
                print('Botão salvar pressionado')
                try:
                    pass

                except Exception as e:
                    print(f'Erro no if botao_salvar ',e)

        except Exception as e:
            print(f'Erro no try do botao_salvar ',e)


        try:
            if 'botao_calcular' in request.form:
                relatorio_precificacao = session.get('relatorio_precificacao')
                print('relatorio precificacao recuperado>>> ',relatorio_precificacao)
                print('Botão calcular pressionado')
                try:
                    item_selecionado = request.form.getlist("incluir_item")
                    print(f'item_selecionado >>> {item_selecionado}')
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
                            margem = 0
                        custo_total = request.form.get(f"custo_total_{i}")
                        if custo_total == '' or custo_total is None:
                            custo_total = 0
                        preco_final = request.form.get(f"preco_final_{i}")
                        if preco_final == '' or preco_final is None:
                            preco_final = 0

                        margens.append(margem)
                        custos.append(custo_total)
                        precos.append(preco_final)
                        acrescimo.append(request.form.get(f"acrescimo_{i}"))
                        if acrescimo[i] == '' or acrescimo[i] is None:
                            acrescimo[i] = 0
                        desconto.append(request.form.get(f"desconto_{i}"))
                        if desconto[i] == '' or desconto[i] is None:
                            desconto[i] = 0

                    print("Margens:", margens)
                    print("Custos:", custos)
                    print("Preços Finais:", precos)
                    print("Acrescimo:", acrescimo)
                    print("Desconto:", desconto)
                    print('=========================================================================================')
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
                    for i in relatorio_precificacao:
                        m = lista_final[cont][0]  # converte a margem para decimal
                        c = lista_final[cont][1] + relatorio_precificacao[cont][7]  # soma o custo do produto ao custo variável
                        a = lista_final[cont][2] / 100  # converte o acrescimo para decimal
                        d = lista_final[cont][3] / 100  # converte o desconto para decimal
                        p = c / (1 - (m/100))
                        p = p + (p * a) - (p * d)
                        # m = m * 100 # converte a margem para porcentagem para enviar para o template
                        a = a * 100 # converte o acrescimo para porcentagem para enviar para o template
                        c = lista_final[cont][1] # retorna o custo conforme informado pelo usuario
                        d = d * 100 # converte o desconto para porcentagem para enviar para o template
                        i = i + (round(m, 1),round(c, 2) , round(a, 1), round(d, 1), round(p, 2))  # casas decimais
                        relatorio_precificacao_novo.append(i[:])  # adiciona o novo item ao relatorio
                        cont += 1

                    print('relatorio_precificacao_novo')
                    relatorio_precificacao = relatorio_precificacao_novo # renomeia a lista para a lista original, depois do calculo, com o valor preco_final
                    print('relatorio_precificacao')
                    print(relatorio_precificacao)

                    return render_template('pricing/precificacao.html',
                                           form_precificacao=form_precificacao,
                                           relatorio_precificacao=relatorio_precificacao)

                except Exception as e:
                    print(f'Erro no try dentro da função calcular ',e)


        except Exception as e:
            print(f'erro for do try da função calcular ',e)

        try:
            if 'botao_cancelar' in request.form:
                print('Botão cancelar pressionado')
                return render_template('pricing/precificacao.html', form_precificacao=form_precificacao)
        except Exception as e:
            print(f'Erro',e)

    relatorio_precificacao = session.get('relatorio_precificacao')
    return render_template(
        "pricing/precificacao.html",
        form_precificacao=form_precificacao,
        relatorio_precificao=relatorio_precificacao,
        data=data)

