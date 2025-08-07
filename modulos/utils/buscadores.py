import logging

from modulos.utils.console import CorFonte
import os
import xml.etree.ElementTree as ET
from modulos.utils.queries import mydb, mycursor
from modulos.utils.formatadores import pasta_xml
from datetime import date
from modulos.utils.formatadores import Formatadores
data = Formatadores.os_data()
data_hoje = date.strftime(data, '%Y-%m-%d')

logging.disable(logging.CRITICAL)  # comente para habilitar
logging.disable(logging.WARNING)  # comente para habilitar
logging.disable(logging.INFO)  # comente para habilitar
logging.disable(logging.DEBUG)  # comente para habilitar


class Comercial:
    def __init__(self):
        pass


    @staticmethod
    def cadastrar_cliente(data, cod_cliente, razao_social, cnpj, insc_estadual, email, cep, telefone, endereco, municipio, uf, tabela, usuario):

        print(CorFonte.fonte_amarela()
            + "class Buscadores | metodo cadastrar_cliente"
            + CorFonte.reset_cor())
        query = """INSERT INTO CLIENTES(DATA,CODIGO,RAZAO_SOCIAL,CNPJ,INSCRICAO_ESTADUAL,EMAIL,CEP, TELEFONE,ENDERECO,MUNICIPIO,UF,TABELA,USUARIO) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        valores = (
            data,
            cod_cliente,
            razao_social,
            cnpj,
            insc_estadual,
            email,
            cep,
            telefone,
            endereco,
            municipio,
            uf,
            tabela,
            usuario)
        print('-------------------------------------')
        print(query, valores)
        print('-------------------------------------')
        mydb.connect()
        mycursor.execute(query, valores)
        # print(mycursor.statement)
        mycursor.fetchall()
        mydb.commit()
        mydb.close()

        pass

class Buscadores:
    def __init__(self):
        pass


    def buscar_cnpj(cnpj):
        """

        :return: cnpj
        """
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

    def buscar_cnpj_cliente(cnpj):
        """
        :return: cnpj
        """
        print(
            CorFonte.fonte_amarela()
            + "class Buscadores | metodo buscar_cnpj_fornecedor"
            + CorFonte.reset_cor()
        )
        mydb.connect()
        query = f"SELECT * FROM clientes WHERE CNPJ = '{cnpj}'"
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

    class OrdemVenda:
        def buscar_pelo_cliente(cliente):

            pass

    class OrdemCompra:

        @staticmethod
        def preco_medio_item_ordem_compra(ean):
            print(
                CorFonte.fonte_amarela()
                + "class Buscadores.OrdemCompra | metodo atualizar_saldo_ordem_compra"
                + CorFonte.reset_cor())
            query = f"select avg(preco) from ordem_compra where ean = %s "
            valores = ean
            mydb.connect()
            mycursor.execute(query, valores)
            mycursor.fetchall()
            mydb.commit()
            mydb.close()

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
                    print('return False')
                    return False
                else:
                    print('return True')
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

            if data_inicial is not None and data_inicial is not '':

                query += " AND DATA >= %s"
                data_inicial = data_inicial.strftime('%Y-%m-%d')
                parametros.append(data_inicial)
                print(f'data_inicial = {data_inicial}')
            else:
                pass

            if data_final is not None and data_final is not '':
                query += " AND DATA <= %s"
                data_final = data_final.strftime('%Y-%m-%d')
                parametros.append(data_final)
                print(f'data_final = {data_final}')

            if ordem_compra is not None and ordem_compra is not '':
                query += " AND ORDEM_COMPRA = %s"
                parametros.append(ordem_compra)

            if ean is not None and ean is not '':
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


class Pricing:
    print(
        CorFonte.fonte_amarela()
        + "class Pricing"  + CorFonte.reset_cor())

    @staticmethod
    def relato_bd_precificacao(ean):
        logging.info(CorFonte.fonte_amarela() + "class Pricing | metodo precificacao" + CorFonte.reset_cor())
        try:
            query = (f"SELECT * FROM PRECIFICACAO WHERE 1=1 and "
                     f"ean like '%{ean}%'")

            logging.debug(query)
            mydb.connect()
            mycursor.execute(query)
            myresult = mycursor.fetchall()
            mydb.commit()
            mydb.close()
            return myresult

        except Exception as e:
            logging.error(e)
            # AlertaMsg.cadastro_inexistente()
            pass


    @staticmethod
    def relato_custos(ean, fornecedor, unidade, descricao):
        logging.info(
            CorFonte.fonte_amarela()
            + "class Pricing | metodo custos" + CorFonte.reset_cor())
        try:
            query = (f"SELECT * FROM PRODUTOS WHERE 1=1 and "
                     f"ean like '%{ean}%' "
                     f"and fornecedor like '%{fornecedor}%' "
                     f"and UNIDADE like '%{unidade}%' "
                     f"and DESCRICAO like '%{descricao}%';")

            logging.debug(query)
            mydb.connect()
            mycursor.execute(query)
            myresult = mycursor.fetchall()
            mydb.commit()
            mydb.close()
            return myresult

        except Exception as e:
            logging.error(e)
            # AlertaMsg.cadastro_inexistente()
            pass


    @staticmethod
    def salvar_precificacao(relatorio_precificacao,usuario):
            logging.info('class Pricing, método salvar_precificacao')
            for i in relatorio_precificacao:
                data_hoje = date.strftime(data, '%Y-%m-%d')
                ean = i[3]
                preco = i[7]
                margem = i[9]
                custos = i[10]
                acrescimo = i[11]
                desconto = i[12]
                preco_venda = i[13]
                usuario = usuario

                # incluir instrução if ean já constar no bd, update
                try:
                    logging.info('Dentro do try salvar_precificacao')
                    query = (f"INSERT INTO PRECIFICACAO(DATA,"
                             f" EAN, VALOR, MARGEM, CUSTOS, ACRESCIMO, DESCONTO, PRECOVENDA, USUARIO) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);")
                    query ="""INSERT INTO PRECIFICACAO (DATA, EAN, VALOR, MARGEM, CUSTOS, ACRESCIMO, DESCONTO, PRECOVENDA, USUARIO) VALUES 
                    (%s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE 
                    DATA = VALUES(DATA),
                    VALOR = VALUES(VALOR),
                    MARGEM = VALUES(MARGEM),
                    CUSTOS = VALUES(CUSTOS),
                    ACRESCIMO = VALUES(ACRESCIMO),
                    DESCONTO = VALUES(DESCONTO),
                    PRECOVENDA = VALUES(PRECOVENDA),
                    USUARIO = VALUES(USUARIO);"""
                    logging.info(query)
                    valores = (data_hoje, ean, preco, margem, custos, acrescimo, desconto, preco_venda, usuario)
                    mydb.connect()
                    mycursor.execute(query, valores)
                    mycursor.fetchall()
                    mydb.commit()
                    mydb.close()

                except Exception as e:
                    logging.error(e)
                    pass
