from flask import render_template, request, session
from modulos.utils.console import CorFonte
from modulos.utils.buscadores import Buscadores, Estoque
from forms import ModGestaoCarteira
from modulos.utils.queries import mydb, mycursor


def gestao_carteira():
    """
    Processamento de Gestão de Carteira com cálculo de estoque alocado e livre.
    LEGENDA DE CORES (Sugestão para o Front-end):
    0: Vermelho (Sem estoque)
    1: Amarelo (Parcial)
    2: Verde (Atendida)

    """

    print(CorFonte.fonte_amarela() + "Iniciando Processamento de Carteira" + CorFonte.reset_cor())
    form_gestao_carteira = ModGestaoCarteira.GestaoCarteira()

    # 1. ESTADO INICIAL (Carrega as OVs para a Tabela Superior)
    lista_ordem_venda_base = Buscadores.OrdemVenda.buscar_pedidos()
    print(f'lista_ordem_venda_base: {lista_ordem_venda_base}')

    # Recupera o estado da sessão
    ordem_selecionada = session.get('ordem_selecionada')
    ordem_alocada_ids = session.get('ordem_alocada', [])

    # 2. PROCESSAMENTO DO FORMULÁRIO (POST)
    if form_gestao_carteira.validate_on_submit():
        # Radio: Qual OV visualizar detalhes
        ordem_radio = request.form.get('ordem_venda')
        if ordem_radio:
            ordem_selecionada = int(ordem_radio)
            session['ordem_selecionada'] = ordem_selecionada

        # Checkbox: Quais OVs reservar estoque
        alocadas_form = request.form.getlist('ordem_alocada')
        ordem_alocada_ids = [int(o) for o in alocadas_form]
        session['ordem_alocada'] = ordem_alocada_ids

    # 3. CÁLCULO DA DEMANDA TOTAL (Soma de todas as OVs marcadas no checkbox)
    demanda_total_por_ean = {}
    if ordem_alocada_ids:
        try:
            mydb.connect()
            mycursor = mydb.cursor()
            parametros = tuple(ordem_alocada_ids)
            placeholders = ",".join(["%s"] * len(parametros))

            query = f"""
                SELECT ean, SUM(quantidade) 
                FROM ordem_venda 
                WHERE ordem_venda IN ({placeholders})
                GROUP BY ean
            """
            mycursor.execute(query, parametros)
            demanda_total_por_ean = dict(mycursor.fetchall())
            mycursor.close()
        except Exception as e:
            print(f"Erro ao calcular demanda de estoque: {e}")

    # 3.1 CÁLCULO DE STATUS LINHA A LINHA PARA A LISTA DE ORDENS ---
    lista_ordem_venda_com_legenda = []

    for ov in lista_ordem_venda_base:
        id_ov = ov[0]  # Assumindo que o ID da OV é o primeiro elemento
        itens_ov_status = Buscadores.OrdemVenda.buscar_itens(id_ov)

        verificador_status_ov = []
        for item in itens_ov_status:
            # item[8] = Qtd Pedida | item[10] = Estoque Total
            q_pedida = float(item[8])
            e_total = float(item[10])

            if e_total >= q_pedida:
                verificador_status_ov.append(2)  # Verde
            elif e_total > 0:
                verificador_status_ov.append(1)  # Amarelo
            else:
                verificador_status_ov.append(0)  # Vermelho

        # Lógica de Agrupamento: O status da OV é o "pior" status entre seus itens
        if not verificador_status_ov:
            status_final = 0
        elif all(x == 2 for x in verificador_status_ov):
            status_final = 2
        elif any(x == 0 for x in verificador_status_ov) and any(x > 0 for x in verificador_status_ov):
            status_final = 1  # Se tem algum zerado mas outros com estoque, é parcial
        elif all(x == 0 for x in verificador_status_ov):
            status_final = 0
        else:
            status_final = 1

        # Adiciona o status calculado como um novo elemento na tupla da OV
        lista_ordem_venda_com_legenda.append(ov + (status_final,))

    # 4. PROCESSAMENTO DOS ITENS DA ORDEM SELECIONADA (Tabela Detalhada Inferior)
    lista_itens_ordem_expandida = []
    if ordem_selecionada:
        itens_originais = Buscadores.OrdemVenda.buscar_itens(ordem_selecionada)

        for item in itens_originais:
            ean = item[4]
            qtd_pedida = float(item[8])
            estoque_total_fisico = float(item[10])
            demanda_marcada = demanda_total_por_ean.get(ean, 0.0)

            # Lógica de Alocação
            if ordem_selecionada in ordem_alocada_ids:
                if estoque_total_fisico >= demanda_marcada:
                    alocado_nesta_ov = qtd_pedida
                else:
                    alocado_nesta_ov = min(qtd_pedida, max(0, estoque_total_fisico))
            else:
                alocado_nesta_ov = 0.0

            # Cálculo do Estoque Livre
            qtde_estoque_livre = max(0, estoque_total_fisico - demanda_marcada)

            # Expande a tupla com Alocado (11) e Livre (12)
            lista_itens_ordem_expandida.append(item + (alocado_nesta_ov, qtde_estoque_livre))

    if 'botao_liberar_ov' in request.form:

        print('botao_liberar_ov acionado')

    # print(f'lista_ordem_venda_com_legenda: {lista_ordem_venda_com_legenda}')
    # print(f'lista_ordem_venda_base: {lista_ordem_venda_base}')
    # print(f'lista_itens_ordem_expandida: {lista_itens_ordem_expandida}')
    return render_template(
        'gestao_carteira/gestao_carteira.html',
        lista_ordem_venda=lista_ordem_venda_com_legenda,  # Agora enviamos a lista com status
        lista_itens_ordem_expandida=lista_itens_ordem_expandida,
        form_gestao_carteira=form_gestao_carteira,
        ordem_selecionada=ordem_selecionada,
        ordem_alocada=ordem_alocada_ids
    )