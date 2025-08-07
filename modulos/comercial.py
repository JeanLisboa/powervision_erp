import logging
import mysql.connector
from flask import render_template, redirect, url_for, request, session, flash

import geral
import modulos.admin
from forms import ModComercial
from modulos.utils.formatadores import Formatadores
from modulos.utils.atualizadores import AtualizaCodigo
from modulos.utils.buscadores import Buscadores
from modulos.utils.alertas import AlertaMsg
from modulos.utils.validadores import Validadores, ValidaStatusPedido
from modulos.utils.console import CorFonte

# inicialização de variáveis
mydb = mysql.connector.connect(host="localhost", user="admin2024", password="204619", database="projeto_erp")
mycursor = mydb.cursor()
logging.basicConfig(level=logging.INFO)


def cadastrar_clientes():
    print(CorFonte.fonte_amarela() + "Função cadastrar_clientes"+ CorFonte.reset_cor())
    data = Formatadores.os_data()
    usuario = "ADMIN"


    """
    # TODO: VERIFICAR O MELHOR CAMINHO.
    1 MANTER O CAMPO TABELA NA TABELA CLIENTE
    2 CRIAR A TABELA TABELA
    3  SELECIONAR A TABELA NO MOMENTO DE CADASTRAR CLIENTE

    1 RETIRAR O CAMPO TABELA DA TABELA CLIENTE
    2 CRIAR A TABELA TABELA
    3 CRIAR UM FORMULARIO PARA VINCULAR TABELA/CLIENTE
    """

    cod_cliente = AtualizaCodigo.cod_cliente()
    if not cod_cliente:
        cod_cliente = '00001'
    else:
        session["cod_cliente"] = cod_cliente
    print(f'cod_cliente: {cod_cliente}')
    form_cadastrar_clientes = ModComercial.CadastrarClientes()
    alert = None
    if request.method == 'POST':
        data = Formatadores.os_data()
        razao_social = form_cadastrar_clientes.razao_social.data
        cnpj = form_cadastrar_clientes.cnpj.data
        insc_estadual = form_cadastrar_clientes.insc_estadual.data
        email = form_cadastrar_clientes.email.data
        cep = form_cadastrar_clientes.cep.data
        telefone = form_cadastrar_clientes.telefone.data
        endereco =  form_cadastrar_clientes.endereco.data
        municipio = form_cadastrar_clientes.municipio.data
        uf = form_cadastrar_clientes.uf.data
        tabela = form_cadastrar_clientes.tabela.data
        tabela = '001'

        try:
            if 'botao_submit_cad_cliente' in request.form:
                print('botao ACIONADO')
                print(f'cod_cliente: {cod_cliente}',
                      f'razao_social: {razao_social}',
                      f'cnpj: {cnpj}',
                      f'insc_estadual: {insc_estadual}',
                      f'email: {email}',
                      f'cep: {cep}',
                      f'telefone: {telefone}',
                      f'endereco: {endereco}',
                      f'municipio: {municipio}',
                      f'uf: {uf} {len(uf)}')

                if Validadores.valida_cnpj(cnpj) is True and Buscadores.buscar_cnpj_cliente(cnpj) is False:
                    alert = AlertaMsg.cadastro_cliente_realizado()
                    try:
                        modulos.utils.buscadores.Comercial.cadastrar_cliente(data,cod_cliente,razao_social,cnpj,insc_estadual,email,cep,telefone,endereco,municipio,uf,tabela, usuario)
                        return redirect(url_for('cadastrar_clientes'))
                    except Exception as e:
                        alert = AlertaMsg.erro_ao_cadastrar_cliente(e)

                elif Validadores.valida_cnpj(cnpj) is False:
                    alert = AlertaMsg.cnpj_invalido()

                elif Buscadores.buscar_cnpj_cliente(cnpj) is True:
                    alert = AlertaMsg.cnpj_ja_existente()

        except Exception as e:
            logging.exception(e)

            # session["alert"] = {"tipo": "danger", "mensagem": f"Erro ao cadastrar cliente: {str(e)}"}

        alert = session.get("alert", None)

    # Sempre retorna o HTML, seja GET ou POST
    return render_template(
        'comercial/cadastrar_clientes.html',
        codigo=cod_cliente,
        alert=alert,
        data=Formatadores.formatar_data(data),
        form_cadastrar_clientes=form_cadastrar_clientes
    )

def gerar_ordem_venda():
    print(CorFonte.fonte_amarela() + "Função gera_ordem_venda"+ CorFonte.reset_cor())
    data = Formatadores.os_data()
    form_gerar_ordem_venda = ModComercial.GerarOrdemVenda()
    # TODO: CORRIGIR SELECTFIELD PARA ATUALIZAR SEM PRECISAR REINICIAR O APP
    if request.method == "POST":
        try:
            if "botao_pesquisar_cliente" in request.form:
                print("botao_pesquisar_cliente ACIONADO")
                cliente = form_gerar_ordem_venda.cliente.data
                print(f'cliente: {cliente}')
                session["cliente"] = cliente

        except:
            pass

        try:
            if "botao_pesquisar_item" in request.form:
                print("botao_pesquisar_item ACIONADO")
                pesquisa_descricao = form_gerar_ordem_venda.pesquisa_descricao.data
                pesquisa_categoria = form_gerar_ordem_venda.pesquisa_categoria.data
                pesquisa_ean = form_gerar_ordem_venda.pesquisa_ean.data
                print(f'pesquisa_descricao: {pesquisa_descricao}')
                print(f'pesquisa_categoria: {pesquisa_categoria}')
                print(f'pesquisa_ean: {pesquisa_ean}')

                # TODO: FUNCAO PARA PESQUISAR PRODUTO E RELACIONAR
                def pesquisa_item():
                    pass


                # TODO: ATUALIZAR FUNÇÃO AtualizaCodigo/ordem_venda PARA INCREMENTAR A ORDEM DE VENDA


                # TODO: CRIAR TABELA ORDEM DE VENDA
                # TODO: FUNCAO PARA RELACIONAR INFORMAÇÕES
                # TODO:

        except:
            pass

    return render_template('comercial/gerar_ordem_venda.html',
                           form_gerar_ordem_venda=form_gerar_ordem_venda,
                           codigo_ordem_venda='',
                           data=data)

