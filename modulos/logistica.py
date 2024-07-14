# INTERNALIZAR PRODUTO COMPRADO PELO SETOR DE COMPRAS (ENTRADA)
# SEPARAR PEDIDO DE VENDA
# DAR SAÍDA NOS PEDIDOS DE VENDA (SAÍDA)
# ENVIA PEDIDO AO CLIENTE
# CADASTRAR TRANSPORTADOR
from flask import render_template
from forms import Mod_Logistica
from geral import Formatadores


def entrada_ordem_compra():
    form_entrada_ordem_compra = Mod_Logistica.EntradaOrdemCompra()
    nome_fantasia = form_entrada_ordem_compra.nome_fantasia.data
    ordem_compra = form_entrada_ordem_compra.ordem_compra.data

    return render_template('logistica/entrada_ordem_compra.html',
                           form_entrada_ordem_compra=form_entrada_ordem_compra,
                           nome_fantasia=nome_fantasia,
                           ordem_compra=ordem_compra,
                           data=Formatadores.formatar_data(Formatadores.os_data()))


def pedidos_pendentes():
    form_entrada_ordem_compra = Mod_Logistica.EntradaOrdemCompra()
    nome_fantasia = form_entrada_ordem_compra.nome_fantasia.data
    ordem_compra = form_entrada_ordem_compra.ordem_compra.data

    return render_template('logistica/pedidos_pendentes.html',
                           form_entrada_ordem_compra=form_entrada_ordem_compra,
                           nome_fantasia=nome_fantasia,
                           ordem_compra=ordem_compra,
                           data=Formatadores.formatar_data(Formatadores.os_data()))
