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
                    relatorio_precificacao = Pricing.precificacao()
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
                    print(f'Erro ',e)

        except Exception as e:
            print(f'Erro ',e)


        try:
            if 'botao_calcular' in request.form:
                relatorio_precificacao = session.get('relatorio_precificacao')
                print('Botão calcular pressionado')
                try:
                    item_selecionado = request.form.getlist("incluir_item")
                    print(f'item_selecionado >>> {item_selecionado}')
                    lista_final = []
                    lista_temp = []
                    margens = []
                    custos = []
                    precos = []
                    markup = []
                    acrescimo = []
                    desconto = []

                    # Supondo que você saiba o número de linhas
                    num_linhas = len(relatorio_precificacao)

                    for i in range(num_linhas):
                        margem = request.form.get(f"margem_{i}")
                        custo_total = request.form.get(f"custo_total_{i}")
                        preco_final = request.form.get(f"preco_final_{i}")
                        margens.append(margem)
                        custos.append(custo_total)
                        precos.append(preco_final)
                        markup.append(request.form.get(f"markup_{i}"))
                        acrescimo.append(request.form.get(f"acrescimo_{i}"))
                        desconto.append(request.form.get(f"desconto_{i}"))

                    print("Margens:", margens)
                    print("Custos:", custos)
                    print("Preços Finais:", precos)
                    print("Markup:", markup)
                    print("Acrescimo:", acrescimo)
                    print("Desconto:", desconto)

                    return render_template('pricing/precificacao.html', form_precificacao=form_precificacao)

                except Exception as e:
                    print(f'Erro ',e)


        except Exception as e:
            print(f'erro ',e)

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

