import logging
import mysql.connector
from flask import render_template, redirect, url_for, request, session, flash

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
    logging.info(CorFonte.fonte_amarela() + "Função cadastrar_clientes"+ CorFonte.reset_cor())
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
    logging.info(f'cod_cliente: {cod_cliente}')
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
        cliente = form_cadastrar_clientes.cliente.data
        tabela = '001'

        try:
            if 'botao_submit_cad_cliente' in request.form:
                logging.info('botao ACIONADO')
                logging.info(f'cod_cliente: {cod_cliente}',
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
    resultado_pesquisa = session.get("resultado_pesquisa", None)
    if request.method == "POST":
        if ordem_venda :
            try:
                if "botao_pesquisar_ordem_venda" in request.form:
                    ordem_venda = session.get("ordem_venda")
                    logging.info("botao_pesquisar_ordem_venda ACIONADO")
                    logging.info(f'ordem_venda: {ordem_venda}')
                    session["ordem_venda_pesquisada"] = ordem_venda
                    # pesquisar ordem de venda

                    def pesquisar_ordem_venda(ordem_venda: str):
                        print(CorFonte.fonte_amarela() + 'função editar_ordem_venda | pesquisar_ordem_venda' + CorFonte.reset_cor())

                        query = "SELECT * FROM ordem_venda WHERE ordem_venda LIKE %s;"
                        logging.info(f'query (parametrizada): {query}, valor: %{ordem_venda}%')
                        try:
                            mydb.connect()
                            mycursor = mydb.cursor()
                            # executa query de forma segura
                            mycursor.execute(query, (f"%{ordem_venda}%",))
                            resultado_pesquisa = mycursor.fetchall()
                            return resultado_pesquisa

                        except Exception as e:
                            logging.error(f"Erro ao pesquisar ordem_venda: {e}")
                            return []

                        finally:
                            mydb.close()

                    cliente = session.get('cliente')
                    resultado_pesquisa = pesquisar_ordem_venda(ordem_venda)
                    temp = []  # lista temporaria para armazenar os resultados
                    for i in resultado_pesquisa:
                        i = i + cliente
                        temp.append(i)
                        print(temp)
                    print(f'----------------------------------------------')
                    resultado_pesquisa = temp
                    session["resultado_pesquisa"] = resultado_pesquisa
                    logging.info(f'resultado_pesquisa: {resultado_pesquisa}')
                    ordem_venda = session.get("ordem_venda")
                    print(f'teste ordem venda na pesquisa: {ordem_venda}')
                    return render_template('comercial/editar_ordem_venda.html',
                                           data=Formatadores.os_data(),
                                           ordem_venda=ordem_venda,
                                           resultado_pesquisa=resultado_pesquisa,
                                           form_editar_ordem_venda=form_editar_ordem_venda)

            except Exception as e:
                logging.exception(e)
                resultado_pesquisa = session.get("resultado_pesquisa")
                return render_template('comercial/editar_ordem_venda.html',

                                       form_editar_ordem_venda=form_editar_ordem_venda,
                                       resultado_pesquisa=resultado_pesquisa)

        else:
            print(CorFonte.fonte_amarela() + "Nenhuma ordem de venda pesquisada" + CorFonte.reset_cor())
        # todo: ajustar frontend da tabela para nao passar por detras do titulo
        try:
            if "botao_editar_item" in request.form:
                print(CorFonte.fonte_amarela() + "Função editar_ordem_venda | botao_editar_item" + CorFonte.reset_cor())
                ordem_venda_pesquisada = session.get("ordem_venda_pesquisada")
                resultado_pesquisa = session.get("resultado_pesquisa")
                print(f'resultado_pesquisa: {resultado_pesquisa}')
                print(f'ordem_venda_pesquisada: {ordem_venda_pesquisada} ')
                logging.info("botao_editar_item acionado")
                item_selecionado = request.form.getlist("editar__item")[0]
                print(f'item_selecionado: {item_selecionado}')

                linha_para_editar = [i for i in resultado_pesquisa if str(i[6]) == str(item_selecionado)]

                print(f'linha_para_editar: {linha_para_editar[0]}')
                # configuração do formulario para editar ytem da ordem de venda
                if linha_para_editar:
                    session["linha_para_editar"] = linha_para_editar

                    ean = ''
                    form_editar_ordem_venda.ean.data = ean
                    session["ean"] = ean

                    quantidade = linha_para_editar[0][11]  # validar posicao
                    form_editar_ordem_venda.quantidade.data = quantidade
                    session["quantidade"] = quantidade

                    descricao = linha_para_editar[0][5]
                    form_editar_ordem_venda.descricao.data = descricao
                    session["descricao"] = descricao

                    val_unitario = linha_para_editar[0][10]
                    form_editar_ordem_venda.val_unitario = val_unitario
                    session["val_unitario"] = val_unitario

                    logging.info(f'linha_para_editar: {linha_para_editar}')
                else:
                    logging.warning("Nenhuma linha encontrada para o item selecionado.")

                ordem_venda = session.get("ordem_venda_pesquisada")
                print(f'teste ordem_venda {ordem_venda}')
                quantidade= session.get('quantidade')
                descricao= session.get('descricao')
                val_unitario= session.get('val_unitario')
                ean= session.get('ean')
                cliente= session.get('cliente')


                return render_template('comercial/editar_ordem_venda.html',
                                       ordem_venda=ordem_venda,
                                       form_editar_ordem_venda=form_editar_ordem_venda,
                                       ean=ean,
                                       cliente=cliente,
                                       quantidade=quantidade,
                                       descricao=descricao,
                                       val_unitario=val_unitario,
                                       data=Formatadores.os_data(),
                                       resultado_pesquisa=resultado_pesquisa,
                                       linha_para_editar=linha_para_editar)


        except Exception as e:
            print('ver erro')
            logging.exception(e)


        try:
            if "botao_salvar_item_adicionado" in request.form:
                print(CorFonte.fonte_amarela() + "Função editar_ordem_venda | botao_salvar_item_adicionado" + CorFonte.reset_cor())
                linha_para_editar = session.get("linha_para_editar")
                resultado_pesquisa = session.get('resultado_pesquisa')
                # recuperar informação dos campos do formulario
                nova_quantidade = form_editar_ordem_venda.adicionar_quantidade.data
                novo_preco_unitario = form_editar_ordem_venda.adicionar_preco_unitario.data
                print(f'nova_quantidade: {nova_quantidade}')
                print(f'novo_preco_unitario: {novo_preco_unitario}')
                print(f'linha_para_editar: {linha_para_editar}')
                def alterar_item(nova_quantidade, novo_preco_unitario, linha_para_editar):
                    preco_lista = linha_para_editar[0][9]
                    preco_venda = novo_preco_unitario
                    acres_desc = (preco_venda * nova_quantidade) - (preco_lista * nova_quantidade)
                    print(CorFonte.fonte_amarela() + "Função editar_ordem_venda | botao_salvar_item_adicionado | função alterar_item" + CorFonte.reset_cor())
                    query = (
                        f"UPDATE ORDEM_VENDA\n"
                        f"SET\n "
                        f"QUANTIDADE = '{nova_quantidade}',\n"
                        f"PRECO_VENDA = '{novo_preco_unitario}',\n"
                        f"ACRESC_DESC = '{acres_desc}',\n"
                        f"TOTAL_PEDIDO = '{nova_quantidade*novo_preco_unitario}',\n"
                        
                        f"WHERE EAN = '{linha_para_editar[0][6]}'\n "
                        f"and ORDEM_COMPRA = '{linha_para_editar[0][1]}';"
                    )
                    print(f"query {query}")
                    #
                    # mydb.connect()
                    # mycursor.execute(query)
                    # mycursor.fetchall()
                    # mydb.commit()
                    # mydb.close()

                alterar_item(nova_quantidade, novo_preco_unitario, linha_para_editar)

                # se as informações forem iguais, alert nada a alterar
                return render_template('comercial/editar_ordem_venda.html',
                                       data=Formatadores.os_data(),
                                       resultado_pesquisa=resultado_pesquisa,
                                       form_editar_ordem_venda=form_editar_ordem_venda)




        except Exception as e:
            logging.exception(e)





    resultado_pesquisa = session.get("resultado_pesquisa", None)
    return render_template('comercial/editar_ordem_venda.html',
                           data=Formatadores.os_data(),
                           form_editar_ordem_venda=form_editar_ordem_venda)


def gestao_carteira():
    pass


def gerar_ordem_venda():

    """
    funcionamento esperado ao acessar a tela Gerar Ordem de Venda:
    - carregar:
     - numero da ordem de venda
     - data
     - clientes cadastrados


    :return:
    """
    # fixme: ao carregar a tela inicial, apenas as funções iniciais devem ser executadas
    logging.info(CorFonte.fonte_amarela() + "Função gera_ordem_venda"+ CorFonte.reset_cor())

    form_gerar_ordem_venda = ModComercial.GerarOrdemVenda()
    # Se ainda não tem cliente na sessão, define agora
    if 'cliente' not in session or not session['cliente']:
        if form_gerar_ordem_venda.cliente.data:
            session['cliente'] = form_gerar_ordem_venda.cliente.data

    if request.method == "GET":
        # Zera o total do pedido e limpa a sessão
        session["total_pedido"] = 0
        total_pedido = 0
        logging.info("Total pedido zerado ao acessar a página.")
        for chave in [
            'lista_ordem_venda',
            'tupla_linha_selecionada',
            'item_selecionado',
            'linha_selecionada',
            'lista_produtos',
            'lista_linha_selecionada',
            'ean',
            'descricao',
            'unidade',
            'tabela',
            'preco_unitario']:
            session.pop(chave, None)

    else:
        total_pedido = session.get("total_pedido", 0)


    def busca_n_ordem_venda():
        logging.info(CorFonte.fonte_amarela() + "Função gera_ordem_venda | busca_n_ordem_venda" + CorFonte.reset_cor())
        mydb.connect()
        mycursor.execute('select max(ordem_venda) FROM ORDEM_VENDA;')
        ordem_venda = mycursor.fetchall()
        # logging.info(f'ordem_venda: {ordem_venda[0][0]} - {type(ordem_venda)}')
        ordem_venda =int(ordem_venda[0][0])
        # logging.info(f'ordem_venda: {ordem_venda} - {type(ordem_venda)}')
        ordem_venda += 1
        mycursor.fetchall()
        fechadb = "SET SQL_SAFE_UPDATES = 1"
        mycursor.execute(fechadb)
        mycursor.fetchall()
        mydb.commit()
        mydb.close()

        def completa_zeros(numero: str, tamanho: int = 6) -> str:
            logging.info(CorFonte.fonte_amarela() + "Função gera_ordem_venda | completa_zeros" + CorFonte.reset_cor())
            return numero.zfill(tamanho)
        ordem_venda = completa_zeros(str(ordem_venda))
        return ordem_venda

    ordem_venda = busca_n_ordem_venda()
    session['ordem_venda'] = ordem_venda

    data = Formatadores.os_data()

    if request.method == 'GET':
        for chave in [
            'lista_ordem_venda', 'tupla_linha_selecionada', 'item_selecionado',
            'linha_selecionada', 'lista_produtos', 'lista_linha_selecionada',
            'ean', 'descricao', 'unidade', 'tabela', 'preco_unitario']:
            session.pop(chave, None)

    if request.method == "POST":
        try:
            if "botao_pesquisar_item" in request.form:
                cliente = session.get('cliente')
                logging.info("botao_pesquisar_item ACIONADO")
                pesquisa_descricao = form_gerar_ordem_venda.pesquisa_descricao.data
                pesquisa_categoria = form_gerar_ordem_venda.pesquisa_categoria.data
                pesquisa_ean = form_gerar_ordem_venda.pesquisa_ean.data
                # logging.info(f'pesq_descricao: {pesquisa_descricao} | pesquisa_categoria: {pesquisa_categoria} | pesquisa_ean: {pesquisa_ean}')
                lista_produtos = geral.Buscadores.OrdemVenda.buscar_lista_produtos(pesquisa_descricao, pesquisa_categoria, pesquisa_ean)

                fornecedor = lista_produtos[0][2]
                # logging.info(f'fornecedor: {fornecedor}')
                session['fornecedor'] = fornecedor
                session['lista_produtos'] = lista_produtos
                session['cliente'] = cliente
                return render_template('gerar_ordem_venda.html',
                                       ordem_venda=ordem_venda,
                                       total_pedido=total_pedido,
                                       relatorio_ordem_venda='',
                                       form_gerar_ordem_venda=form_gerar_ordem_venda,
                                       codigo_ordem_venda='',
                                       lista_produtos=lista_produtos,
                                       data=data)
        except Exception as e:
            logging.info(e)

        try:
            if 'botao_limpar_ordem' in request.form:
                logging.info('botao_limpar_ordem ACIONADO')
                return redirect(url_for('gerar_ordem_venda'))
        except Exception as e:
            logging.info(e)

        try:
            if 'botao_incluir_item' in request.form:
                # FIXME: AJUSTAR INFORMAÇÃO DO TOTAL DO PEDIDO PARA QUE NAO SEJA ATUALIZADO QUANDO O ITEM NÃO FOR INSERIDO NA TABELA
                total_pedido = session.get('total_pedido', 0)
                usuario = 'ADMIN'
                logging.info('botao_incluir_item ACIONADO')
                lista_ordem_venda = session.get('lista_ordem_venda', [])
                tupla_linha_selecionada = session.get('tupla_linha_selecionada')
                cliente = form_gerar_ordem_venda.cliente.data or session.get('cliente')
                fornecedor = session.get('fornecedor')
                logging.info(f'cliente: {cliente}')
                lista_linha_selecionada = list(tupla_linha_selecionada)
                session['lista_linha_selecionada'] = lista_linha_selecionada
                quantidade = form_gerar_ordem_venda.quantidade.data
                # logging.info(f'quantidade: {quantidade}')
                preco = form_gerar_ordem_venda.preco_unitario.data
                preco_lista =  lista_linha_selecionada[5]
                total_item = quantidade * preco
                preco_venda = total_item/quantidade
                total_preco_lsta_teste = preco_lista * quantidade
                total_preco_venda_teste = preco_venda * quantidade
                # logging.info(f'total_preco_lsta_teste: {total_preco_lsta_teste}')
                # logging.info(f'total_preco_venda_teste: {total_preco_venda_teste}')
                desconto_acrescimo = (preco_venda * quantidade) - (preco_lista * quantidade)
                # logging.info(f'desconto_acrescimo: {desconto_acrescimo}')

                lista_linha_selecionada.append(fornecedor)
                lista_linha_selecionada.append(quantidade)
                lista_linha_selecionada.append(total_item)
                lista_linha_selecionada.append(usuario)
                lista_linha_selecionada.append(preco_venda)
                lista_linha_selecionada.append(desconto_acrescimo)
                lista_linha_selecionada.append(cliente[0]) # COD CLIENTE
                lista_linha_selecionada.append(cliente[1]) # NOME FANTASIA
                session['cliente'] = cliente
                total_pedido = total_pedido + total_item
                session['total_pedido'] = total_pedido

                print(f'lista_linha_selecionada: {lista_linha_selecionada}')

                def valida_linha_a_incluir_em_ordem_venda(lista_linha_selecionada, lista_ordem_venda):
                    # VALIDA SE A LINHA JÁ EXISTE NA ORDEM DE VENDA
                    cliente = session.get('cliente')
                    if lista_linha_selecionada not in lista_ordem_venda:
                        logging.info('lista disponivel')
                        print(f'cliente: {cliente}')
                        # logging.info(f'lista_linha_selecionada: {lista_linha_selecionada}')
                        lista_ordem_venda.append(lista_linha_selecionada[:])
                        logging.info(f'lista_ordem_venda: {lista_ordem_venda}')
                        session['lista_ordem_venda'] = lista_ordem_venda
                    else:
                        logging.info('lista indisponivel')
                        logging.info(f'lista_linha_selecionada: {lista_linha_selecionada}')
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
        except Exception as e:
            logging.info('Exceção no botao_incluir_item')
            logging.info(e)

        try:
            if 'botao_selecionar_item' in request.form:
                # total_pedido = session.get('total_pedido', 0)
                # logging.info('botao_selecionar_item ACIONADO')
                cliente = session.get('cliente')
                # TODO: PERSISTIR CAMPO FORNECEDOR AO CLiCAR EM REMOVER LNHA
                # logging.info('A - Localiza o EAN selecionado na tabela de produtos')
                lista_produtos = session.get('lista_produtos')
                item_selecionado = request.form.get('botao_selecionar_item')
                # detectar numero da linha selecionada
                """
                    para obter o numero da linha selecionada, 
                    basta pegar o id do botão no html:
                    <input class="" type="hidden" name="incluir_item" value="{{i[3]}}">
                """

                # logging.info(f'1 - item_selecionado: {item_selecionado}')  # retorna o ean selecionado na lista
                session['item_selecionado'] = item_selecionado  # salva o ean selecionado na sessao
                cont = 0
                for i in lista_produtos: # lista com todos os produtos da tabela de opções
                    # logging.info(f'loop for i: {i[3]}-{item_selecionado} - cont: {cont}')
                    if i[3] == item_selecionado:  # verifica se o ean selecionado corresponde ao ean da linha
                        # logging.info(f'2 - item localizado: {i[3]}')
                        linha_selecionada = i
                        # logging.info(f'3 - linha_selecionada: {linha_selecionada}')
                        session['linha_selecionada'] = linha_selecionada
                        break
                    cont += 1
                linha_selecionada = session.get('linha_selecionada')  # recupera a linha selecionada do loop
                # logging.info(f'4 - linha_selecionada Recuperada: {linha_selecionada}')
                # todo: BAXAR O N DE ORDEM DO BANCO DE DADOD

                ordem_venda = session.get('ordem_venda')
                codigo_produto = linha_selecionada[1]
                ean = linha_selecionada[3]
                descricao = linha_selecionada[4]
                unidade = linha_selecionada[5]
                tabela = '001'
                preco_unitario = linha_selecionada[7]
                logging.info(f'cliente recuperado: {cliente}')
                # fornecedor = linha_selecionada[2]
                tupla_linha_selecionada = (codigo_produto, ean, descricao, unidade , tabela, preco_unitario)
                tupla_linha_selecionada = (tupla_linha_selecionada + (ordem_venda,))
                # logging.info(f'5 - tupla_linha_selecionada>>.: {tupla_linha_selecionada}')
                session['tupla_linha_selecionada'] = tupla_linha_selecionada
                session['cliente'] = cliente
                return render_template('gerar_ordem_venda.html',
                                       ordem_venda=ordem_venda,
                                       cliente=cliente,
                                       total_pedido=total_pedido,
                                       relatorio_ordem_venda='',
                                       form_gerar_ordem_venda=form_gerar_ordem_venda,
                                       tupla_linha_selecionada=tupla_linha_selecionada,
                                       codigo_ordem_venda='',
                                       lista_produtos=lista_produtos,
                                       lista_ordem_venda=lista_ordem_venda,
                                       data=data)
        except Exception as e:
            logging.info('Erro no botao_selecionar_item')
            logging.info(e)

        try:
            if "botao_remover_item" in request.form:
                logging.info("botao_remover_item ACIONADO")
                busca_ean_excluir = request.form.get('botao_remover_item')
                logging.info(f'item a excluir: {busca_ean_excluir} -  {type(busca_ean_excluir)}')
                cliente = session.get('cliente')
                cliente = form_gerar_ordem_venda.cliente.data
                logging.info(f'cliente: {cliente}')
                lista_ordem_venda = session.get('lista_ordem_venda', [])  #

                contador = 0
                for i in lista_ordem_venda:
                    logging.info(f'A lista_ordem_venda contém {len(lista_ordem_venda)} posições.')
                    logging.info(f'posicao {contador}:{busca_ean_excluir} - {type(busca_ean_excluir)} | {i[1]} - {type(i[1])}')
                    if i[1] == busca_ean_excluir:
                        logging.info(f'Ean {busca_ean_excluir} localizado na posicao {contador}')
                        del lista_ordem_venda[contador]
                        logging.info(f'Nova lsta:\n {lista_ordem_venda}')
                    contador += 1


            # session['cliente'] = cliente
        except Exception as e:
            logging.info(f"Erro ao processar remoção: {e}")

        try:
            if "botao_submit_ordem_venda" in request.form:
                usuario = session.get('usuario')
                cliente = session.get('cliente')
                logging.info("botao_gerar_ordem Venda ACIONADO")
                cont_temp = 1
                lista_ordem_venda = session.get('lista_ordem_venda')
                logging.info(f'lista_ordem_venda: {lista_ordem_venda}')
                while cont_temp <= len(lista_ordem_venda):
                    # logging.info(f'lista_ordem_venda: {lista_ordem_venda}')
                    for i in lista_ordem_venda:
                        values_ordem_venda = (data.strftime('%Y-%m-%d'), i[6], cont_temp, i[0], i[7], i[2],i[1], i[3],i[4],i[5],i[11],i[8],i[12],i[9], 'ADMIN', 'ABERTO', i[13], i[14])
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
                                f"USUARIO, "
                                f"STATUS_PEDIDO, "
                                f"COD_CLIENTE,"
                                f"CLIENTE)"
                                f" VALUES {values_ordem_venda};")
                        logging.info(values_ordem_venda)
                        # input('>>>>>>>>>>>>>>>>>>>>>>>>>>>> VALIDE A QUERY')
                        logging.info(f"Query {cont_temp} >>>> {query}")
                        mycursor.execute(query)
                        mycursor.fetchall()
                        fechadb = "SET SQL_SAFE_UPDATES = 1"
                        mycursor.execute(fechadb)
                        mycursor.fetchall()
                        mydb.commit()
                        mydb.close()
                        cont_temp += 1

                        tupla_linha_selecionada = ()
                        session['tupla_linha_selecionada'] = tupla_linha_selecionada
                        lista_produtos = []
                        session['lista_produtos'] = lista_produtos
                        lista_ordem_venda = []
                        session['lista_ordem_venda'] = lista_ordem_venda

                return redirect(url_for('gerar_ordem_venda'))
            tupla_linha_selecionada = session.get('tupla_linha_selecionada', [])
            lista_ordem_venda = session.get('lista_ordem_venda', [])
            lista_produtos = session.get('lista_produtos', [])

            return render_template('comercial/gerar_ordem_venda.html',
                                   ordem_venda=busca_n_ordem_venda(),
                                   lista_ordem_venda=lista_ordem_venda,
                                   tupla_linha_selecionada=tupla_linha_selecionada,
                                   lista_produtos=lista_produtos,
                                   total_pedido=total_pedido)

        except Exception as e:
            logging.info(f"Erro ao gerar ordem: {e}")

    ordem_venda = session.get('ordem_venda')
    tupla_linha_selecionada  = session.get('tupla_linha_selecionada')
    lista_produtos = session.get('lista_produtos')
    lista_ordem_venda = session.get('lista_ordem_venda')


    return render_template('comercial/gerar_ordem_venda.html',
                           ordem_venda=busca_n_ordem_venda(),

                           total_pedido=total_pedido,
                           relatorio_ordem_venda='',
                           form_gerar_ordem_venda=form_gerar_ordem_venda,
                           tupla_linha_selecionada=tupla_linha_selecionada,
                           codigo_ordem_venda='',
                           lista_produtos=lista_produtos,
                           lista_ordem_venda=lista_ordem_venda,
                           data=data)


def relatorio_ordem_venda():
    logging.info(CorFonte.fonte_amarela() + "Função relatorio_ordem_venda"+ CorFonte.reset_cor())
    form_relatorio_vendas = ModComercial.RelatorioOrdemVenda()
    data_de = form_relatorio_vendas.data_de.data
    data_ate = form_relatorio_vendas.data_ate.data
    ordem_venda = form_relatorio_vendas.ordem_venda.data
    cliente = form_relatorio_vendas.cliente.data
    if request.method == "POST":
        try:
            if "botao_consulta" in request.form:
                logging.info('Botao consulta Acionado')
                logging.info(f'data_de: {data_de}')
                logging.info(f'data_ate: {data_ate}')
                logging.info(f'ordem_venda: {ordem_venda}')
                logging.info(f'cliente: {cliente}')
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
                for i in resultado_relatorio:
                    logging.info(f'i : {i}')


        except Exception as e:
            logging.info(f"Erro ao gerar ordem: {e}")
    resultado_relatorio = session.get('resultado_relatorio')
    return render_template('comercial/relatorio_ordem_venda.html',
                           form_relatorio_ordem_venda=form_relatorio_vendas,
                           data_de=data_de,
                           data_ate=data_ate,
                           ordem_venda=ordem_venda,
                           cliente=cliente,
                           resultado_relatorio_ordem_venda=resultado_relatorio)
