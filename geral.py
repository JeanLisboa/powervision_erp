pasta_xml = r"C:\relato\XML\ANTIGOS" # utilizado pelo modulo logistica / entrada de ordem compra
import mysql.connector
from pandas.io.formats.info import series_see_also_sub
from pycpfcnpj import cpfcnpj as validador_cnpj
from flask import session, redirect, url_for, request
import xml.etree.ElementTree as ET
import openpyxl
import os
from datetime import date

# utils ok
pasta_xml = r"C:\relato\XML\ANTIGOS" # utilizado pelo modulo logistica / entrada de ordem compra
"""
class CorFonte: edita as cores dos logs no terminal
class AlertaMsg: edita as mensagens de alerta
class Formatadores: formata e retorna dados para os modulos, ex. data, cnpj, cep
class ValidaStatusPedido: classe especifica do modulo entrada de ordem_compra
class Buscadores: consultas a banco de dados para todos os modulos
class Validadores: validacoes diversas, cnpj, cpf,  etc
class BancoDeDados: no momento, sem uso
class Estoque: atualiza saldo ordem_compra e relatorio estoque

"""
#  utils ok
class CorFonte:
    """
        # configura cor de fonte no terminal
        # 38;2 especifica que o rgb será aplicado à cor da fonte e ';2' especifica que será aplicado a cor pelo rgb
        # 48;2 especifica que o rgb será aplicado à cor ao background e ';2' especifica que será aplicado a cor pelo rgb

    """
    @staticmethod
    def fonte_vermelha():
        return "\033[38;2;255;0;0;48;2;0;0;0m"  # erro

    @staticmethod
    def fonte_verde():  #
        return "\033[92m"

    @staticmethod
    def fonte_amarela():  # interação do usuário
        return "\033[93m"

    @staticmethod
    def fonte_azul():
        return "\033[34m"

    @staticmethod
    def fonte_azul_claro():  # acionamento de função
        return "\033[36m"

    @staticmethod
    def reset_cor():
        return "\033[0m"

#  utils ok
def acesso_db():

    mydb = mysql.connector.connect(
        host="localhost", user="admin2024", password="204619", database="projeto_erp"
    )
    connect = mydb.connect()
    mycursor = mydb.cursor()
    return mydb, mycursor, connect

# utils ok
mydb, mycursor, connect = acesso_db()



#  utils ok
class AlertaMsg:
    def __init__(self):
        self.cnpj_invalido = self.cnpj_invalido
        self.cnpj_ja_existente = self.cnpj_ja_existente
        self.cad_fornecedor_realizado = self.cad_fornecedor_realizado

    @staticmethod
    def produto_ja_cadastrado(ean):
        print("class AlertaMsg: produto_ja_cadastrado()")
        session["alert"] = (
            f'<div id = "alert" class="alert alert-danger", '
            f'role="alert">PRODUTO JÁ CADASTRADO: EAN {ean}</div>'
        )
        return redirect(url_for("cadastrar_produtos"))

    @staticmethod
    def produto_incluido_na_tabela(ean, descricao):
        print("class AlertaMsg: produto_incluido_na_tabela()")
        session["alert"] = (
            f'<div id = "alert" class="alert alert-success", '
            f'role="alert">PRODUTO INCLUIDO NA TABELA: EAN {ean} | {descricao}</div>'
        )
        return redirect(url_for("cadastrar_produtos"))

    @staticmethod
    def produto_ja_digitado():
        print("class AlertaMsg: produto_ja_digitado()")
        session["alert"] = (
            f'<div id = "alert" class="alert alert-danger", role="alert">PRODUTO JÁ DIGITADO</div>'
        )
        # return redirect(url_for('cadastrar_produtos'))

    @staticmethod
    def campos_em_branco():
        print(
            CorFonte.fonte_amarela()
            + "class AlertaMsg: campos_em_branco()"
            + CorFonte.reset_cor()
        )
        session["alert"] = (
            f'<div id = "alert" class="alert alert-danger", '
            f'role="alert">TODOS OS CAMPOS DEVEM SER PREENCHIDOS</div>'
        )
        return redirect(url_for("cadastrar_produtos"))

    @staticmethod
    def campo_nf_em_branco():
        print(
            CorFonte.fonte_amarela()
            + "class AlertaMsg: campos_em_branco()"
            + CorFonte.reset_cor()
        )
        session["alert"] = (
            f'<div id = "alert" class="alert alert-danger", '
            f'role="alert">TODOS OS CAMPOS DEVEM SER PREENCHIDOS</div>'
        )
        return redirect(url_for("cadastrar_produtos"))
    @staticmethod
    def ean_ja_digitado(ean):
        print(
            CorFonte.fonte_amarela()
            + "class AlertaMsg: ean_ja_digitado()"
            + CorFonte.reset_cor()
        )
        session["alert"] = (
            f'<div id = "alert" class="alert alert-danger", '
            f'role="alert">EAN {ean} JÁ CONSTA NA TABELA DE ITENS A CADASTRAR</div>'
        )
        return redirect(url_for("cadastrar_produtos"))

    @staticmethod
    def produto_cadastrado_com_sucesso():
        print(
            CorFonte.fonte_amarela()
            + "class AlertaMsg: produto_cadastrado_com_sucesso()"
            + CorFonte.reset_cor()
        )
        session["alert"] = (
            '<div id = "alert" class="alert alert-success", '
            'role="alert">PRODUTO CADASTRADO COM SUCESSO</div>'
        )
        return redirect(url_for("cadastrar_produtos"))

    @staticmethod
    def fornecedor_invalido_cad_prod():
        print(
            CorFonte.fonte_amarela()
            + "class AlertaMsg: fornecedor_invalido_cad_prod()"
            + CorFonte.reset_cor()
        )
        session["alert"] = (
            '<div id="alert" class="alert alert-danger" '
            'role="alert">INSIRA UM FORNECEDOR VÁLIDO</div>'
        )
        return redirect(url_for("cadastrar_produtos"))

    @staticmethod
    def cad_fornecedor_realizado():
        print(
            CorFonte.fonte_amarela()
            + "class AlertaMsg: cad_fornecedor_realizado()"
            + CorFonte.reset_cor()
        )
        session["alert"] = (
            '<div id="alert" class="alert alert-success", role="alert">CADASTRO REALIZADO!</div>'
        )
        return redirect(url_for("cadastrar_fornecedores"))

    @staticmethod
    def fornecedor_invalido():
        print(
            CorFonte.fonte_amarela()
            + "class AlertaMsg: fornecedor_invalido()"
            + CorFonte.reset_cor()
        )
        session["alert"] = (
            '<div id="alert" class="alert alert-danger" role="alert">INSIRA UM FORNECEDOR VÁLIDO</div>'
        )
        return redirect(url_for("cadastrar_fornecedores"))

    @staticmethod
    def cnpj_invalido():
        print(
            CorFonte.fonte_amarela()
            + "class AlertaMsg: cnpj_invalido()"
            + CorFonte.reset_cor()
        )
        session["alert"] = (
            '<div id = "alert" class="alert alert-danger" role="alert">CNPJ INVALIDO!</div>'
        )
        return redirect(url_for("cadastrar_fornecedores"))

    @staticmethod
    def cnpj_ja_existente():
        print(
            CorFonte.fonte_amarela()
            + "class AlertaMsg: cnpj_ja_existente()"
            + CorFonte.reset_cor()
        )
        session["alert"] = (
            '<div id = "alert" class="alert alert-danger" role="alert">CNPJ JA EXISTENTE!</div>'
        )
        return redirect(url_for("cadastrar_fornecedores"))

    @staticmethod
    def cadastro_inexistente():
        print(
            CorFonte.fonte_amarela()
            + "class AlertaMsg: cadastro_inexistente()"
            + CorFonte.reset_cor()
        )
        session["alert"] = (
            '<div id = "alert" class="alert alert-danger" role="alert">CADASTRO INEXISTENTE</div>'
        )
        return redirect(url_for("gerar_ordem_de_compra"))

#  utils ok
class Formatadores:
    @staticmethod
    def formatar_xml(nome_arquivo):
        print(
            CorFonte.fonte_amarela()
            + "class Formatadores | metodo formatar_xml"
            + CorFonte.reset_cor()
        )
        print(
            "Método formatar_xml"
            "Recebe a chave da nf e "
            "retorna ean, quantidade, preco unitário e total do item"
        )

        # Definir namespace
        lista_itens_nf_nova = ""
        namespace = {"nfe": "http://www.portalfiscal.inf.br/nfe"}
        xml_filename = f"{nome_arquivo}.xml"  # Definir o caminho da pasta onde o arquivo XML está localizado
        xml_path = os.path.join(pasta_xml, xml_filename)
        if not os.path.isfile(xml_path):  # Verificar se o arquivo existe
            print(f"Arquivo {xml_path} não encontrado.")
        else:
            try:
                tree = ET.parse(xml_path)  # Carregar e analisar o arquivo XML
                root = tree.getroot()
                ide = root.find(
                    ".//nfe:ide", namespace
                )  # Acessar informações gerais da nota fiscal
                emit = root.find(".//nfe:emit", namespace)
                dest = root.find(".//nfe:dest", namespace)
                nf_info = {
                    "UF": ide.find("nfe:cUF", namespace).text,
                    "Número NF": ide.find("nfe:nNF", namespace).text,
                    "Data de Emissão": ide.find("nfe:dhEmi", namespace).text,
                    "Emitente": {
                        "CNPJ": emit.find("nfe:CNPJ", namespace).text,
                        "Nome": emit.find("nfe:xNome", namespace).text,
                    },
                    "Destinatário": {
                        "CNPJ": dest.find("nfe:CNPJ", namespace).text,
                        "Nome": dest.find("nfe:xNome", namespace).text,
                    },
                    "Produtos": [],
                }

                produto_info = []
                for det in root.findall(
                    ".//nfe:det", namespace
                ):  # Extrair todos os produtos
                    prod = det.find("nfe:prod", namespace)
                    produto_info = {
                        "Ean": prod.find("nfe:cEANTrib", namespace).text,
                        # 'Código': prod.find('nfe:cProd', namespace).text,
                        # 'Descrição': prod.find('nfe:xProd', namespace).text,
                        "Quantidade": int(float(prod.find("nfe:qCom", namespace).text)),
                        "Valor Unitário": int(
                            float(prod.find("nfe:vUnCom", namespace).text)
                        ),
                        "Valor Total": int(
                            float(prod.find("nfe:vProd", namespace).text)
                        ),
                    }
                    nf_info["Produtos"].append(produto_info)

                lista_itens_nf = []
                lista_itens_nf_temp = []
                lista_itens_nf_nova = []
                lista_itens_nf_temp_nova = []

                for key, value in nf_info.items():  # Imprimir as informações extraídas
                    if isinstance(value, list):
                        for (
                            item
                        ) in (
                            value
                        ):  # cada 'item' é uma linha contendo todos os campos de 'produto_info'
                            item = dict(item)
                            lista_itens_nf_temp.append(item)
                            lista_itens_nf.append(lista_itens_nf_temp[:])
                            lista_itens_nf_temp.clear()
                        for lista_in_dict in lista_itens_nf:
                            for i in lista_in_dict:
                                lista_itens_nf_temp_nova.append(i["Ean"])
                                lista_itens_nf_temp_nova.append(i["Quantidade"])
                                lista_itens_nf_temp_nova.append(i["Valor Unitário"])
                                lista_itens_nf_temp_nova.append(i["Valor Total"])
                                lista_itens_nf_nova.append(lista_itens_nf_temp_nova[:])
                                lista_itens_nf_temp_nova.clear()
                        print("lista_itens_nf_nova >> finalizada")

            except ET.ParseError as e:
                print(f"Erro ao analisar o arquivo XML: {e}")
            except AttributeError as e:
                print(f"Erro ao acessar elementos no XML: {e}")

        return lista_itens_nf_nova

    @staticmethod
    def formatar_data(data):
        print(
            CorFonte.fonte_amarela()
            + "class Formatadores | metodo formatar_data"
            + CorFonte.reset_cor()
        )
        return data.strftime("%d/%m/%Y")

    @staticmethod
    def data_formato_db(data):
        print(
            CorFonte.fonte_amarela()
            + "class Formatadores | metodo data_formato_db"
            + CorFonte.reset_cor()
        )
        return data.strftime("%Y-%m-%d")

    @staticmethod
    def os_data():
        print(
            CorFonte.fonte_amarela()
            + "class Formatadores | metodo os_data"
            + CorFonte.reset_cor()
        )
        agora = date.today()
        return agora

# utils ok
class ValidaStatusPedido:

    def __init__(self):
        pass

    @staticmethod
    def validacao_1(status_ordem):
        print(
            CorFonte.fonte_amarela()
            + "class ValidaStatusPedido | metodo validacao_1"
            + CorFonte.reset_cor()
        )
        print(
            "class ValidaStatusPedido | metodo validacao_1"
            "Objetivo: Verificar se o xml está no servidor"
        )

        if status_ordem is True:
            return True
        else:  # xml nao localizado
            return False

    @staticmethod
    def validacao_2(cnpj):
        print(
            CorFonte.fonte_amarela()
            + "class ValidaStatusPedido | metodo validacao_2"
            + CorFonte.reset_cor()
        )
        print(
            "class ValidaStatusPedido | metodo validacao_2"
            "Objetivo: Verificar se o fornecedor está cadastrado"
        )
        # print(fonte_amarela + 'VALIDAÇÃO 2: VERIFICAR SE O FORNECEDOR ESTÁ CADASTRADO' + reset_cor)
        if Buscadores.buscar_cnpj(cnpj) is True:
            print(
                CorFonte.fonte_azul()
                + f"cnpj encontrado: {cnpj}"
                + CorFonte.reset_cor()
            )
            # print(fonte_verde + 'VALIDAÇÃO 2 concluída' + reset_cor)
            return True
        else:
            print("cnpj não encontrado")
            # lst_nf = ['Fornecedor não encontrado']
            return False

    @staticmethod
    def validacao_3(status_ordem, ordem):
        print(
            CorFonte.fonte_amarela()
            + "class ValidaStatusPedido | metodo validacao_3"
            + CorFonte.reset_cor()
        )
        print(
            "class ValidaStatusPedido | metodo validacao_3"
            "Objetivo: Verificar se o pedido está aberto"
        )
        # print(fonte_amarela + 'VALIDÇÃO 3: VERIFICAR SE O PEDIDO ESTÁ EM ABERTO' + reset_cor)
        if status_ordem is True:
            # print(CorFonte.fonte_azul() + f'Pedido {ordem} aberto' + CorFonte.fonte_azul())
            # print(fonte_verde + 'VALIDAÇÃO 3 concluída' + reset_cor)
            return True
        else:
            print(
                CorFonte.fonte_vermelha()
                + "Pedido encerrado ou cancelado"
                + CorFonte.reset_cor()
            )
            return False

    @staticmethod
    def validacao_4(nf, ordem):
        print(
            CorFonte.fonte_amarela()
            + "class ValidaStatusPedido | metodo validacao_4"
            + CorFonte.reset_cor()
        )
        print(
            "class ValidaStatusPedido | metodo validacao_4"
            "Objetivo: Verificar ordem x nf"
        )
        # print(fonte_amarela + 'VALIDAÇÃO 4: VALIDAR PEDIDO X NF' + reset_cor)
        itens_nf = Buscadores.Xml.buscar_linhas_nf(str(nf))
        # print(f'itens_nf = {itens_nf}')
        # print(fonte_amarela + 'VALIDAÇÃO 4: (2) RECEBER OC, CRIAR LISTA DE EAN E PRECO' + reset_cor)
        itens_oc = Validadores.valida_pedido_recebido(ordem)
        # print(f'itens_oc = {itens_oc}')
        # print(fonte_amarela + 'VALIDAÇÃO 4: (3) COMPARAR AS DUAS LISTAS' + reset_cor)
        # maior_dif_permitida = modulos.admin.maior_dif_permitida
        maior_dif_permitida = 0.2
        # print(f'maior_dif_permitida = {maior_dif_permitida}')
        cont_preco_fora_politica = 0

        # print('for ean_oc in itens_oc:')
        for ean_oc in itens_oc:  # 'oc' = 'ordem de compra'
            # print(f'ean pesquisado: {ean_oc[0]}')

            for ean_nf in itens_nf:
                # print(f'ean_nf = {ean_nf[0]}')
                if ean_oc[0] == ean_nf[0]:
                    # print(CorFonte.fonte_azul() + f'ean_oc[0] = {ean_oc[0]} || ean_oc[1] = {ean_oc[1]}'
                    #                    f'ean_nf[0] = {ean_nf[0]} || ean_nf[1] = {ean_nf[1]}' + CorFonte.reset_cor())
                    if (ean_oc[1] - ean_nf[1]) <= maior_dif_permitida:
                        print(
                            CorFonte.fonte_verde()
                            + f"preco dentro da politica"
                            + CorFonte.reset_cor()
                        )
                    else:
                        print(
                            CorFonte.fonte_vermelha()
                            + f"preco fora da politica"
                            + CorFonte.reset_cor()
                        )
                        cont_preco_fora_politica += 1

        if cont_preco_fora_politica == 0:
            return True
        else:
            return False

#  utils ok
class Validadores:

    @staticmethod
    def valida_pedido_recebido(pedido):
        # 1 faz a query no banco de dados e retorna uma lista com os itens do pedido
        print(
            CorFonte.fonte_amarela()
            + "class Validadores | metodo valida_pedido_recebido"
            + CorFonte.reset_cor()
        )

        lista_itens = []
        query = f"SELECT * FROM ORDEM_COMPRA WHERE ORDEM_COMPRA  = '{pedido}'"
        mydb.connect()
        mycursor.execute(query)
        itens_ordem_de_compra = mycursor.fetchall()
        mydb.commit()
        valida_itens = ""

        try:
            if itens_ordem_de_compra:
                for i in itens_ordem_de_compra:
                    item_zip = (i[7], i[9])
                    lista_itens.append(item_zip)

            return lista_itens
        except Exception as e:
            print(f"Erro: {e}")
            return False

    @staticmethod
    def valida_status_pedido(pedido):
        print(CorFonte.fonte_amarela() + "class Validadores | metodo valida_status_pedido" + CorFonte.reset_cor())
        lista_itens = []
        # 1 faz a query no banco de dados e retorna uma lista com os itens do pedido

        query = f"SELECT * FROM ORDEM_COMPRA WHERE ORDEM_COMPRA  = '{pedido}'"
        mydb.connect()
        mycursor.execute(query)
        itens_ordem_de_compra = mycursor.fetchall()
        mydb.commit()
        valida_itens = ""
        for i in itens_ordem_de_compra:
            print(i)
        print("-------------------------------")
        try:
            return itens_ordem_de_compra
        except Exception as e:
            print(f"Erro: {e}")
            return False

    ordem_compra = ""

    @staticmethod
    def valida_cnpj(cnpj):
        print(
            CorFonte.fonte_amarela()
            + "class Validadores | metodo valida_cnpj"
            + CorFonte.reset_cor()
        )
        print("class Validadores | método valida_cnpj")
        print(f"cnpj original {cnpj}")
        cnpj = str(cnpj)
        print(f"cnpj convertido {cnpj}")
        return validador_cnpj.validate(cnpj)

    @staticmethod
    def valida_inscricao_estadual(insc_estadual):
        print(
            CorFonte.fonte_amarela()
            + "class Validadores | metodo valida_inscricao_estadual"
            + CorFonte.reset_cor()
        )

        insc_estadual = str(insc_estadual)
        if len(insc_estadual) != 9:
            return False
        else:
            return True

# utils ok
class AtualizaCodigo:
    @staticmethod
    def cod_produto():
        print(
            CorFonte.fonte_amarela()
            + "class AtualizaCodigo | metodo cod_produto"
            + CorFonte.reset_cor()
        )
        try:
            query = "SELECT MAX(CODIGO) FROM PRODUTOS"
            mydb.connect()
            mycursor.execute(query)
            myresult = mycursor.fetchall()
            mydb.commit()
            max_codigo = 0
            for x in myresult:
                max_codigo = x[0]
            max_codigo = int(max_codigo)
            max_codigo = max_codigo + 1
            max_codigo = str(max_codigo)
            if len(max_codigo) == 1:
                max_codigo = "00000" + max_codigo
            if len(max_codigo) == 2:
                max_codigo = "0000" + max_codigo
            if len(max_codigo) == 3:
                max_codigo = "000" + max_codigo
            if len(max_codigo) == 4:
                max_codigo = "00" + max_codigo
            if len(max_codigo) == 5:
                max_codigo = "0" + max_codigo
            return max_codigo
        except:
            max_codigo = "000001"
            return max_codigo

    @staticmethod
    def cod_fornecedor():
        print(
            CorFonte.fonte_amarela()
            + "class AtualizaCodigo | metodo cod_fornecedor"
            + CorFonte.reset_cor()
        )
        try:
            query = "SELECT MAX(CODIGO) FROM fornecedores"
            mydb.connect()
            mycursor.execute(query)
            myresult = mycursor.fetchall()
            mydb.commit()
            max_codigo = 0
            for x in myresult:
                max_codigo = x[0]
            max_codigo = int(max_codigo)
            max_codigo = max_codigo + 1
            max_codigo = str(max_codigo)
            if len(max_codigo) == 1:
                max_codigo = "00000" + max_codigo
            if len(max_codigo) == 2:
                max_codigo = "0000" + max_codigo
            if len(max_codigo) == 3:
                max_codigo = "000" + max_codigo
            if len(max_codigo) == 4:
                max_codigo = "00" + max_codigo
            if len(max_codigo) == 5:
                max_codigo = "0" + max_codigo
            return max_codigo
        except:
            max_codigo = "000001"
            return max_codigo

    @staticmethod
    def ordem_compra():
        print(
            CorFonte.fonte_amarela()
            + "class AtualizaCodigo | metodo ordem_compra"
            + CorFonte.reset_cor()
        )
        try:
            query =f"SELECT MAX(ORDEM_COMPRA) FROM ordem_compra"

            print(f'query: {query}')
            mydb.connect()
            mycursor.execute(query)
            myresult = mycursor.fetchall()
            print(f'myresult: {myresult[0][0]}')
            if myresult[0][0] is None:  # se nao houver ordem_compra cadastrada
                myresult = '000000'
            mydb.commit()
            ordem_compra_atual = 0
            for x in myresult:
                ordem_compra_atual = x[0]
            ordem_compra_atual = int(ordem_compra_atual)

            ordem_compra_atual = ordem_compra_atual + 1
            ordem_compra_atual = str(ordem_compra_atual)

            if len(ordem_compra_atual) == 1:
                ordem_compra_atual = "00000" + ordem_compra_atual

            if len(ordem_compra_atual) == 2:
                ordem_compra_atual = "0000" + ordem_compra_atual

            if len(ordem_compra_atual) == 3:
                ordem_compra_atual = "000" + ordem_compra_atual


            if len(ordem_compra_atual) == 4:
                ordem_compra_atual = "00" + ordem_compra_atual


            if len(ordem_compra_atual) == 5:
                ordem_compra_atual = "0" + ordem_compra_atual

            else:
                ordem_compra_atual = ordem_compra_atual

            return ordem_compra_atual
        except Exception as e:
            print(e)
            ordem_compra_atual = "000001"
            return

# utils ok
class Buscadores:
    def __init__(self):
        pass

    def buscar_cnpj(cnpj):
        print(
            CorFonte.fonte_amarela()
            + "class Buscadores | metodo buscar_cnpj"
            + CorFonte.reset_cor()
        )
        mydb.connect()
        query = f"SELECT * FROM fornecedores WHERE CNPJ = '{cnpj}'"
        mycursor.execute(query)
        myresult = mycursor.fetchall()

        if len(myresult) == 0:
            return False
        else:
            return True

    class Xml:
        chave_nf = ""
        nome_arquivo = ""
        pasta_xml = r"C:\relato\XML\ANTIGOS"

        @staticmethod
        def retorna_xml(nf):
            print(
                CorFonte.fonte_amarela()
                + "class Buscadores.Xml | metodo retorna_xml"
                + CorFonte.reset_cor()
            )
            print("Recebe a NF e retorna o caminho do XML")
            pasta_xml = r"C:\relato\XML\ANTIGOS"
            namespaces = {"ns1": "http://www.portalfiscal.inf.br/nfe"}
            arquivo_encontrado = None
            lst_zipada = []

            for arquivo in os.listdir(
                pasta_xml
            ):  # Procura pelo arquivo na pasta especificada
                if nf in arquivo[26:34] and arquivo.endswith("-nfe.xml"):
                    arquivo_encontrado = os.path.join(pasta_xml, arquivo)
                    print(f"arquivo encontrado >> {arquivo_encontrado}")
                    # print('----------------------------------------------')
            return arquivo_encontrado[22:-4]

        @staticmethod
        def buscar_linhas_nf(nf):
            print(
                CorFonte.fonte_amarela()
                + "class Buscadores.Xml | metodo buscar_linhas_nf"
                + CorFonte.reset_cor()
            )
            pasta_xml = r"C:\relato\XML\ANTIGOS"
            namespaces = {"ns1": "http://www.portalfiscal.inf.br/nfe"}
            arquivo_encontrado = None
            lst_zipada = []

            for arquivo in os.listdir(
                pasta_xml
            ):  # Procura pelo arquivo na pasta especificada
                if nf in arquivo[26:34] and arquivo.endswith("-nfe.xml"):
                    arquivo_encontrado = os.path.join(pasta_xml, arquivo)
                    print(f"arquivo encontrado >> {arquivo_encontrado}")
                    break

            if arquivo_encontrado:  # Verifica se o arquivo foi encontrado
                xNome4 = ""
                lst_produto = []
                lst_ean = []
                lst_icms = []
                lst_val_compra = []
                tree = ET.parse(arquivo_encontrado)
                root = tree.getroot()
                for det in root.findall(".//ns1:det", namespaces):
                    # xNome4 = det.find('.//ns1:xNome4', namespaces)
                    cProd = det.find(".//ns1:cProd", namespaces)
                    cEAN = det.find(".//ns1:cEANTrib", namespaces)
                    pICMS = det.find(".//ns1:pICMS", namespaces)
                    vUnCom = det.find(".//ns1:vUnCom", namespaces)
                    vUnCom.text = vUnCom.text.replace(".", ",")
                    vUnCom.text = vUnCom.text.replace(",", ".")
                    vUnCom.text = vUnCom.text.replace(" ", "")
                    vUnCom.text = vUnCom.text.rstrip("0")
                    item_zip = (cEAN.text, float(vUnCom.text))
                    lst_zipada.append(item_zip)
            else:
                print("Arquivo não encontrado")
                return None
            # print("----------------------------------------------")
            return lst_zipada

        @staticmethod
        def buscar_arquivo(nf):
            print(
                CorFonte.fonte_amarela()
                + "class Buscadores.Xml | metodo buscar_arquivo"
                + CorFonte.reset_cor()
            )

            nf = str(nf)
            for nome_arquivo in os.listdir(pasta_xml):
                i = nome_arquivo
                i = i[25:34]  # pegar apenas o num da nf
                i = i.lstrip("0")  # tirar zeros a esquerda
                if i == nf:
                    print(f"NFO {i}/{nf} localizada na pasta")
                    # print("----------------------------------------------")
                    return nome_arquivo

        @staticmethod
        def buscar_colunas_xml(nome_arquivo):
            print(
                CorFonte.fonte_amarela()
                + "class Buscadores.Xml | metodo buscar_colunas_xml"
                + CorFonte.reset_cor()
            )
            nome_arquivo = f"{pasta_xml}/{nome_arquivo}"

            def extrair_tags(element, prefix=""):
                tags = set()
                for child in element:
                    tag_name = f"{prefix}/{child.tag.split('}')[-1]}"
                    print("tag_name >>>", tag_name)
                    tags.add(tag_name)
                    tags.update(extrair_tags(child, tag_name))
                return tags

            try:
                tree = ET.parse(nome_arquivo)  # Parse do XML
                root_element = tree.getroot()
                colunas = extrair_tags(root_element)  # Extrair todas as tags
                print(f"Colunas encontradas: {colunas}")
                return colunas

            except ET.ParseError:
                print(f"Erro ao analisar o arquivo: {nome_arquivo}")
                return None

        @staticmethod
        def buscar_cnpj(nome_arquivo):
            print(
                CorFonte.fonte_amarela()
                + "class Buscadores.Xml | metodo buscar_cnpj"
                + CorFonte.reset_cor()
            )
            nome_arquivo = f"{pasta_xml}/{nome_arquivo}"
            try:
                tree = ET.parse(nome_arquivo)  # Parse do XML
                root_element = tree.getroot()
                # Obter namespace
                namespaces = {
                    node[0]: node[1]
                    for _, node in ET.iterparse(nome_arquivo, events=["start-ns"])
                }
                # Buscar o elemento CNPJ específico
                cnpj_element = root_element.find(
                    ".//{http://www.portalfiscal.inf.br/nfe}CNPJ", namespaces
                )

                # USE O CODIGO ABAIXO PARA EXTRAIR O CNPJ DO DESTINATÁRIO
                # cnpj_element = root_element.find(
                #     './/{http://www.portalfiscal.inf.br/nfe}NFe/'
                #     '{http://www.portalfiscal.inf.br/nfe}infNFe/'
                #     '{http://www.portalfiscal.inf.br/nfe}dest/'
                #     '{http://www.portalfiscal.inf.br/nfe}CNPJ',
                #     namespaces)

                if cnpj_element is not None:
                    cnpj = cnpj_element.text
                    print(f" CNPJ: {cnpj}")
                    return cnpj
                else:
                    print("CNPJ não encontrado")
                    return None

            except ET.ParseError:
                print(f"Erro ao analisar o arquivo: {nome_arquivo}")
                return None

        @staticmethod
        def buscar_pedido(nome_arquivo):
            print(
                CorFonte.fonte_amarela()
                + "class Buscadores.Xml | metodo buscar_pedido"
                + CorFonte.reset_cor()
            )
            nome_arquivo = f"{pasta_xml}/{nome_arquivo}"
            try:
                tree = ET.parse(nome_arquivo)  # Parse do XML
                root_element = tree.getroot()
                namespaces = {
                    node[0]: node[1]
                    for _, node in ET.iterparse(nome_arquivo, events=["start-ns"])
                }
                # Buscar o elemento xPed específico
                xped_element = root_element.find(
                    ".//{http://www.portalfiscal.inf.br/nfe}xPed", namespaces
                )
                if xped_element is not None:
                    pedido = xped_element.text
                    return pedido
                else:
                    print("Ordem de Compra não encontrada com namespace")

                xped_element_no_ns = root_element.find(
                    ".//xPed"
                )  # Buscar o elemento xPed específico sem considerar namespace

                if xped_element_no_ns is not None:
                    print(f"xPed encontrado sem namespace: {xped_element_no_ns.text}")
                    return xped_element_no_ns.text
                else:
                    print("xPed não encontrado sem namespace")

                return None

            except ET.ParseError:
                print(f"Erro ao analisar o arquivo: {nome_arquivo}")
                return None

        @staticmethod
        def buscar_razao_social(nome_arquivo):
            print(
                CorFonte.fonte_amarela()
                + "class Buscadores.Xml | metodo buscar_razao_social"
                + CorFonte.reset_cor()
            )
            nome_arquivo = f"{pasta_xml}/{nome_arquivo}"
            try:
                tree = ET.parse(nome_arquivo)  # Parse do XML
                root_element = tree.getroot()
                namespaces = {
                    node[0]: node[1]
                    for _, node in ET.iterparse(nome_arquivo, events=["start-ns"])
                }
                # Buscar o elemento CNPJ específico
                razao_social = root_element.find(
                    ".//{http://www.portalfiscal.inf.br/nfe}xNome", namespaces
                )
                # USE O CODIGO ABAIXO PARA EXTRAIR A RAZAO SOCIAL DO DESTINATÁRIO
                # razao_social = root_element.find('.//{http://www.portalfiscal.inf.br/nfe}NFe/'
                #                                  '{http://www.portalfiscal.inf.br/nfe}infNFe/'
                #                                  '{http://www.portalfiscal.inf.br/nfe}dest/'
                #                                  '{http://www.portalfiscal.inf.br/nfe}xNome', namespaces)
                if razao_social is not None:
                    razao_social_ = razao_social.text
                    print(f"RAZAO SOCIAL: {razao_social_}")
                    return razao_social_
                else:
                    print("RAZAO SOCIAL não encontrado")
                    return None
            except ET.ParseError:
                print(f"Erro ao analisar o arquivo: {nome_arquivo}")
                return None

    class OrdemCompra:
        @staticmethod
        def atualizar_estoque(
            data,
            tipo_mov,
            ordem_compra,
            nota_fiscal,
            ean,
            codigo,
            descricao,
            quantidade,
            valor,
            usuario,
        ):
            print(
                CorFonte.fonte_amarela()
                + "class Buscadores.OrdemCompra | metodo atualizar_saldo_ordem_compra"
                + CorFonte.reset_cor()
            )

            query = """
            INSERT INTO ESTOQUE
            (DATA, TIPO_MOV, ORDEM_COMPRA, NOTA_FISCAL, EAN, CODIGO, DESCRICAO, QUANTIDADE, VALOR, USUARIO)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            valores = (
                data,
                tipo_mov,
                ordem_compra,
                nota_fiscal,
                ean,
                codigo,
                descricao,
                quantidade,
                valor,
                usuario)
            # print(f'query: {query}-{valores}')
            mydb.connect()
            mycursor.execute(query, valores)
            mycursor.fetchall()
            mydb.commit()
            mydb.close()

        @staticmethod
        def atualizar_saldo_ordem_compra(ordem_compra, ean, quantidade, valor):

            print(CorFonte.fonte_amarela()
                  + f"class Buscadores.OrdemCompra | metodo atualizar_saldo_ordem_compra | {ordem_compra}"
                  + CorFonte.reset_cor())
            status = 'ABERTO'
            consulta = f'SELECT * FROM ORDEM_COMPRA WHERE ORDEM_COMPRA = "0{ordem_compra}" and EAN = "{ean}";'
            mydb.connect()
            mycursor.execute(consulta)

            #  1 - mostra o saldo da ordem de compra
            resultado_consulta = mycursor.fetchall()
            # print(f'res consulta: {resultado_consulta}')

            # 2 - compara o saldo_qtd com a quantidade digitada pelo usuario
            saldo_qtd = resultado_consulta[0][11]
            qtde_inicial = resultado_consulta[0][8]

            # 3 - se o saldo_qtd  for maior que 0 e menor que qtde_inicial, entao o status eh PARCIALMENTE RECEBIDO

            quantidade = int(quantidade)
            print(f'quantidade: {quantidade}')
            if quantidade == 0:
                pass


            elif saldo_qtd > 0 and ((saldo_qtd - quantidade) > 0):
                status = 'PARCIALMENTE RECEBIDO'
                print(f'saldo_qtd: {saldo_qtd} | status: {status}')

                saldo_valor_consulta = resultado_consulta[0][12]
                saldo_valor_consulta = float(saldo_valor_consulta)

                saldo_total_item = (saldo_qtd - quantidade) * valor
                print(f'saldo_total_item: {saldo_total_item}')
                query = (f'UPDATE ORDEM_COMPRA SET '
                         f'SALDO_QTD = "{saldo_qtd - quantidade}", '
                         f'SALDO_TOTAL_ITEM = "{saldo_total_item}",'
                         f'STATUS = "{status}"'
                         f'WHERE ORDEM_COMPRA = "0{ordem_compra}" and EAN = "{ean}" ;')

                print(query)
                mycursor.execute(query)
                mycursor.fetchall()
                mydb.commit()
                mydb.close()

            elif saldo_qtd > 0 and ((saldo_qtd - quantidade) == 0):
                status = 'RECEBIMENTO FINALIZADO'
                print(f'saldo_qtd: {saldo_qtd} | status: {status}')

                quantidade = int(quantidade)
                print(f'Foram Recebidas {quantidade} Unidades de Venda')

                saldo_valor_consulta = resultado_consulta[0][12]
                saldo_valor_consulta = float(saldo_valor_consulta)

                saldo_total_item = (saldo_qtd - quantidade) * valor
                print(f'saldo_total_item: {saldo_total_item}')
                query = (f'UPDATE ORDEM_COMPRA SET '
                         f'SALDO_QTD = "{saldo_qtd - quantidade}", '
                         f'SALDO_TOTAL_ITEM = "{saldo_total_item}",'
                         f'STATUS = "{status}"'
                         f'WHERE ORDEM_COMPRA = "0{ordem_compra}" and EAN = "{ean}" ;')

                print(query)
                mycursor.execute(query)
                mycursor.fetchall()
                mydb.commit()
                mydb.close()

            elif saldo_qtd > 0 and ((saldo_qtd - quantidade) < 0):
                status = 'RECEBIMENTO FINALIZADO'
                print(f'saldo_qtd: {saldo_qtd} | status: {status}')
                quantidade = int(saldo_qtd)
                print(f'Foram Recebidas {quantidade} Unidades de Venda')
                print(f'Sobra de {quantidade - saldo_qtd} Unidades de Venda')
                saldo_valor_consulta = resultado_consulta[0][12]
                saldo_valor_consulta = float(saldo_valor_consulta)
                saldo_total_item = (saldo_qtd - quantidade) * valor
                print(f'saldo_total_item: {saldo_total_item}')
                query = (f'UPDATE ORDEM_COMPRA SET '
                         f'SALDO_QTD = "0", '
                         f'SALDO_TOTAL_ITEM = "0",'
                         f'STATUS = "{status}"'
                         f'WHERE ORDEM_COMPRA = "0{ordem_compra}" and EAN = "{ean}" ;')

                # print(query)
                mycursor.execute(query)
                mycursor.fetchall()
                mydb.commit()
                mydb.close()

            elif saldo_qtd < 0:
                status = 'RECEBIMENTO FINALIZADO'
                query = (f'UPDATE ORDEM_COMPRA SET '
                         f'SALDO_QTD = "0", '
                         f'SALDO_TOTAL_ITEM = "0",'
                         f'STATUS = "{status}"'
                         f'WHERE ORDEM_COMPRA = "0{ordem_compra}" and EAN = "{ean}" ;')

                # print(query)
                mycursor.execute(query)
                mycursor.fetchall()
                mydb.commit()
                mydb.close()



        @staticmethod
        def busca_saldo_ordem_compra(ordem_compra):
            print(
                CorFonte.fonte_amarela()
                + f"class Buscadores.OrdemCompra | metodo buscar_saldo_ordem_compra | {ordem_compra}"
                + CorFonte.reset_cor()
            )
            query = f'SELECT * FROM ORDEM_COMPRA WHERE ORDEM_COMPRA = "0{ordem_compra}";'
            # ajustar código para a que a qtde de '0' seja automática
            mydb.connect()
            mycursor.execute(query)
            resultado = mycursor.fetchall()

            mydb.commit()
            mydb.close()
            return resultado

        @staticmethod
        def verifica_status_ordem(ordem_compra):
            print(
                CorFonte.fonte_amarela()
                + f"class Buscadores.OrdemCompra | metodo verifica_status_ordem"
                + CorFonte.reset_cor()
            )
            print(f"Verifica status_ordem_compra: {ordem_compra}")
            if len(ordem_compra) == 5:
                ordem_compra = f'0{ordem_compra}'
            if len(ordem_compra) == 4:
                ordem_compra = f'00{ordem_compra}'
            if len(ordem_compra) == 3:
                ordem_compra = f'000{ordem_compra}'
            if len(ordem_compra) == 2:
                ordem_compra = f'0000{ordem_compra}'
            if len(ordem_compra) == 1:
                ordem_compra = f'00000{ordem_compra}'

            query = f'SELECT SUM(SALDO_QTD) FROM ORDEM_COMPRA WHERE ORDEM_COMPRA = "{ordem_compra}";'
            # ajustar código para a que a qtde de '0' seja automática
            mydb.connect()
            mycursor.execute(query)
            resultado = mycursor.fetchall()



            mydb.commit()
            mydb.close()
            print(f'resultado:\n {resultado}')
            i = 0
            for i in resultado:
                print(f'>>>>>>>>>>{i[0]}')
                if i[0] > 0:
                    return True
                else:
                    return False

        @staticmethod
        def buscar_nf2(nf):
            print(
                CorFonte.fonte_amarela()
                + f"class Buscadores.OrdemCompra | metodo buscar_nf2"
                + CorFonte.reset_cor()
            )
            print("class Buscadores.OrdemCompra | metodo buscar_nf2")
            nf = str(nf)
            cnpj_encontrado = []

            for chave_nf in os.listdir(pasta_xml):
                i = chave_nf
                i = i[25:34]  # pegar apenas o num da nf
                i = i.lstrip("0")  # tirar zeros a esquerda
                if i == nf:
                    print(f"nfo {i}/{nf} localizada na pasta")
                    print(chave_nf)
                    for root, dirs, files in os.walk(pasta_xml):
                        for file in files:
                            caminho_arquivo = os.path.join(root, file)
                            if file.endswith(".xml"):
                                if file == chave_nf:
                                    print(
                                        f"Arquivo encontrado nf >> {nf} | chave >> {chave_nf} | caminho >>> {caminho_arquivo}"
                                    )
                                    tree = ET.parse(caminho_arquivo)  ##
                                    print(f"tree >>> {tree}")
                                    root_element = tree.getroot()
                                    namespaces = {
                                        "ns1": root_element.tag.split("}")[0].strip("{")
                                    }
                                    for det in root_element.findall(
                                        ".//ns1:det", namespaces
                                    ):
                                        cnpj = det.find(".//ns1:CNPJ3", namespaces)
                                        razao_social = det.find(
                                            ".//ns1:xNome4", namespaces
                                        )
                                        print(f"cnpj det >>> {cnpj}")
                                        print(f"razao_social >>> {razao_social}")
                                    break

                    return cnpj_encontrado

        chave_nf = ""

        def buscar_nf(pasta_xml, chave_nf, nf):
            print(
                CorFonte.fonte_amarela()
                + f"class Buscadores.OrdemCompra | metodo buscar_nf"
                + CorFonte.reset_cor()
            )
            cnpjs_encontrados = []
            nf = str(nf)
            # Definir o caminho da pasta onde o arquivo XML está localizado
            for chave_nf in os.listdir(pasta_xml):
                i = chave_nf
                i = i[25:34]  # pegar apenas o num da nf
                i = i.lstrip("0")  # tirar zeros a esquerda
                if i == nf:
                    print(f"nfo {i}/{nf} localizada na pasta")
                    print(chave_nf)

            # Navegar pela pasta
            for root, dirs, files in os.walk(pasta_xml):
                for file in files:
                    if file.endswith(".xml"):
                        caminho_arquivo = os.path.join(root, file)
                        if file == chave_nf:
                            try:
                                tree = ET.parse(caminho_arquivo)
                                root_element = tree.getroot()
                                # Para ver o conteúdo do XML (opcional)
                                xml_string = ET.tostring(
                                    root_element, encoding="utf-8"
                                ).decode("utf-8")
                                # print(f'Conteúdo do XML:{xml_string}')

                                # Obter namespace
                                namespaces = {
                                    "ns1": root_element.tag.split("}")[0].strip("{")
                                }

                                # Buscar elementos com namespace
                                for det in root_element.findall(
                                    ".//ns1:det", namespaces
                                ):
                                    cnpj_element = det.find(".//ns1:CNPJ", namespaces)
                                    razao_social_element = det.find(
                                        ".//ns1:xNome", namespaces
                                    )

                                    if cnpj_element is not None:
                                        cnpj = cnpj_element.text
                                        print(f"CNPJ: {cnpj}")
                                    else:
                                        print("CNPJ não encontrado")

                                    if razao_social_element is not None:
                                        razao_social = razao_social_element.text
                                        print(f"Razão Social: {razao_social}")
                                    else:
                                        print("Razão Social não encontrada")

                                    cnpjs_encontrados.append((file, cnpj, razao_social))
                            except ET.ParseError:
                                print(f"Erro ao analisar o arquivo: {caminho_arquivo}")

            return cnpjs_encontrados, chave_nf

        @staticmethod
        def busca_fornecedor_pelo_ean(ean):
            print(
                CorFonte.fonte_amarela()
                + f"class Buscadores.OrdemCompra | metodo buscar_fornecedor_pelo_ean"
                + CorFonte.reset_cor()
            )
            print("class Buscadores.OrdemCompra | metodo buscar_fornecedor_pelo_ean")
            query = ""

            if ean:
                query = f"select * from produtos where ean = {ean}"
                mydb.connect()
                mycursor.execute(query)
                myresult = mycursor.fetchall()
                mydb.commit()
                mydb.close()
                return myresult
        # CRIAR UMA FUNÇÃO PARA PUXAR A ORDEM DE COMPRA E O SALDO DOS PRODUTOS.
        # SE O SALDO FOR 0, PRINTAR 'FINALIZADO' NA COLUNA STATUSS
        @staticmethod
        def buscar_ordem_compra2(ordem_compra, razaosocial):
            print(
                CorFonte.fonte_amarela()
                + f"class Buscadores.OrdemCompra | metodo buscar_ordem_compra2"
                + CorFonte.reset_cor()
            )
            print("class Buscadores.OrdemCompra | metodo buscar_ordem_compra2")
            query = ""
            try:
                if ordem_compra == "":
                    query = (
                        f"SELECT "
                        f"ORDEM_COMPRA.DATA, "
                        f"ORDEM_COMPRA.CODIGO, "
                        f"FORNECEDORES.RAZAOSOCIAL, "
                        f"ORDEM_COMPRA.ORDEM_COMPRA, "
                        f"ORDEM_COMPRA.TOTAL_ITEM "
                        f"FROM ORDEM_COMPRA "
                        f"INNER JOIN FORNECEDORES "
                        f"ON ORDEM_COMPRA.CODIGO = FORNECEDORES.CODIGO "
                        f'WHERE RAZAOSOCIAL like "%{razaosocial}%";'
                    )
                if razaosocial == "":
                    query = (
                        f"SELECT "
                        f"ORDEM_COMPRA.DATA, "
                        f"ORDEM_COMPRA.CODIGO, "
                        f"PRODUTOS.FORNECEDOR, "
                        f"ORDEM_COMPRA.ORDEM_COMPRA, "
                        f"ORDEM_COMPRA.TOTAL_ITEM "
                        f"FROM ORDEM_COMPRA "
                        f"INNER JOIN PRODUTOS "
                        f"ON ORDEM_COMPRA.DESCRICAO = PRODUTOS.DESCRICAO "
                        f'WHERE ORDEM_COMPRA like "%{ordem_compra}%" '
                        f"ORDER BY ORDEM_COMPRA DESC;"
                    )

                else:
                    query = (
                        f"SELECT "
                        f"ORDEM_COMPRA.DATA, "
                        f"ORDEM_COMPRA.CODIGO, "
                        f"PRODUTOS.FORNECEDOR, "
                        f"ORDEM_COMPRA.ORDEM_COMPRA, "
                        f"ORDEM_COMPRA.TOTAL_ITEM "
                        f"FROM ORDEM_COMPRA "
                        f"INNER JOIN PRODUTOS "
                        f"ON ORDEM_COMPRA.DESCRICAO = PRODUTOS.DESCRICAO "
                        f'WHERE ORDEM_COMPRA like "%{ordem_compra}%" AND FORNECEDOR like "%{razaosocial}%" '
                        f"ORDER BY ORDEM_COMPRA DESC;"
                    )

                mydb.connect()
                mycursor.execute(query)
                myresult = mycursor.fetchall()
                mydb.commit()
                mydb.close()
                return myresult
            except Exception as e:
                print(e)

                return

        @staticmethod
        def buscar_ordem_compra(ordem_compra):
            print(CorFonte.fonte_amarela()
                + f"class Buscadores.OrdemCompra | metodo buscar_ordem_compra"
                + CorFonte.reset_cor())

            try:
                query = (
                    f"select * from ordem_compra where ordem_compra = {ordem_compra}"
                )

                mydb.connect()
                mycursor.execute(query)
                myresult = mycursor.fetchall()
                mydb.commit()
                mydb.close()
                return myresult
            except Exception as e:
                print(e)
                pass

        @staticmethod
        def buscar_ordem_compra_pela_razaosocial(razaosocial):
            print(
                CorFonte.fonte_amarela()
                + f"class Buscadores.OrdemCompra | metodo buscar_ordem_compra_pela_razaosocial"
                + CorFonte.reset_cor()
            )
            print("Buscadores.OrdemCompra.buscar_ordem_compra_pela_razaosocial()")
            try:
                query = f'select * from ordem_compra where FORNECEDOR like "%{razaosocial}%"'
                # print(query)
                mydb.connect()
                mycursor.execute(query)
                myresult = mycursor.fetchall()
                mydb.commit()
                mydb.close()
                return myresult
            except Exception as e:
                print(e)
                pass

        @staticmethod
        def preco_medio(codigo):
            print(
                CorFonte.fonte_amarela()
                + f"class Buscadores.OrdemCompra | metodo preco_medio"
                + CorFonte.reset_cor()
            )

            try:
                query = f"select avg(preco) from ordem_compra where codigo = {codigo}"
                mydb.connect()
                mycursor.execute(query)
                myresult = mycursor.fetchall()
                mydb.commit()
                mydb.close()

                for i in myresult:
                    myresult = round(i[0], 2)
                if myresult is None:
                    myresult = 0
                return myresult
            except Exception as e:
                print(e)
                pass

        @staticmethod
        def visualizar_nf(nf):
            pass

        @staticmethod
        def ordem_compra_em_aberto(codigo):
            print(
                CorFonte.fonte_amarela()
                + f"class Buscadores.OrdemCompra | metodo ordem_compra_em_aberto"
                + CorFonte.reset_cor()
            )
            quantidade = 0
            valor = 0
            try:
                quantidade_em_aberto = f'select sum(quantidade) from ordem_compra where CODIGO = "{codigo}";'
                mydb.connect()
                mycursor.execute(quantidade_em_aberto)
                myresult_qtd = mycursor.fetchall()
                mydb.commit()
                mydb.close()

                for quantidade in myresult_qtd:
                    myresult_qtd = quantidade[0]

                valor_em_aberto = f'select sum(total_item) from ordem_compra where CODIGO = "{codigo}";'
                mydb.connect()
                mycursor.execute(valor_em_aberto)
                myresult_val = mycursor.fetchall()
                mydb.commit()
                mydb.close()
                # print(myresult)

                if codigo == 0:
                    myresult_qtd = 0
                    myresult_val = 0
                    print(myresult_qtd, myresult_val)

                for valor in myresult_val:
                    myresult_val = round(valor[0], 2)
                return myresult_qtd, myresult_val

            except Exception as e:
                print(e)

            pass

        @staticmethod
        def ultimo_preco(codigo):
            print(
                CorFonte.fonte_amarela()
                + f"class Buscadores.OrdemCompra | metodo ultimo_preco"
                + CorFonte.reset_cor()
            )
            try:
                query = f"select preco from ordem_compra where codigo = {codigo} order by ordem_compra desc limit 1;"
                mydb.connect()
                mycursor.execute(query)
                myresult = mycursor.fetchall()
                mydb.commit()
                mydb.close()
                # print(myresult)

                for i in myresult:
                    myresult = i[0]
                if myresult is None:
                    myresult = 0
                return myresult
            except Exception as e:
                print(e)
                pass

        @staticmethod
        def buscar_fornecedor():
            print(
                CorFonte.fonte_amarela()
                + f"class Buscadores.OrdemCompra | metodo buscar_fornecedor"
                + CorFonte.reset_cor()
            )
            try:
                query = f"select razaosocial from fornecedores order by razaosocial"
                mydb.connect()
                mycursor.execute(query)
                myresult = mycursor.fetchall()
                mydb.commit()
                mydb.close()
                lista_fornecedores = []
                for i in myresult:
                    lista_fornecedores.append(i)
                    lista_fornecedores = list(lista_fornecedores)
                return lista_fornecedores
            except:
                myresult = ""
                return myresult

        @staticmethod
        def buscar_pelo_fornecedor(fornecedor):
            print(
                CorFonte.fonte_amarela()
                + "classe Buscadores.OrdemCompra | Método buscar_pelo_fornecedor"
                + CorFonte.reset_cor()
            )
            try:
                query = f"select * from produtos where fornecedor LIKE '%{fornecedor}%' order by DESCRICAO"
                mydb.connect()
                mycursor.execute(query)
                myresult = mycursor.fetchall()
                mydb.commit()
                mydb.close()
                lista_produtos = []
                for i in myresult:
                    lista_produtos.append(i)
                    lista_produtos = list(lista_produtos)
                return lista_produtos
            except:
                myresult = ""
                return myresult

    def buscar_produto_pelo_ean(ean):
        print(
            CorFonte.fonte_amarela()
            + "classe Buscadores | método buscar_produto_pelo_ean"
            + CorFonte.reset_cor()
        )
        try:
            query = f'select * from produtos where ean = "{ean}"'
            mydb.connect()
            mycursor.execute(query)
            myresult = mycursor.fetchall()
            mydb.commit()
            mydb.close()
            # print(myresult)
            try:
                # print(len(myresult))

                if len(myresult) > 0:
                    return False
                else:
                    return True
            except Exception as e:
                return len(myresult), e
        except Exception as e:
            return e

    def buscar_produto_pelo_codigo(self):
        print(
            CorFonte.fonte_amarela()
            + "classe Buscadores | método buscar_produto_pelo_codigo"
            + CorFonte.reset_cor()
        )
        try:
            mydb.commit()
            mydb.connect()
            query = f"select * from produtos where CODIGO = {self}"

            mycursor.execute(query)
            myresult = mycursor.fetchall()
            print(f" myresult >>>> {myresult}")
            mydb.close()

            return myresult
        except:
            pass

    def buscar_produto_pela_descricao(self):
        print(
            CorFonte.fonte_amarela()
            + "classe Buscadores | metodo buscar pela descricao"
            + CorFonte.reset_cor()
        )
        try:
            query = f'select * from produtos where DESCRICAO = "{self}"'
            mydb.connect()
            mycursor.execute(query)
            myresult = mycursor.fetchall()
            mydb.commit()
            mydb.close()
            print(myresult)
            return myresult
        except:
            # geral.AlertaMsg.cadastro_inexistente()
            pass

    def buscar_produto_pela_descricao_e_fornecedor(descricao, fornecedor):
        print(
            CorFonte.fonte_amarela()
            + "class Buscadores | metodo buscar_produto_pela_descricao_e_fornecedor"
            + CorFonte.reset_cor()
        )
        try:
            query = f'select * from produtos where DESCRICAO like {descricao} and fornecedor = "{fornecedor}"'
            mydb.connect()
            mycursor.execute(query)
            myresult = mycursor.fetchall()
            mydb.commit()
            mydb.close()
            print(myresult)
            return myresult
        except Exception as e:
            print(e)
            # geral.AlertaMsg.cadastro_inexistente()
            pass

    @staticmethod
    def mostrar_tabela_produtos():
        print(
            CorFonte.fonte_amarela()
            + "classe Buscadores | metodo mostrar_tabela_de_produtos"
            + CorFonte.reset_cor()
        )
        mydb.connect()
        query = "select * from produtos"

        mycursor.execute(query)
        myresult = mycursor.fetchall()
        return myresult

    @staticmethod
    def buscar_nf_pelo_cnpj(cnpj):
        print(
            CorFonte.fonte_amarela()
            + "classe Buscadores | metodo buscar_nf_pelo_cnpj"
            + CorFonte.reset_cor()
        )
        nfs_encontradas = []
        print("metodo buscar nf pelo cnpj")
        print(f"buscar pelo cnpj >> {cnpj}")

        for root, dirs, files in os.walk(pasta_xml):
            for file in files:
                if file.endswith(".xml"):
                    caminho_arquivo = os.path.join(root, file)
                    try:
                        tree = ET.parse(caminho_arquivo)
                        root_element = tree.getroot()

                        # Ajuste o nome da tag conforme necessário
                        cnpj_element = root_element.find(".//CNPJ")
                        if cnpj_element is not None:
                            nfs_encontradas.append((file, cnpj_element.text))
                    except ET.ParseError:
                        print(f"Erro ao analisar o arquivo: {caminho_arquivo}")

#  utils ok
class Estoque:
    @staticmethod
    def atualiza_saldo_ordem_compra(ean, ordem_compra, quantidade, saldo_qtd, preco):
        print(
            CorFonte.fonte_amarela()
            + "class Estoque | metodo atualiza_saldo_ordem_compra" + CorFonte.reset_cor())


        qtd_atualizada = saldo_qtd - quantidade
        if qtd_atualizada < 0:
            qtd_atualizada = saldo_qtd
        saldo_total_item = qtd_atualizada * preco
        print(CorFonte.fonte_amarela() + "class Estoque | metodo atualiza_saldo_ordem_compra" + CorFonte.reset_cor())
        try:
            query = (f"UPDATE ORDEM_COMPRA SET "
                     f"SALDO_QTD ='{qtd_atualizada}'"
                     f"SALDO_TOTAL_ITEM = '{saldo_total_item}'"
                     # f"STATUS = '{status}'"
                     f"WHERE EAN = '{ean}' and ordem_compra = {ordem_compra} ;")
            print(query)
            mydb.connect()
            mycursor.execute(query)
            myresult = mycursor.fetchall()
            mydb.commit()
            mydb.close()
            print(myresult)
            return myresult
        except Exception as e:
            print(e)
            # geral.AlertaMsg.cadastro_inexistente()
            pass

    @staticmethod
    def relatorio_estoque(data_inicial, data_final, ordem_compra, ean, tipo_mov, nota_fiscal, descricao):
        estoque_processado = []
        estoque = []
        print(f'Relatorio Estoque')

        try:
            query = "SELECT * FROM ESTOQUE WHERE 1=1"  # query base
            parametros = []

            if data_inicial != None and data_inicial != '':

                query += " AND DATA >= %s"
                data_inicial = data_inicial.strftime('%Y-%m-%d')
                parametros.append(data_inicial)
                print(f'data_inicial = {data_inicial}')
            else:
                pass

            if data_final != None and data_final != '':
                query += " AND DATA <= %s"
                data_final = data_final.strftime('%Y-%m-%d')
                parametros.append(data_final)
                print(f'data_final = {data_final}')

            if ordem_compra != None and ordem_compra != '':
                query += " AND ORDEM_COMPRA = %s"
                parametros.append(ordem_compra)

            if ean != None and ean != '':
                query += " AND EAN = %s"
                parametros.append(f'{ean}')
            else:
                pass

            if tipo_mov is not None and tipo_mov is not '' and tipo_mov != 'Todos':
                query += " AND TIPO_MOV = %s"
                if tipo_mov == 'Saída':
                    tipo_mov = 'saida'
                parametros.append(tipo_mov.upper())
            else:
                pass

            if nota_fiscal is not None and nota_fiscal is not '':
                query += " AND NOTA_FISCAL = %s"
                parametros.append(nota_fiscal)
            else:
                pass

            if descricao is not None:
                query += " AND DESCRICAO LIKE %s"
                parametros.append(f"%s{descricao}%")


            query += ";"
            print(f'query: {query}')
            print(f'parametros: {parametros}')


            mydb.connect()
            mycursor.execute(query, parametros)
            estoque = mycursor.fetchall()
            saldo_qtd = 0
            saldo_valor = 0
            for item in estoque:
                data, tipo, ordem, nota, ean, cod, desc, qtd, valor, usuario = item
                total = qtd * valor
                saldo_qtd += qtd
                saldo_valor += total
                processamento = (item, total,saldo_qtd, saldo_valor)
                estoque_processado.append(processamento)
            mydb.commit()
            mydb.close()
        except Exception as e:
            print(e)
            pass

        return estoque_processado

def download_planilha():
    pasta = r"C:\Users\jean.lino\Downloads"  # Substitua pelo caminho da sua pasta
    file_name = "planilha.xlsx"
    file_path = os.path.join(pasta, file_name)

    # Crie a pasta se ela não existir
    os.makedirs(pasta, exist_ok=True)

    # Crie uma nova planilha
    workbook = openpyxl.Workbook()
    sheet = workbook.active

    # Adicione as colunas à planilha
    columns = [
        "Fornecedor",
        "EAN",
        "Valor",
        "Unidade",
        "Quantidade",
    ]  # Substitua pelos nomes das suas colunas
    sheet.append(columns)

    # Salve a planilha na pasta específica
    workbook.save(file_path)

    print(f"Planilha salva em: {file_path}")


