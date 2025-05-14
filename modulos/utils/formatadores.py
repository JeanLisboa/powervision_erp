from modulos.utils.console import CorFonte
import os
from datetime import date

import xml.etree.ElementTree as ET
pasta_xml = r"C:\relato\XML\ANTIGOS" # utilizado pelo modulo logistica / entrada de ordem compra

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
