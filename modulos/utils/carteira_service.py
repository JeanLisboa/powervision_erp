from config.db import mydb



def buscar_pedidos_resumo():
    sql = """
        SELECT
            ov.ordem_venda,
            ov.data,
            ov.cod_cliente,
            c.nome AS cliente,
            ov.processar,
            SUM(i.quantidade * i.preco_venda) AS total_pedido,
            ov.status_estoque
        FROM ordem_venda ov
        JOIN cliente c ON c.cod_cliente = ov.cod_cliente
        JOIN ordem_venda_item i ON i.ordem_venda = ov.ordem_venda
        GROUP BY
            ov.ordem_venda,
            ov.data,
            ov.cod_cliente,
            c.nome,
            ov.processar,
            ov.status_estoque
        ORDER BY ov.data DESC
    """

    conn = mydb()
    cur = conn.cursor(dictionary=True)
    cur.execute(sql)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return rows


def buscar_itens_pedido(ordem_venda):
    sql = """
        SELECT
            i.item,
            i.cod_produto,
            p.descricao,
            p.ean,
            p.unidade,
            i.preco_custo,
            i.preco_venda,
            (i.quantidade * i.preco_venda) AS total_produto,
            i.status_estoque
        FROM ordem_venda_item i
        JOIN produto p ON p.cod_produto = i.cod_produto
        WHERE i.ordem_venda = %s
        ORDER BY i.item
    """

    conn = mydb()
    cur = conn.cursor(dictionary=True)
    cur.execute(sql, (ordem_venda,))
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return rows
