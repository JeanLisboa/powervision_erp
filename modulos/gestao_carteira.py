from flask import render_template, request, session
from modulos.utils.console import CorFonte
from modulos.utils.buscadores import Buscadores, Estoque
from forms import ModGestaoCarteira
from modulos.utils.queries import mydb, mycursor

# def gestao_carteira():
#         """
#             FLUXO DE PROCESSAMENTO
#
#             LAYOUT DA TELA DE GESTÃO DE CARTEIRA:
#                 - LEGENDA:
#                     - SINAL VERDE: ORDEM DE VENDA OU ITEM COMPLEMENTE ATENDIDA
#                     - SINAL AMARELO: ORDEM DE VENDA OU ITEM PARCIALMENTE ATENDIDA
#                     - SINAL VERMELHO: ORDEM DE VENDA OU ITEM NÃO ATENDIDA
#
#             0 - AO ACESSAR A TELA, AS ORDENS EM ABERTO E PENDENTES DEVEM APARECER SEM AÇÃO DO USUÁRIO
#             0.1 - O USUARIO DEVE TER A VISAO DO ESTOQUE TOTAL E ESTOQUE ALOCADO.
#
#             1 - NA PARTE SUPERIOR DA TELA, O USUARIO SELECIONA A ORDEM DE VENDA E OS RESPECTIVOS ITENS DEVERÃO APARECER NA PARTE INFERIOR.
#             1.1 - NA PARTE INFERIOR, O USUÁRIO VISUALIZARÁ LINHA A LINHA: OS ITEM, QTDE, ESTOQUE LIVRE E ALOCADO
#             2 - NA PARTE SUPERIOR DA TELA, O USUARIO TEM A OPÇÃO DE
#
#         """
#
#         print(CorFonte.fonte_amarela() + "Função gestao_carteira" + CorFonte.reset_cor())
#
#         form_gestao_carteira = ModGestaoCarteira.GestaoCarteira()
#
#         # ===== Estado inicial =====
#         lista_ordem_venda = Buscadores.OrdemVenda.buscar_pedidos()
#         print(f'lista_ordem_venda: {lista_ordem_venda}')
#
#         lista_itens_ordem = []
#         lista_itens_ordem_expandida = []
#         ordem_selecionada = session.get('ordem_selecionada')
#         ordem_alocada = session.get('ordem_alocada', [])  # SEMPRE lista
#         # ===== POST =====
#         if form_gestao_carteira.validate_on_submit():
#
#             # ---- RADIO (navegação) ----
#             ordem = request.form.get('ordem_venda')
#             if ordem:
#                 ordem_selecionada = int(ordem)
#                 session['ordem_selecionada'] = ordem_selecionada
#                 lista_itens_ordem = Buscadores.OrdemVenda.buscar_itens(ordem_selecionada)
#                 print(f'lista_itens_ordem: {lista_itens_ordem}')
#                 print('-'*50)
#                 lista_estoque_total = []
#                 for i in lista_itens_ordem:
#                     print(f'i: {i}')
#
#                 print('-'*50)
#                 print(f'lista_estoque_total: {lista_estoque_total}')
#             else:
#                 session.pop('ordem_selecionada', None)
#                 ordem_selecionada = None
#                 lista_itens_ordem = []
#
#             # ---- CHECKBOX (ação futura) ----
#             ordem_alocada = request.form.getlist('ordem_alocada')
#             ordem_alocada = [int(o) for o in ordem_alocada] # transforma em int
#             session['ordem_alocada'] = ordem_alocada
#             print(f'Ordem selecionada (radio): {ordem_selecionada}')
#             print(f'Ordens marcadas para alocar (checkbox): {ordem_alocada}')
#
#             def teste(lista):
#                 print(CorFonte.fonte_amarela() + 'função teste' + CorFonte.reset_cor())
#                 if not lista:
#                     return []
#
#                 # 1 - recebe a lista de ordens de venda
#                 # 2 - retornar
#                 # 2.1 coluna 1: ean
#                 # 2.2 coluna 2: somatorio da quantidade lista_ordem_venda por ean
#                 # 2.3 coluna 3: total estoque
#                 try:
#                     mydb.connect()
#                     mycursor = mydb.cursor()
#                     lista = tuple(lista)
#                     if not lista:
#                         raise ValueError("Lista de ordens de venda vazia")
#
#                     placeholders = ",".join(["%s"] * len(lista))
#
#                     query = f"""
#                         SELECT
#                             ean,
#                             SUM(quantidade) AS qtde_total
#                         FROM ordem_venda
#                         WHERE ordem_venda IN ({placeholders})
#                         GROUP BY ean
#                     """
#
#                     mycursor.execute(query, lista)
#                     resultado = mycursor.fetchall()
#                     print(f'resultado: {resultado}')
#                     return resultado
#
#                 except Exception as error:
#                     print('erro', error)
#                     return []
#
#                 finally:
#                     mycursor.close()
#                     print(CorFonte.fonte_amarela() + '-' * 150 + CorFonte.reset_cor())
#
#             for i in ordem_alocada:
#                 print(f'ordem_alocada (i): {i}')
#
#
#             estoque_alocado = teste(ordem_alocada)
#             # 1️⃣ transforma estoque_alocado em dicionário (EAN → qtde)
#             estoque_dict = dict(estoque_alocado)
#
#             # 2️⃣ cria nova lista com a coluna adicional
#             lista_itens_ordem_expandida = []
#
#             for item in lista_itens_ordem:
#                 print(f'dentro do for')
#                 ean = item[4]  # EAN está na posição 4
#                 estoque = estoque_dict.get(ean, 0.0)
#                 print(f'ean: {ean} | estoque: {estoque}')
#                 print(f'estoque livre: {item[10]}')
#
#                 # 3️⃣ cria nova tupla com a coluna extra no final
#                 if item[10] == 0:  # item[10] * estoque total
#                     add_total_alocado = item + (0.0,)
#                 else:
#
#                     add_total_alocado = item + (estoque,)
#                 print(f'add_total_alocado: {add_total_alocado}')
#
#                 lista_itens_ordem_expandida.append(add_total_alocado)
#                 print(f'lista_itens_ordem_extendida: {lista_itens_ordem_expandida}')
#             for i in lista_itens_ordem_expandida:
#                 print(f'lista_itens_ordem_expandida {i}')
#
#             # lista_itens_ordem_expandida (
#             # status           0>> 'ABERTO',
#             # item             1>> '1',
#             # codigo_produto   2>> '000002',
#             # descricao        3>> 'CHAVEIRO SOUVENIR',
#             # ean              4>> '7896020159300',
#             # un               5>> 'G',
#             # preco_lista      6>> '12.5',
#             # total_venda      7>> '12.5',
#             # quantidade       8>> '1',
#             # total_pedido'    9>> 12.5',
#             # estoque_livre    10>> 0.0,
#             # total_alocado    11>> 1.0)
#         if not ordem_alocada:
#             ordem_alocada = []
#         if not lista_itens_ordem_expandida:
#             lista_itens_ordem_expandida = []
#         return render_template(
#             'gestao_carteira/gestao_carteira.html',
#             estoque_total='',
#             lista_ordem_venda=lista_ordem_venda,
#             lista_itens_ordem_expandida=lista_itens_ordem_expandida,
#             form_gestao_carteira=form_gestao_carteira,
#             ordem_selecionada=ordem_selecionada,
#             ordem_alocada=ordem_alocada
#         )

def gestao_carteira():
    """
    Processamento de Gestão de Carteira com cálculo de estoque alocado e livre.
    LEGENDA DE CORES (Sugestão para o Front-end):
    - Verde: Atendida (Alocado == Pedido)
    - Amarelo: Parcial (0 < Alocado < Pedido)
    - Vermelho: Sem estoque (Alocado == 0)
    """
    print(CorFonte.fonte_amarela() + "Iniciando Processamento de Carteira" + CorFonte.reset_cor())

    form_gestao_carteira = ModGestaoCarteira.GestaoCarteira()

    # 1. ESTADO INICIAL (Carrega as OVs para a Tabela Superior)
    lista_ordem_venda = Buscadores.OrdemVenda.buscar_pedidos()

    # Recupera o estado da sessão (para manter dados ao marcar checkboxes)
    ordem_selecionada = session.get('ordem_selecionada')
    ordem_alocada_ids = session.get('ordem_alocada', [])

    lista_itens_ordem_expandida = []

    # 2. PROCESSAMENTO DO FORMULÁRIO (POST)
    if form_gestao_carteira.validate_on_submit():
        # Identifica qual OV foi selecionada para visualização (Radio)
        ordem_radio = request.form.get('ordem_venda')
        if ordem_radio:
            ordem_selecionada = int(ordem_radio)
            session['ordem_selecionada'] = ordem_selecionada

        # Identifica quais OVs foram marcadas para reserva de estoque (Checkbox)
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

    # 4. PROCESSAMENTO DOS ITENS DA ORDEM SELECIONADA (Tabela Inferior)
    if ordem_selecionada:
        # Busca os itens da ordem em foco
        itens_originais = Buscadores.OrdemVenda.buscar_itens(ordem_selecionada)

        for item in itens_originais:
            # MAPEAMENTO DAS COLUNAS (baseado no seu layout):
            # item[4]  -> EAN
            # item[8]  -> Quantidade Pedida nesta OV
            # item[10] -> Estoque Total Físico (vinda do banco/ERPs)

            ean = item[4]
            qtd_pedida = float(item[8])
            estoque_total_fisico = float(item[10])

            # Demanda total somada de todas as ordens que o usuário marcou
            demanda_marcada = demanda_total_por_ean.get(ean, 0.0)

            # LÓGICA DE ALOCAÇÃO:
            # Se a OV atual está marcada no checkbox, tentamos alocar a quantidade pedida
            if ordem_selecionada in ordem_alocada_ids:
                # O alocado não pode ser maior que o pedido nem maior que o estoque físico
                # Usamos a demanda_marcada para saber se o estoque físico suporta o grupo de OVs
                if estoque_total_fisico >= demanda_marcada:
                    alocado_nesta_ov = qtd_pedida
                else:
                    # Se o estoque não supre todas, alocamos o que resta proporcionalmente
                    # (Aqui simplificado: prioriza a exibição do saldo disponível)
                    folga = max(0, estoque_total_fisico)
                    alocado_nesta_ov = min(qtd_pedida, folga)
            else:
                alocado_nesta_ov = 0.0

            # CÁLCULO DO ESTOQUE LIVRE: (Estoque Total Físico - O que foi alocado para o grupo)
            # Reflete quanto sobraria no armazém se essas ordens fossem faturadas agora.
            qtde_estoque_livre = max(0, estoque_total_fisico - demanda_marcada)

            # 5. MONTAGEM DA TUPLA EXPANDIDA
            # Coluna 11: Estoque Alocado nesta OV
            # Coluna 12: Estoque Livre (Saldo do CD após as seleções)
            item_expandido = item + (alocado_nesta_ov, qtde_estoque_livre)
            lista_itens_ordem_expandida.append(item_expandido)
        print(f'lista_itens_ordem_expandida: {lista_itens_ordem_expandida}')
    return render_template(
        'gestao_carteira/gestao_carteira.html',
        lista_ordem_venda=lista_ordem_venda,
        lista_itens_ordem_expandida=lista_itens_ordem_expandida,
        form_gestao_carteira=form_gestao_carteira,
        ordem_selecionada=ordem_selecionada,
        ordem_alocada=ordem_alocada_ids
    )