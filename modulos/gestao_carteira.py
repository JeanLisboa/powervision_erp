from flask import render_template, request, session
from modulos.utils.console import CorFonte
from modulos.utils.buscadores import Buscadores, Estoque
from forms import ModGestaoCarteira

def gestao_carteira():
        """
            FLUXO DE PROCESSAMENTO
            *** INCLUIR BOTAO DE LIBERAÇÃO DO PEDIDO

            LAYOUT DA TELA DE GESTÃO DE CARTEIRA:
                - LEGENDA:
                    - SINAL VERDE: ORDEM DE VENDA OU ITEM COMPLEMENTE ATENDIDA
                    - SINAL AMARELO: ORDEM DE VENDA OU ITEM PARCIALMENTE ATENDIDA
                    - SINAL VERMELHO: ORDEM DE VENDA OU ITEM NÃO ATENDIDA

            0 - AO ACESSAR A TELA, AS ORDENS EM ABERTO E PENDENTES DEVEM APARECER SEM AÇÃO DO USUÁRIO
            0.1 - O USUARIO DEVE TER A VISAO DO ESTOQUE TOTAL E ESTOQUE ALOCADO.

            1 - NA PARTE SUPERIOR DA TELA, O USUARIO SELECIONA A ORDEM DE VENDA E OS RESPECTIVOS ITENS DEVERÃO APARECER NA PARTE INFERIOR.
            1.1 - NA PARTE INFERIOR, O USUÁRIO VISUALIZARÁ LINHA A LINHA: OS ITEM, QTDE, ESTOQUE LIVRE E ALOCADO
            2 - NA PARTE SUPERIOR DA TELA, O USUARIO TEM A OPÇÃO DE

        """

        print(CorFonte.fonte_amarela() + "Função gestao_carteira" + CorFonte.reset_cor())

        form_gestao_carteira = ModGestaoCarteira.GestaoCarteira()

        # ===== Estado inicial =====
        lista_ordem_venda = Buscadores.OrdemVenda.buscar_pedidos()
        lista_itens_ordem = []

        ordem_selecionada = session.get('ordem_selecionada')
        ordem_alocada = session.get('ordem_alocada', [])  # SEMPRE lista

        # ===== POST =====
        if form_gestao_carteira.validate_on_submit():

            # ---- RADIO (navegação) ----
            ordem = request.form.get('ordem_venda')
            if ordem:
                ordem_selecionada = int(ordem)
                session['ordem_selecionada'] = ordem_selecionada
                lista_itens_ordem = Buscadores.OrdemVenda.buscar_itens(ordem_selecionada)
                # estoque_livre = Estoque.informa_estoque_livre(ean)
                print('-'*50)
                lista_estoque_total = []
                for i in lista_itens_ordem:
                    print(f'i: {i}')
                    print(f'i: {i[4]}')
                    # estoque_total = Estoque.informa_estoque_livre(i[4])
                    # lista_estoque_total.append(estoque_total[:])

                print('-'*50)
                print(f'lista_estoque_total: {lista_estoque_total}')
            else:
                session.pop('ordem_selecionada', None)
                ordem_selecionada = None
                lista_itens_ordem = []

            # ---- CHECKBOX (ação futura) ----
            ordem_alocada = request.form.getlist('ordem_alocada')
            ordem_alocada = [int(o) for o in ordem_alocada]
            session['ordem_alocada'] = ordem_alocada

            print(f'Ordem selecionada (radio): {ordem_selecionada}')
            print(f'Ordens marcadas para alocar (checkbox): {ordem_alocada}')

        if not ordem_alocada:
            ordem_alocada = []
        return render_template(
            'gestao_carteira/gestao_carteira.html',
            estoque_total='',
            lista_ordem_venda=lista_ordem_venda,
            lista_itens_ordem=lista_itens_ordem,
            form_gestao_carteira=form_gestao_carteira,
            ordem_selecionada=ordem_selecionada,
            ordem_alocada=ordem_alocada
        )
