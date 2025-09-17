import logging
import mysql.connector
from flask import render_template, redirect, url_for, request, session, flash
from oauthlib.uri_validate import query
from openpyxl.styles.builtins import total
from sqlalchemy.dialects.mysql import insert

import geral
import modulos.admin
from forms import ModComercial
from main import usuario
from modulos.compras import relatorio_compras
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
    2 CRIAR A TABELA 
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


def editar_ordem_venda():
    print(CorFonte.fonte_amarela() + "Função editar_ordem_venda"+ CorFonte.reset_cor())
    form_editar_ordem_venda = ModComercial.EditarOrdemVenda()
    ordem_venda = form_editar_ordem_venda.pesquisar_ordem_venda.data
    session["ordem_venda"] = ordem_venda
    if request.method == "POST":
        try:
            if "botao_pesquisar_ordem_venda" in request.form:
                ordem_venda = session.get("ordem_venda")
                print("botao_pesquisar_ordem_venda ACIONADO")
                print(f'ordem_venda: {ordem_venda}')
                # pesquisar ordem de venda
                def pesquisar_ordem_venda(ordem_venda):
                    query = f"SELECT * FROM ordem_venda where ordem_venda like '%{ordem_venda}%';"
                    print(f'query: {query}')
                    mydb.connect()
                    mycursor.execute(query)
                    resultado_pesquisa = mycursor.fetchall()
                    return resultado_pesquisa

                resultado_pesquisa = pesquisar_ordem_venda(ordem_venda)
                print(f'resultado_pesquisa: {resultado_pesquisa}')

        except Exception as e:
            logging.exception(e)

    return render_template('comercial/editar_ordem_venda.html',
                           data=Formatadores.os_data(),
                           ordem_venda='00001',
                           form_editar_ordem_venda=form_editar_ordem_venda)




def gestao_carteira():
    pass



def gerar_ordem_venda():

    print(CorFonte.fonte_amarela() + "Função gera_ordem_venda"+ CorFonte.reset_cor())
    data = Formatadores.os_data()
    form_gerar_ordem_venda = ModComercial.GerarOrdemVenda()
    total_pedido = 0
    # FIXME: AJUSTAR O TOTAL DA ORDEM DE VENDA PARA SEJA ZERADO AO ACESSAR A PAGINA


    if request.method == 'GET':
        for chave in [
            'lista_ordem_venda', 'tupla_linha_selecionada', 'item_selecionado',
            'linha_selecionada', 'lista_produtos', 'lista_linha_selecionada',
            'ean', 'descricao', 'unidade', 'tabela', 'preco_unitario']:
            session.pop(chave, None)

    if request.method == "POST":
        session['cliente'] = form_gerar_ordem_venda.cliente.data
        try:
            if "botao_pesquisar_item" in request.form:
                cliente = session.get('cliente')
                print("botao_pesquisar_item ACIONADO")
                pesquisa_descricao = form_gerar_ordem_venda.pesquisa_descricao.data
                pesquisa_categoria = form_gerar_ordem_venda.pesquisa_categoria.data
                pesquisa_ean = form_gerar_ordem_venda.pesquisa_ean.data
                print(f'pesq_descricao: {pesquisa_descricao} | pesquisa_categoria: {pesquisa_categoria} | pesquisa_ean: {pesquisa_ean}')
                lista_produtos = geral.Buscadores.OrdemVenda.buscar_lista_produtos(pesquisa_descricao, pesquisa_categoria, pesquisa_ean)
                fornecedor = lista_produtos[0][2]
                print(f'fornecedor: {fornecedor}')
                session['fornecedor'] = fornecedor
                session['lista_produtos'] = lista_produtos
                session['cliente'] = cliente
        except Exception as e:
            print(e)

        try:
            if 'botao_limpar_ordem' in request.form:
                print('botao_limpar_ordem ACIONADO')
                return redirect(url_for('gerar_ordem_venda'))
        except Exception as e:
            print(e)

        try:
            if 'botao_incluir_item' in request.form:
                total_pedido = session.get('total_pedido', 0)
                usuario = 'ADMIN'
                print('botao_incluir_item ACIONADO')
                lista_ordem_venda = session.get('lista_ordem_venda', [])
                tupla_linha_selecionada = session.get('tupla_linha_selecionada')
                fornecedor = session.get('fornecedor')
                cliente = session.get('cliente')
                print(f'cliente: {cliente}')
                lista_linha_selecionada = list(tupla_linha_selecionada)
                session['lista_linha_selecionada'] = lista_linha_selecionada
                quantidade = form_gerar_ordem_venda.quantidade.data
                print(f'quantidade: {quantidade}')
                preco = form_gerar_ordem_venda.preco_unitario.data
                preco_lista =  lista_linha_selecionada[5]

                total_item = quantidade * preco
                preco_venda = total_item/quantidade
                total_preco_lsta_teste = preco_lista * quantidade
                total_preco_venda_teste = preco_venda * quantidade
                print(f'total_preco_lsta_teste: {total_preco_lsta_teste}')
                print(f'total_preco_venda_teste: {total_preco_venda_teste}')
                desconto_acrescimo = (preco_venda * quantidade) - (preco_lista * quantidade)
                print(f'desconto_acrescimo: {desconto_acrescimo}')

                lista_linha_selecionada.append(fornecedor)
                lista_linha_selecionada.append(quantidade)
                lista_linha_selecionada.append(total_item)
                lista_linha_selecionada.append(usuario)
                lista_linha_selecionada.append(preco_venda)
                lista_linha_selecionada.append(desconto_acrescimo)
                total_pedido = total_pedido + total_item
                session['total_pedido'] = total_pedido

                print(f'lista_linha_selecionada: {lista_linha_selecionada}')

                def valida_linha_a_incluir_em_ordem_venda(lista_linha_selecionada, lista_ordem_venda):
                    # VALIDA SE A LINHA JÁ EXISTE NA ORDEM DE VENDA
                    if lista_linha_selecionada not in lista_ordem_venda:
                        print('lista disponivel')
                        print(f'lista_linha_selecionada: {lista_linha_selecionada}')
                        lista_ordem_venda.append(lista_linha_selecionada[:])
                        print(f'lista_ordem_venda: {lista_ordem_venda}')
                        session['lista_ordem_venda'] = lista_ordem_venda
                    else:
                        print('lista indisponivel')
                        print(f'lista_linha_selecionada: {lista_linha_selecionada}')
                valida_linha_a_incluir_em_ordem_venda(lista_linha_selecionada, lista_ordem_venda)

                def limpa_campos():
                    # ZERA CAMPOS APÓS ADICIONAR ITEM NA ORDEM DE VENDA
                    form_gerar_ordem_venda.preco_unitario.data = 0
                    form_gerar_ordem_venda.quantidade.data = 1
                    form_gerar_ordem_venda.ean.data = None
                    form_gerar_ordem_venda.descricao.data = None
                    form_gerar_ordem_venda.unidade.data = None
                    session['tupla_linha_selecionada'] = None
                limpa_campos()

                return  render_template('comercial/gerar_ordem_venda.html',

                                        form_gerar_ordem_venda=form_gerar_ordem_venda,
                                        data=Formatadores.formatar_data(Formatadores.os_data()))

        except Exception as e:
            print('Exceção no botao_incluir_item')
            print(e)

        try:
            if 'botao_selecionar_item' in request.form:
                total_pedido = session.get('total_pedido', 0)
                print('botao_selecionar_item ACIONADO')
                cliente = session.get('cliente')
                # TODO: ATUALIZAR FUNÇÃO AtualizaCodigo/ordem_venda PARA INCREMENTAR A ORDEM DE VENDA
                # TODO: PERSISTIR CAMPO FORNECEDOR AO CLCAR EM REMOVER LNHA
                print('A - Localiza o EAN selecionado na tabela de produtos')
                lista_produtos = session.get('lista_produtos')
                item_selecionado = request.form.get('botao_selecionar_item')
                # detectar numero da linha selecionada
                """
                    para obter o numero da linha selecionada, 
                    basta pegar o id do botão no html:
                    <input class="" type="hidden" name="incluir_item" value="{{i[3]}}">
                """

                print(f'1 - item_selecionado: {item_selecionado}')  # retorna o ean selecionado na lista
                session['item_selecionado'] = item_selecionado  # salva o ean selecionado na sessao
                cont = 0
                for i in lista_produtos: # lista com todos os produtos da tabela de opções
                    print(f'loop for i: {i[3]}-{item_selecionado} - cont: {cont}')
                    if i[3] == item_selecionado:  # verifica se o ean selecionado corresponde ao ean da linha
                        print(f'2 - item localizado: {i[3]}')
                        linha_selecionada = i
                        print(f'3 - linha_selecionada: {linha_selecionada}')
                        session['linha_selecionada'] = linha_selecionada
                        break
                    cont += 1
                linha_selecionada = session.get('linha_selecionada')  # recupera a linha selecionada do loop
                print(f'4 - linha_selecionada Recuperada: {linha_selecionada}')
                # todo: BAXAR O N DE ORDEM DO BANCO DE DADOD

                ordem_venda = '000001'
                session['ordem_venda'] = ordem_venda
                codigo_produto = linha_selecionada[1]
                ean = linha_selecionada[3]
                descricao = linha_selecionada[4]
                unidade = linha_selecionada[5]
                tabela = '001'
                preco_unitario = linha_selecionada[7]
                print(f'cliente recuperado: {cliente}')
                # fornecedor = linha_selecionada[2]
                tupla_linha_selecionada = (codigo_produto, ean, descricao, unidade , tabela, preco_unitario)
                tupla_linha_selecionada = (tupla_linha_selecionada + (ordem_venda,))
                print(f'5 - tupla_linha_selecionada>>.: {tupla_linha_selecionada}')
                session['tupla_linha_selecionada'] = tupla_linha_selecionada
                session['cliente'] = cliente

        except Exception as e:
            print('Erro no botao_selecionar_item')
            print(e)

        try:
            if "botao_remover_item" in request.form:
                print("botao_remover_item ACIONADO")
                busca_ean_excluir = request.form.get('botao_remover_item')
                print(f'item a excluir: {busca_ean_excluir} -  {type(busca_ean_excluir)}')
                cliente = session.get('cliente')
                cliente = form_gerar_ordem_venda.cliente.data
                print(f'cliente: {cliente}')
                lista_ordem_venda = session.get('lista_ordem_venda', [])  #

                contador = 0
                for i in lista_ordem_venda:
                    print(f'A lista_ordem_venda contém {len(lista_ordem_venda)} posições.')
                    print(f'posicao {contador}:{busca_ean_excluir} - {type(busca_ean_excluir)} | {i[1]} - {type(i[1])}')
                    if i[1] == busca_ean_excluir:
                        print(f'Ean {busca_ean_excluir} localizado na posicao {contador}')
                        del lista_ordem_venda[contador]
                        print(f'Nova lsta:\n {lista_ordem_venda}')
                    contador += 1

            # session['cliente'] = cliente
        except Exception as e:
            print(f"Erro ao processar remoção: {e}")

        try:
            if "botao_submit_ordem_venda" in request.form:
                usuario = session.get('usuario')
                print("botao_gerar_ordem Venda ACIONADO")
                cont_temp = 1
                lista_ordem_venda = session.get('lista_ordem_venda')
                print(f'lista_ordem_venda: {lista_ordem_venda}')
                while cont_temp <= len(lista_ordem_venda):
                    print(f'lista_ordem_venda: {lista_ordem_venda}')
                    for i in lista_ordem_venda:
                        # print('gerando ordem de venda')
                        # print(f'data: {data.strftime('%Y-%m-%d')}')
                        # print(f'ean: {i[1]}')
                        # print(f'descricao: {i[2]}')
                        # print(f'unidade: {i[3]}')
                        # print(f'tabela: {i[4]}')
                        # print(f'preco lista: {i[5]}')
                        # print(f'ordem_venda: {i[6]}')
                        # print(f'fornecedor: {i[7]}')
                        # print(f'quantidade: {i[8]}')
                        # print(f'preco_total_item: {i[9]}')
                        # print(f'preco_total_ordem: {i[10]}')
                        # print(f'preco_venda: {i[11]}')
                        # print(f'desconto|acrescimo: {i[12]}')
                        # print(f'usuario: {usuario}')
                        # print(f'status: {'ABERTO'}')
                        # print('---------------------------------------')
                        values_ordem_venda = (data.strftime('%Y-%m-%d'), i[6], cont_temp, i[0], i[7], i[2],i[1], i[3],i[4],i[5],i[11],i[8],i[12],i[9], 'ADMIN', 'ABERTO')
                        cont_temp += 1
                        mydb.connect()
                        query = (
                                f"INSERT INTO ORDEM_VENDA"
                                f"(DATA, "
                                f"ORDEM_VENDA, "
                                f"ITEM, "
                                f"CODIGO_PRODUTO, "
                                f"FORNECEDOR, "
                                f"DESCRICAO, "
                                f"EAN, "
                                f"UN, "
                                f"TABELA, "
                                f"PRECO_LISTA, "
                                f"PRECO_VENDA, "
                                f"QUANTIDADE, "
                                f"ACRESC_DESC, "
                                f"TOTAL_PEDIDO, "
                                f"USUARIO, STATUS_PEDIDO)"
                                f" VALUES {values_ordem_venda};")
                        print(values_ordem_venda)
                        print(f"Query {cont_temp} >>>> {query}")

                        mycursor.execute(query)
                        mycursor.fetchall()
                        fechadb = "SET SQL_SAFE_UPDATES = 1"
                        mycursor.execute(fechadb)
                        mycursor.fetchall()
                        mydb.commit()
                        mydb.close()
                        cont_temp += 1


        except Exception as e:
            print(f"Erro ao gerar ordem: {e}")
    ordem_venda = session.get('ordem_venda')
    tupla_linha_selecionada  = session.get('tupla_linha_selecionada')
    lista_produtos = session.get('lista_produtos')
    lista_ordem_venda = session.get('lista_ordem_venda')


    return render_template('comercial/gerar_ordem_venda.html',
                           ordem_venda=ordem_venda,
                           total_pedido=total_pedido,
                           relatorio_ordem_venda='',
                           form_gerar_ordem_venda=form_gerar_ordem_venda,
                           tupla_linha_selecionada=tupla_linha_selecionada,
                           codigo_ordem_venda='',
                           lista_produtos=lista_produtos,
                           lista_ordem_venda=lista_ordem_venda,
                           data=data)

def relatorio_ordem_venda():
    print(CorFonte.fonte_amarela() + "Função relatorio_ordem_venda"+ CorFonte.reset_cor())
    form_relatorio_vendas = ModComercial.RelatorioOrdemVenda()
    data_de = form_relatorio_vendas.data_de.data
    data_ate = form_relatorio_vendas.data_ate.data
    ordem_venda = form_relatorio_vendas.ordem_venda.data
    cliente = form_relatorio_vendas.cliente.data
    if request.method == "POST":
        try:
            if "botao_consulta" in request.form:
                print('Botao consulta Acionado')
                print(f'data_de: {data_de}')
                print(f'data_ate: {data_ate}')
                print(f'ordem_venda: {ordem_venda}')
                print(f'cliente: {cliente}')

                query = "SELECT * FROM ordem_venda where 1=1;"

                if data_de:
                    query += f" and data >= '{data_de}'"
                if data_ate:
                    query += f" and data <= '{data_ate}'"
                if ordem_venda:
                    query += f" and ordem_venda = '{ordem_venda}'"
                if cliente:
                    query += f" and codigo_cliente = '{cliente}'"

                mydb.connect()
                mycursor.execute(query)
                resultado_relatorio = mycursor.fetchall()  # pega os dados só aqui
                session['resultado_relatorio'] = resultado_relatorio
                mydb.close()  # fecha conexão

                print('-----------------------------------------------')
                print(f'query: {query}')

                for i in resultado_relatorio:
                    print(f'i : {i}')






        except Exception as e:
            print(f"Erro ao gerar ordem: {e}")
    resultado_relatorio = session.get('resultado_relatorio')
    return render_template('comercial/relatorio_ordem_venda.html',
                           form_relatorio_ordem_venda=form_relatorio_vendas,
                           data_de=data_de,
                           data_ate=data_ate,
                           ordem_venda=ordem_venda,
                           cliente=cliente,
                           resultado_relatorio_ordem_venda=resultado_relatorio)
