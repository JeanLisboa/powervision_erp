from modulos.utils.console import CorFonte
# from modulos.utils.carteira_service import buscar_itens_pedido, buscar_pedidos_resumo
from flask import render_template, request,session
from flask_wtf import FlaskForm
from modulos.utils.console import CorFonte
from modulos.utils.buscadores import Buscadores
from forms import ModGestaoCarteira

def gestao_carteira():
    print(CorFonte.fonte_amarela() + "Função gestao_carteira" + CorFonte.reset_cor())

    form_gestao_carteira = ModGestaoCarteira.GestaoCarteira()

    lista_ordem_venda = Buscadores.OrdemVenda.buscar_pedidos()
    lista_itens_ordem = []   # <<< OBRIGATÓRIO
    ordem_selecionada = session.get('ordem_selecionada')

    if form_gestao_carteira.validate_on_submit():
        ordem = request.form.get('ordem_venda')

        if ordem:
            ordem_selecionada = int(ordem)
            session['ordem_selecionada'] = ordem_selecionada
            lista_itens_ordem = Buscadores.OrdemVenda.buscar_itens(ordem_selecionada)

            print(f'ordem selecionada: {ordem_selecionada}')
            print(f'lista_itens_ordem: {lista_itens_ordem}')
        else:
            session.pop('ordem_selecionada', None)
            ordem_selecionada = None
            lista_itens_ordem = []

    return render_template(
        'gestao_carteira/gestao_carteira.html',
        lista_ordem_venda=lista_ordem_venda,
        lista_itens_ordem=lista_itens_ordem,
        form_gestao_carteira=form_gestao_carteira,
        ordem_selecionada=ordem_selecionada
    )
