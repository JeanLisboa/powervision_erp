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

def gerar_ordem_venda():
    print(CorFonte.fonte_amarela() + "Função gera_ordem_venda"+ CorFonte.reset_cor())
    data = Formatadores.os_data()
    form_gerar_ordem_venda = ModComercial.GerarOrdemVenda()

    if request.method == 'GET':
        for chave in [
            'lista_ordem_venda', 'tupla_linha_selecionada', 'item_selecionado',
            'linha_selecionada', 'lista_produtos', 'lista_linha_selecionada',
            'ean', 'descricao', 'unidade', 'tabela', 'preco_unitario']:
            session.pop(chave, None)
    # TODO: CORRIGIR SELECTFIELD PARA ATUALIZAR SEM PRECISAR REINICIAR O APP
    if request.method == "POST":
        session['cliente'] = form_gerar_ordem_venda.cliente.data
        # try:
        #     if "botao_pesquisar_cliente" in request.form:
        #         print("botao_pesquisar_cliente ACIONADO")
        #         # cliente = form_gerar_ordem_venda.cliente.data
        #         # print(f'cliente: {cliente}')
        #         # session["cliente"] = cliente
        #
        # except Exception as e:
        #     print('Erro ao processar pesquisa de clientes')
        #     print(e)

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
            if 'botao_incluir_item' in request.form:
                lista_ordem_venda = session.get('lista_ordem_venda', [])
                tupla_linha_selecionada = session.get('tupla_linha_selecionada')
                fornecedor = session.get('fornecedor')
                print('botao_incluir_item ACIONADO')
                cliente = session.get('cliente')
                print(f'cliente: {cliente}')

                lista_linha_selecionada = list(tupla_linha_selecionada)
                session['lista_linha_selecionada'] = lista_linha_selecionada

                quantidade = form_gerar_ordem_venda.quantidade.data
                preco_unitario = form_gerar_ordem_venda.preco_unitario.data
                total_item = quantidade * preco_unitario

                lista_linha_selecionada.append(fornecedor)
                lista_linha_selecionada.append(quantidade)
                lista_linha_selecionada.append(total_item)

                if lista_linha_selecionada not in lista_ordem_venda:
                    print('lista disponivel')
                    print(f'lista_linha_selecionada: {lista_linha_selecionada}')
                    lista_ordem_venda.append(lista_linha_selecionada[:])
                    print(f'lista_ordem_venda: {lista_ordem_venda}')
                    session['lista_ordem_venda'] = lista_ordem_venda

                else:
                    print('lista indisponivel')

        except Exception as e:
            print('Exceção no botao_incluir_item')
            print(e)

        try:
            if 'botao_selecionar_item' in request.form:
                print('botao_selecionar_item ACIONADO')
                cliente = session.get('cliente')
                # TODO: ATUALIZAR FUNÇÃO AtualizaCodigo/ordem_venda PARA INCREMENTAR A ORDEM DE VENDA
                #
                # TODO: PERSISTIR CAMPO FORNECEDOR AO CLCAR EM REMOVER LNHA
                # TODO: DESABiLiTAR CAMPO PESQUSAR CLiENTE APÓS PRMERA LNHA CADASTRADA
                # FIXME: LIMPAR CAMPOS APÓS INCLUIR SELECIONAR O PRODUTO
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
                        break  # interrompe o loop
                    cont += 1

                linha_selecionada = session.get('linha_selecionada')  # recupera a linha selecionada do loop
                print(f'4 - linha_selecionada Recuperada: {linha_selecionada}')
                ordem_venda = '000001'
                session['ordem_venda'] = ordem_venda
                codigo_produto = linha_selecionada[1]
                ean = linha_selecionada[3]
                descricao = linha_selecionada[4]
                unidade = linha_selecionada[5]
                tabela = '001'
                preco_unitario = linha_selecionada[7]
                print(f'cliente recuperado: {cliente}')
                fornecedor = linha_selecionada[2]
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


    ordem_venda = session.get('ordem_venda')
    tupla_linha_selecionada  = session.get('tupla_linha_selecionada')
    # print(f'tupla_linha_selecionada: {tupla_linha_selecionada}')
    lista_produtos = session.get('lista_produtos')
    # print(f'lista_produtos: {lista_produtos}')
    linha_selecionada = session.get('linha_selecionada')
    lista_ordem_venda = session.get('lista_ordem_venda')
    cliente = session.get('cliente')
    return render_template('comercial/gerar_ordem_venda.html',
                           ordem_venda=ordem_venda,
                           cliente=cliente,
                           form_gerar_ordem_venda=form_gerar_ordem_venda,
                           tupla_linha_selecionada=tupla_linha_selecionada,
                           codigo_ordem_venda='',
                           lista_produtos=lista_produtos,
                           lista_ordem_venda=lista_ordem_venda,
                           data=data)
