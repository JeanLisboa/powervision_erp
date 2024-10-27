from datetime import date
import mysql.connector
from pycpfcnpj import cpfcnpj as validador_cnpj
from flask import session, redirect, url_for, request
import xml.etree.ElementTree as ET
import openpyxl
import os

import forms
# import modulos.admin

pasta_xml = r'C:\relato\XML\ANTIGOS'


def acesso_db():
    mydb = mysql.connector.connect(
        host="localhost",
        user="admin2024",
        password="204619",
        database="projeto_erp"
    )
    connect = mydb.connect()
    mycursor = mydb.cursor()
    return mydb, mycursor, connect
mydb, mycursor, connect = acesso_db()


class CorFonte:

    @staticmethod
    def fonte_vermelha():
        return '\033[31m'

    @staticmethod
    def fonte_verde():
        return '\033[92m'

    @staticmethod
    def fonte_amarela():
        return '\033[93m'

    @staticmethod
    def fonte_azul():
        return '\033[34m'

    @staticmethod
    def fonte_azul_claro():
        return '\033[36m'

    @staticmethod
    def reset_cor():
        return '\033[0m'


class AlertaMsg:
    def __init__(self):
        self.cnpj_invalido = self.cnpj_invalido
        self.cnpj_ja_existente = self.cnpj_ja_existente
        self.cad_fornecedor_realizado = self.cad_fornecedor_realizado

    @staticmethod
    def produto_ja_cadastrado(ean):
        session['alert'] = (f'<div id = "alert" class="alert alert-danger", '
                            f'role="alert">PRODUTO JÁ CADASTRADO EAN {ean}</div>')
        return redirect(url_for('cadastrar_produtos'))

    @staticmethod
    def produto_incluido_na_tabela(ean, descricao):
        session['alert'] = (f'<div id = "alert" class="alert alert-success", '
                            f'role="alert">PRODUTO INCLUIDO NA TABELA: EAN {ean} | {descricao}</div>')
        return redirect(url_for('cadastrar_produtos'))

    @staticmethod
    def produto_ja_digitado():
        session['alert'] = f'<div id = "alert" class="alert alert-danger", role="alert">PRODUTO JÁ DIGITADO</div>'
        return redirect(url_for('cadastrar_produtos'))

    @staticmethod
    def campos_em_branco():
        session['alert'] = (f'<div id = "alert" class="alert alert-danger", '
                            f'role="alert">TODOS OS CAMPOS DEVEM SER PREENCHIDOS</div>')
        return redirect(url_for('cadastrar_produtos'))

    @staticmethod
    def ean_ja_digitado(ean):
        session['alert'] = (f'<div id = "alert" class="alert alert-danger", '
                            f'role="alert">EAN {ean} JÁ CONSTA NA TABELA DE ITENS A CADASTRAR</div>')
        return redirect(url_for('cadastrar_produtos'))

    @staticmethod
    def produto_cadastrado_com_sucesso():
        session['alert'] = \
            ('<div id = "alert" class="alert alert-success", '
             'role="alert">PRODUTO CADASTRADO COM SUCESSO</div>')
        return redirect(url_for('cadastrar_produtos'))

    @staticmethod
    def fornecedor_invalido_cad_prod():
        session['alert'] = ('<div id="alert" class="alert alert-danger" '
                            'role="alert">INSIRA UM FORNECEDOR VÁLIDO</div>')
        return redirect(url_for('cadastrar_produtos'))

    @staticmethod
    def cad_fornecedor_realizado():
        session['alert'] \
            = '<div id="alert" class="alert alert-success", role="alert">CADASTRO REALIZADO!</div>'
        return redirect(url_for('cadastrar_fornecedores'))
    @staticmethod
    def fornecedor_invalido():
        session['alert'] = '<div id="alert" class="alert alert-danger" role="alert">INSIRA UM FORNECEDOR VÁLIDO</div>'
        return redirect(url_for('cadastrar_fornecedores'))


    @staticmethod
    def cnpj_invalido():
        session['alert'] = \
            '<div id = "alert" class="alert alert-danger" role="alert">CNPJ INVALIDO!</div>'
        return redirect(url_for('cadastrar_fornecedores'))

    @staticmethod
    def cnpj_ja_existente():
        session['alert'] = \
            '<div id = "alert" class="alert alert-danger" role="alert">CNPJ JA EXISTENTE!</div>'
        return redirect(url_for('cadastrar_fornecedores'))

    @staticmethod
    def cadastro_inexistente():
        session['alert'] = \
            '<div id = "alert" class="alert alert-danger" role="alert">CADASTRO INEXISTENTE</div>'
        return redirect(url_for('gerar_ordem_de_compra'))


class Formatadores:

    @staticmethod
    def formatar_xml(nome_arquivo):
        print('Método formatar_xml\n'
              'Recebe a chave da nf e \n'
              'retorna ean, quantidade, preco unitário e total do item')

        # Definir namespace
        lista_itens_nf_nova = ''
        namespace = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
        xml_filename = f'{nome_arquivo}.xml' # Definir o caminho da pasta onde o arquivo XML está localizado
        xml_path = os.path.join(pasta_xml, xml_filename)
        if not os.path.isfile(xml_path): # Verificar se o arquivo existe
            print(f"Arquivo {xml_path} não encontrado.")
        else:
            try:
                tree = ET.parse(xml_path) # Carregar e analisar o arquivo XML
                root = tree.getroot()
                ide = root.find('.//nfe:ide', namespace) # Acessar informações gerais da nota fiscal
                emit = root.find('.//nfe:emit', namespace)
                dest = root.find('.//nfe:dest', namespace)
                nf_info = {
                    'UF': ide.find('nfe:cUF', namespace).text,
                    'Número NF': ide.find('nfe:nNF', namespace).text,
                    'Data de Emissão': ide.find('nfe:dhEmi', namespace).text,
                    'Emitente': {
                        'CNPJ': emit.find('nfe:CNPJ', namespace).text,
                        'Nome': emit.find('nfe:xNome', namespace).text
                    },
                    'Destinatário': {
                        'CNPJ': dest.find('nfe:CNPJ', namespace).text,
                        'Nome': dest.find('nfe:xNome', namespace).text
                    },
                    'Produtos': []
                }

                produto_info = []
                for det in root.findall('.//nfe:det', namespace):  # Extrair todos os produtos
                    prod = det.find('nfe:prod', namespace)
                    produto_info = {
                        'Ean': prod.find('nfe:cEANTrib', namespace).text,
                        # 'Código': prod.find('nfe:cProd', namespace).text,
                        # 'Descrição': prod.find('nfe:xProd', namespace).text,
                        'Quantidade': int(float(prod.find('nfe:qCom', namespace).text)),
                        'Valor Unitário': int(float(prod.find('nfe:vUnCom', namespace).text)),
                        'Valor Total': int(float(prod.find('nfe:vProd', namespace).text))
                    }
                    nf_info['Produtos'].append(produto_info)

                lista_itens_nf = []
                lista_itens_nf_temp = []
                lista_itens_nf_nova = []
                lista_itens_nf_temp_nova = []

                for key, value in nf_info.items():  # Imprimir as informações extraídas
                    if isinstance(value, list):
                        for item in value:  # cada 'item' é uma linha contendo todos os campos de 'produto_info'
                            item = dict(item)
                            lista_itens_nf_temp.append(item)
                            lista_itens_nf.append(lista_itens_nf_temp[:])
                            lista_itens_nf_temp.clear()
                        for lista_in_dict in lista_itens_nf:
                            for i in lista_in_dict:
                                lista_itens_nf_temp_nova.append(i['Ean'])
                                lista_itens_nf_temp_nova.append(i['Quantidade'])
                                lista_itens_nf_temp_nova.append(i['Valor Unitário'])
                                lista_itens_nf_temp_nova.append(i['Valor Total'])
                                lista_itens_nf_nova.append(lista_itens_nf_temp_nova[:])
                                lista_itens_nf_temp_nova.clear()
                        print('lista_itens_nf_nova >> finalizada')

            except ET.ParseError as e:
                print(f"Erro ao analisar o arquivo XML: {e}")
            except AttributeError as e:
                print(f"Erro ao acessar elementos no XML: {e}")

        return lista_itens_nf_nova

    @staticmethod
    def formatar_data(data):
        return data.strftime('%d/%m/%Y')

    @staticmethod
    def data_formato_db(data):
        return data.strftime('%Y-%m-%d')

    @staticmethod
    def os_data():
        agora = date.today()
        return agora


class ValidaStatusPedido:
    @staticmethod
    def validacao_1(status_ordem):
        print('class ValidaStatusPedido | metodo validacao_1\n'
              'Objetivo: Verificar se o xml está no servidor')

        if status_ordem is True:
            return True
        else:  # xml nao localizado
            return False

    @staticmethod
    def validacao_2(cnpj):
        print('class ValidaStatusPedido | metodo validacao_2\n'
              'Objetivo: Verificar se o fornecedor está cadastrado')
        # print(fonte_amarela + '\nVALIDAÇÃO 2: VERIFICAR SE O FORNECEDOR ESTÁ CADASTRADO' + reset_cor)
        if Buscadores.buscar_cnpj(cnpj) is True:
            print(CorFonte.fonte_azul() + f'cnpj encontrado: {cnpj}' + CorFonte.reset_cor())
            # print(fonte_verde + 'VALIDAÇÃO 2 concluída' + reset_cor)
            return True
        else:
            print('cnpj não encontrado')
            # lst_nf = ['Fornecedor não encontrado']
            return False

    @staticmethod
    def validacao_3(status_ordem, ordem):
        print('class ValidaStatusPedido | metodo validacao_3\n'
              'Objetivo: Verificar se o pedido está aberto')
        # print(fonte_amarela + '\nVALIDÇÃO 3: VERIFICAR SE O PEDIDO ESTÁ EM ABERTO' + reset_cor)
        if status_ordem is True:
            # print(CorFonte.fonte_azul() + f'Pedido {ordem} aberto' + CorFonte.fonte_azul())
            # print(fonte_verde + 'VALIDAÇÃO 3 concluída' + reset_cor)
            return True
        else:
            print(CorFonte.fonte_vermelha() + 'Pedido encerrado ou cancelado' + CorFonte.reset_cor())
            return False

    @staticmethod
    def validacao_4(nf,ordem):
        print('class ValidaStatusPedido | metodo validacao_4\n'
              'Objetivo: Verificar ordem x nf')
        # print(fonte_amarela + '\nVALIDAÇÃO 4: VALIDAR PEDIDO X NF' + reset_cor)
        itens_nf = Buscadores.Xml.buscar_linhas_nf(str(nf))
        # print(f'itens_nf = {itens_nf}\n')
        # print(fonte_amarela + '\nVALIDAÇÃO 4: (2) RECEBER OC, CRIAR LISTA DE EAN E PRECO' + reset_cor)
        itens_oc = Validadores.valida_pedido_recebido(ordem)
        # print(f'itens_oc = {itens_oc}\n')
        # print(fonte_amarela + '\nVALIDAÇÃO 4: (3) COMPARAR AS DUAS LISTAS' + reset_cor)
        # maior_dif_permitida = modulos.admin.maior_dif_permitida
        maior_dif_permitida = 0.2
        # print(f'maior_dif_permitida = {maior_dif_permitida}\n')
        cont_preco_fora_politica = 0

        # print('for ean_oc in itens_oc:')
        for ean_oc in itens_oc:  # 'oc' = 'ordem de compra'
            # print(f'\nean pesquisado: {ean_oc[0]}')

            for ean_nf in itens_nf:
                # print(f'ean_nf = {ean_nf[0]}')
                if ean_oc[0] == ean_nf[0]:
                    # print(CorFonte.fonte_azul() + f'ean_oc[0] = {ean_oc[0]} || ean_oc[1] = {ean_oc[1]}\n'
                    #                    f'ean_nf[0] = {ean_nf[0]} || ean_nf[1] = {ean_nf[1]}' + CorFonte.reset_cor())
                    if (ean_oc[1] - ean_nf[1]) <= maior_dif_permitida:
                        print(CorFonte.fonte_verde() + f'preco dentro da politica' + CorFonte.reset_cor())
                    else:
                        print(CorFonte.fonte_vermelha() + f'preco fora da politica' + CorFonte.reset_cor())
                        cont_preco_fora_politica += 1

        if cont_preco_fora_politica == 0:
            return True
        else:
            return False

class Validadores:


    @staticmethod
    def valida_pedido_recebido(pedido):
        lista_itens = []
        # 1 faz a query no banco de dados e retorna uma lista com os itens do pedido
        print('class Validadores | método valida_nf_recebida')
        query = f"SELECT * FROM ORDEM_COMPRA WHERE ORDEM_COMPRA  = '{pedido}'"
        mydb.connect()
        mycursor.execute(query)
        itens_ordem_de_compra = mycursor.fetchall()
        mydb.commit()
        valida_itens = ''

        try:
            if itens_ordem_de_compra:
                # print('chama função lista_itens_de_compra...'
                #       'esta função serve para criar uma lista '
                #       'e comparar com as linhas do xml, afim '
                #       'de validar os itens de acordo com a política')

                for i in itens_ordem_de_compra:
                    item_zip = (i[7], i[9])
                    lista_itens.append(item_zip)

            return lista_itens
        except Exception as e:
            print(f'Erro: {e}')
            return False

    @staticmethod
    def valida_status_pedido(pedido):
        lista_itens = []
        # 1 faz a query no banco de dados e retorna uma lista com os itens do pedido
        print('class Validadores | método valida_status_pedido')
        query = f"SELECT * FROM ORDEM_COMPRA WHERE ORDEM_COMPRA  = '{pedido}'"
        mydb.connect()
        mycursor.execute(query)
        itens_ordem_de_compra = mycursor.fetchall()
        mydb.commit()
        valida_itens = ''
        for i in itens_ordem_de_compra:
            print(i)
        print('-------------------------------')
        try:
            return itens_ordem_de_compra
        except Exception as e:
            print(f'Erro: {e}')
            return False

    ordem_compra = ''


    @staticmethod
    def valida_cnpj(cnpj):
        print('class Validadores | método valida_cnpj')
        print(f'cnpj original {cnpj}')
        cnpj = (str(cnpj))
        print(f'cnpj convertido {cnpj}')
        return validador_cnpj.validate(cnpj)

    @staticmethod
    def valida_inscricao_estadual(insc_estadual):
        print('class Validadores | método valida_inscricao_estadual')
        insc_estadual = (str(insc_estadual))
        if len(insc_estadual) != 9:
            return False
        else:
            return True


class AtualizaCodigo:
    @staticmethod
    def cod_produto():
        print('class AtualizaCodigo | metodo cod_produto')
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
                max_codigo = '00000' + max_codigo
            if len(max_codigo) == 2:
                max_codigo = '0000' + max_codigo
            if len(max_codigo) == 3:
                max_codigo = '000' + max_codigo
            if len(max_codigo) == 4:
                max_codigo = '00' + max_codigo
            if len(max_codigo) == 5:
                max_codigo = '0' + max_codigo
            return max_codigo
        except:
            max_codigo = '000001'
            return max_codigo

    @staticmethod
    def cod_fornecedor():
        print('class AtualizaCodigo | metodo cod_fornecedor')
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
                max_codigo = '00000' + max_codigo
            if len(max_codigo) == 2:
                max_codigo = '0000' + max_codigo
            if len(max_codigo) == 3:
                max_codigo = '000' + max_codigo
            if len(max_codigo) == 4:
                max_codigo = '00' + max_codigo
            if len(max_codigo) == 5:
                max_codigo = '0' + max_codigo
            return max_codigo
        except:
            max_codigo = '000001'
            return max_codigo

    @staticmethod
    def ordem_compra():
        print('class AtualizaCodigo | metodo ordem_compra')
        try:
            query = "SELECT MAX(ORDEM_COMPRA) FROM ordem_compra"
            mydb.connect()
            mycursor.execute(query)
            myresult = mycursor.fetchall()
            mydb.commit()
            ordem_compra_atual = 0
            for x in myresult:
                ordem_compra_atual = x[0]
            ordem_compra_atual = int(ordem_compra_atual)
            ordem_compra_atual = ordem_compra_atual + 1
            ordem_compra_atual = str(ordem_compra_atual)
            if len(ordem_compra_atual) == 1:
                ordem_compra_atual = '00000' + ordem_compra_atual
            if len(ordem_compra_atual) == 2:
                ordem_compra_atual = '0000' + ordem_compra_atual
            if len(ordem_compra_atual) == 3:
                ordem_compra_atual = '000' + ordem_compra_atual
            if len(ordem_compra_atual) == 4:
                ordem_compra_atual = '00' + ordem_compra_atual
            if len(ordem_compra_atual) == 5:
                ordem_compra_atual = '0' + ordem_compra_atual
            return ordem_compra_atual
        except Exception as e:
            print(e)
            ordem_compra_atual = '000001'
            return


class Buscadores:
    def __init__(self):
        pass

    def buscar_cnpj(cnpj):
        print('class Buscadores | metodo buscar_cnpj')
        mydb.connect()
        query = f"SELECT * FROM fornecedores WHERE CNPJ = '{cnpj}'"
        mycursor.execute(query)
        myresult = mycursor.fetchall()

        if len(myresult) == 0:
            return False
        else:
            return True
    class Xml:
        chave_nf = ''
        nome_arquivo =''
        pasta_xml = r'C:\relato\XML\ANTIGOS'


        @staticmethod
        def retorna_xml(nf):
            print('----------------------------------------------')
            print('class Buscadores.Xml | metodo retorna_xml')
            print('Recebe a NF e retorna o caminho do XML')
            pasta_xml = r'C:\relato\XML\ANTIGOS'
            namespaces = {'ns1': 'http://www.portalfiscal.inf.br/nfe'}
            arquivo_encontrado = None
            lst_zipada = []

            for arquivo in os.listdir(pasta_xml):  # Procura pelo arquivo na pasta especificada
                if nf in arquivo[26:34] and arquivo.endswith('-nfe.xml'):
                    arquivo_encontrado = os.path.join(pasta_xml, arquivo)
                    print(f'arquivo encontrado >> {arquivo_encontrado}')
                    # print('----------------------------------------------')
            return arquivo_encontrado[22:-4]

        @staticmethod
        def buscar_linhas_nf(nf):
            print('----------------------------------------------')
            print('class Buscadores.Xml | metodo buscar_linhas_nf')
            pasta_xml = r'C:\relato\XML\ANTIGOS'
            namespaces = {'ns1': 'http://www.portalfiscal.inf.br/nfe'}
            arquivo_encontrado = None
            lst_zipada = []

            for arquivo in os.listdir(pasta_xml): # Procura pelo arquivo na pasta especificada
                if nf in arquivo[26:34] and arquivo.endswith('-nfe.xml'):
                    arquivo_encontrado = os.path.join(pasta_xml, arquivo)
                    print(f'arquivo encontrado >> {arquivo_encontrado}')
                    break

            if arquivo_encontrado:  # Verifica se o arquivo foi encontrado
                xNome4 = ''
                lst_produto = []
                lst_ean = []
                lst_icms = []
                lst_val_compra = []
                tree = ET.parse(arquivo_encontrado)
                root = tree.getroot()
                for det in root.findall('.//ns1:det', namespaces):
                    # xNome4 = det.find('.//ns1:xNome4', namespaces)
                    cProd = det.find('.//ns1:cProd', namespaces)
                    cEAN = det.find('.//ns1:cEANTrib', namespaces)
                    pICMS = det.find('.//ns1:pICMS', namespaces)
                    vUnCom = det.find('.//ns1:vUnCom', namespaces)
                    vUnCom.text = vUnCom.text.replace('.', ',')
                    vUnCom.text = vUnCom.text.replace(',', '.')
                    vUnCom.text = vUnCom.text.replace(' ', '')
                    vUnCom.text = vUnCom.text.rstrip('0')
                    item_zip = (cEAN.text, float(vUnCom.text))
                    lst_zipada.append(item_zip)
            else:
                print('Arquivo não encontrado')
                return None
            print('----------------------------------------------')
            return lst_zipada

        @staticmethod
        def buscar_arquivo(nf):
            print('----------------------------------------------')
            print('class Buscadores.Xml | metodo buscar_arquivo')
            nf = str(nf)
            for nome_arquivo in os.listdir(pasta_xml):
                i = nome_arquivo
                i = i[25:34]  # pegar apenas o num da nf
                i = i.lstrip('0')# tirar zeros a esquerda
                if i == nf:
                    print(f'NFO {i}/{nf} localizada na pasta')
                    print('----------------------------------------------')
                    return nome_arquivo

        @staticmethod
        def buscar_colunas_xml(nome_arquivo):
            print('class Buscadores.Xml | metodo buscar_colunas_xml')
            nome_arquivo = f'{pasta_xml}/{nome_arquivo}'

            def extrair_tags(element, prefix=''):
                tags = set()
                for child in element:
                    tag_name = f"{prefix}/{child.tag.split('}')[-1]}"
                    print('tag_name >>>', tag_name)
                    tags.add(tag_name)
                    tags.update(extrair_tags(child, tag_name))
                return tags

            try:
                tree = ET.parse(nome_arquivo) # Parse do XML
                root_element = tree.getroot()
                colunas = extrair_tags(root_element) # Extrair todas as tags
                print(f'Colunas encontradas: {colunas}')
                return colunas

            except ET.ParseError:
                print(f"Erro ao analisar o arquivo: {nome_arquivo}")
                return None

        @staticmethod
        def buscar_cnpj(nome_arquivo):
            print('class Buscadores.Xml | metodo buscar_cnpj')
            nome_arquivo = f'{pasta_xml}/{nome_arquivo}'
            try:
                tree = ET.parse(nome_arquivo) # Parse do XML
                root_element = tree.getroot()
                # Obter namespace
                namespaces = {node[0]: node[1] for _, node in ET.iterparse(nome_arquivo, events=['start-ns'])}
                # Buscar o elemento CNPJ específico
                cnpj_element = root_element.find(
                    './/{http://www.portalfiscal.inf.br/nfe}CNPJ',namespaces)

                # USE O CODIGO ABAIXO PARA EXTRAIR O CNPJ DO DESTINATÁRIO
                # cnpj_element = root_element.find(
                #     './/{http://www.portalfiscal.inf.br/nfe}NFe/'
                #     '{http://www.portalfiscal.inf.br/nfe}infNFe/'
                #     '{http://www.portalfiscal.inf.br/nfe}dest/'
                #     '{http://www.portalfiscal.inf.br/nfe}CNPJ',
                #     namespaces)

                if cnpj_element is not None:
                    cnpj = cnpj_element.text
                    print(f' CNPJ: {cnpj}')
                    return cnpj
                else:
                    print('CNPJ não encontrado')
                    return None

            except ET.ParseError:
                print(f"Erro ao analisar o arquivo: {nome_arquivo}")
                return None

        @staticmethod
        def buscar_pedido(nome_arquivo):
            print('class Buscadores.Xml | metodo buscar_pedido')
            nome_arquivo = f'{pasta_xml}/{nome_arquivo}'
            try:
                tree = ET.parse(nome_arquivo) # Parse do XML
                root_element = tree.getroot()
                namespaces = {node[0]: node[1] for _, node in ET.iterparse(nome_arquivo, events=['start-ns'])}
                # Buscar o elemento xPed específico
                xped_element = root_element.find('.//{http://www.portalfiscal.inf.br/nfe}xPed', namespaces)
                if xped_element is not None:
                    pedido = xped_element.text
                    return pedido
                else:
                    print('Ordem de Compra não encontrada com namespace')

                xped_element_no_ns = root_element.find('.//xPed') # Buscar o elemento xPed específico sem considerar namespace

                if xped_element_no_ns is not None:
                    print(f'xPed encontrado sem namespace: {xped_element_no_ns.text}')
                    return xped_element_no_ns.text
                else:
                    print('xPed não encontrado sem namespace')

                return None

            except ET.ParseError:
                print(f"Erro ao analisar o arquivo: {nome_arquivo}")
                return None

        @staticmethod
        def buscar_razao_social(nome_arquivo):
            print('class Buscadores.Xml | metodo buscar_razao_social')
            nome_arquivo = f'{pasta_xml}/{nome_arquivo}'
            try:
                tree = ET.parse(nome_arquivo)  # Parse do XML
                root_element = tree.getroot()
                namespaces = {node[0]: node[1] for _, node in ET.iterparse(nome_arquivo, events=['start-ns'])}
                # Buscar o elemento CNPJ específico
                razao_social = root_element.find('.//{http://www.portalfiscal.inf.br/nfe}xNome', namespaces)
                # USE O CODIGO ABAIXO PARA EXTRAIR A RAZAO SOCIAL DO DESTINATÁRIO
                # razao_social = root_element.find('.//{http://www.portalfiscal.inf.br/nfe}NFe/'
                #                                  '{http://www.portalfiscal.inf.br/nfe}infNFe/'
                #                                  '{http://www.portalfiscal.inf.br/nfe}dest/'
                #                                  '{http://www.portalfiscal.inf.br/nfe}xNome', namespaces)
                if razao_social is not None:
                    razao_social_ = razao_social.text
                    print(f'RAZAO SOCIAL: {razao_social_}')
                    return razao_social_
                else:
                    print('RAZAO SOCIAL não encontrado')
                    return None
            except ET.ParseError:
                print(f"Erro ao analisar o arquivo: {nome_arquivo}")
                return None

    class OrdemCompra:
        @staticmethod
        def atualizar_saldo_ordem_compra(ordem_compra):
            print(f'class Buscadores.OrdemCompra | metodo atualizar_saldo_ordem_compra | {ordem_compra}')

        @staticmethod
        def atualizar_status_ordem_compra(ordem_compra):
            print(f'class Buscadores.OrdemCompra | metodo atualizar_status_ordem_compra | {ordem_compra}')

            # recebe a conferencia da ordem de compra
            # se todos os itens ok: status = pedido liquidado
            # caso contrário: status = recebido parcialmente

        @staticmethod
        def verifica_status_ordem(ordem_compra):
            print('class Buscadores.OrdemCompra | metodo verifica_status_ordem')
            print(f'Verifica status_ordem_compra: {ordem_compra}')
            query = (f'SELECT SUM(SALDO_QTD) FROM ORDEM_COMPRA WHERE ORDEM_COMPRA = "{ordem_compra}";')
            mydb.connect()
            mycursor.execute(query)
            resultado = mycursor.fetchall()
            mydb.commit()
            mydb.close()
            i = 0
            for i in resultado:
                # print(i[0])
                if i[0] > 0:
                    return True
                else:
                    return False

        @staticmethod
        def buscar_nf2(nf):
            print('class Buscadores.OrdemCompra | metodo buscar_nf2')
            nf = str(nf)
            cnpj_encontrado = []

            for chave_nf in os.listdir(pasta_xml):
                i = chave_nf
                i = i[25:34]  # pegar apenas o num da nf
                i = i.lstrip('0')# tirar zeros a esquerda
                if i == nf:
                    print(f'nfo {i}/{nf} localizada na pasta')
                    print(chave_nf)
                    for root, dirs, files in os.walk(pasta_xml):
                        for file in files:
                            caminho_arquivo = os.path.join(root, file)
                            if file.endswith('.xml'):
                                if file == chave_nf:
                                    print(f'Arquivo encontrado nf >> {nf} | chave >> {chave_nf} | caminho >>> {caminho_arquivo}')
                                    tree = ET.parse(caminho_arquivo)  ##
                                    print(f'tree >>> {tree}')
                                    root_element = tree.getroot()
                                    namespaces = {'ns1': root_element.tag.split('}')[0].strip('{')}
                                    for det in root_element.findall('.//ns1:det', namespaces):
                                        cnpj = det.find('.//ns1:CNPJ3', namespaces)
                                        razao_social = det.find('.//ns1:xNome4', namespaces)
                                        print(f'cnpj det >>> {cnpj}')
                                        print(f'razao_social >>> {razao_social}')
                                    break

                    return cnpj_encontrado
        chave_nf = ''

        def buscar_nf(pasta_xml, chave_nf, nf):
            cnpjs_encontrados = []
            nf = str(nf)
            # Definir o caminho da pasta onde o arquivo XML está localizado
            for chave_nf in os.listdir(pasta_xml):
                i = chave_nf
                i = i[25:34]  # pegar apenas o num da nf
                i = i.lstrip('0')# tirar zeros a esquerda
                if i == nf:
                    print(f'nfo {i}/{nf} localizada na pasta')
                    print(chave_nf)

            # Navegar pela pasta
            for root, dirs, files in os.walk(pasta_xml):
                for file in files:
                    if file.endswith('.xml'):
                        caminho_arquivo = os.path.join(root, file)
                        if file == chave_nf:
                            try:
                                tree = ET.parse(caminho_arquivo)
                                root_element = tree.getroot()
                                # Para ver o conteúdo do XML (opcional)
                                xml_string = ET.tostring(root_element, encoding='utf-8').decode('utf-8')
                                # print(f'Conteúdo do XML:\n{xml_string}')

                                # Obter namespace
                                namespaces = {'ns1': root_element.tag.split('}')[0].strip('{')}

                                # Buscar elementos com namespace
                                for det in root_element.findall('.//ns1:det', namespaces):
                                    cnpj_element = det.find('.//ns1:CNPJ', namespaces)
                                    razao_social_element = det.find('.//ns1:xNome', namespaces)

                                    if cnpj_element is not None:
                                        cnpj = cnpj_element.text
                                        print(f'CNPJ: {cnpj}')
                                    else:
                                        print('CNPJ não encontrado')

                                    if razao_social_element is not None:
                                        razao_social = razao_social_element.text
                                        print(f'Razão Social: {razao_social}')
                                    else:
                                        print('Razão Social não encontrada')

                                    cnpjs_encontrados.append((file, cnpj, razao_social))
                            except ET.ParseError:
                                print(f"Erro ao analisar o arquivo: {caminho_arquivo}")

            return cnpjs_encontrados, chave_nf

        @staticmethod
        def buscar_ordem_compra2(ordem_compra, razaosocial):
            print('class Buscadores.OrdemCompra | metodo buscar_ordem_compra2')
            query = ''
            try:
                if ordem_compra == '':
                    query = (f'SELECT '
                             f'ORDEM_COMPRA.DATA, '
                             f'ORDEM_COMPRA.CODIGO, '
                             f'FORNECEDORES.RAZAOSOCIAL, '
                             f'ORDEM_COMPRA.ORDEM_COMPRA, '
                             f'ORDEM_COMPRA.TOTAL_ITEM '
                             f'FROM ORDEM_COMPRA '
                             f'INNER JOIN FORNECEDORES '
                             f'ON ORDEM_COMPRA.CODIGO = FORNECEDORES.CODIGO '
                             f'WHERE RAZAOSOCIAL like "%{razaosocial}%";')
                if razaosocial == '':
                    query = (f'SELECT '
                             f'ORDEM_COMPRA.DATA, '
                             f'ORDEM_COMPRA.CODIGO, '
                             f'PRODUTOS.FORNECEDOR, '
                             f'ORDEM_COMPRA.ORDEM_COMPRA, '
                             f'ORDEM_COMPRA.TOTAL_ITEM '
                             f'FROM ORDEM_COMPRA '
                             f'INNER JOIN PRODUTOS '
                             f'ON ORDEM_COMPRA.DESCRICAO = PRODUTOS.DESCRICAO '
                             f'WHERE ORDEM_COMPRA like "%{ordem_compra}%" '
                             f'ORDER BY ORDEM_COMPRA DESC;')

                else:
                    query = (f'SELECT '
                             f'ORDEM_COMPRA.DATA, '
                             f'ORDEM_COMPRA.CODIGO, '
                             f'PRODUTOS.FORNECEDOR, '
                             f'ORDEM_COMPRA.ORDEM_COMPRA, '
                             f'ORDEM_COMPRA.TOTAL_ITEM '
                             f'FROM ORDEM_COMPRA '
                             f'INNER JOIN PRODUTOS '
                             f'ON ORDEM_COMPRA.DESCRICAO = PRODUTOS.DESCRICAO '
                             f'WHERE ORDEM_COMPRA like "%{ordem_compra}%" AND FORNECEDOR like "%{razaosocial}%" '
                             f'ORDER BY ORDEM_COMPRA DESC;')

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
            print('Buscadores.OrdemCompra.buscar_ordem_compra()')
            try:
                query = f'select * from ordem_compra where ordem_compra = {ordem_compra}'
                print(query)
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
            print('Buscadores.OrdemCompra.buscar_ordem_compra_pela_razaosocial()')
            try:
                query = f'select * from ordem_compra where FORNECEDOR like "%{razaosocial}%"'
                print(query)
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
            print('Buscadores.OrdemCompra.preco_medio()')
            try:
                query = f'select avg(preco) from ordem_compra where codigo = {codigo}'
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
            try:
                query = f'select preco from ordem_compra where codigo = {codigo} order by ordem_compra desc limit 1;'
                mydb.connect()
                mycursor.execute(query)
                myresult = mycursor.fetchall()
                mydb.commit()
                mydb.close()
                print(myresult)

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
                myresult = ''
                return myresult

        @staticmethod
        def buscar_pelo_fornecedor(fornecedor):
            print('função pesquisar pelo fornecedor')
            try:
                query = f"select * from produtos where fornecedor = '{fornecedor}' order by DESCRICAO"
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
                myresult = ''
                return myresult

    def buscar_produto_pelo_ean(ean):
        print('metodo buscar pelo ean')
        try:
            query = f'select * from produtos where ean = "{ean}"'
            mydb.connect()
            mycursor.execute(query)
            myresult = mycursor.fetchall()
            mydb.commit()
            mydb.close()
            # print(myresult)
            try:
                print(len(myresult))

                if len(myresult) > 0:
                    return False
                else:
                    return True
            except Exception as e:
                return len(myresult), e
        except Exception as e:
            return e

    def buscar_produto_pelo_codigo(self):
        print('metodo buscar pelo codigo')
        try:
            mydb.commit()
            mydb.connect()
            query = f"select * from produtos where CODIGO = {self}"

            mycursor.execute(query)
            myresult = mycursor.fetchall()
            print(f' myresult >>>> {myresult}')
            mydb.close()

            return myresult
        except:
            pass

    def buscar_produto_pela_descricao(self):
        print('metodo buscar pelo descricao')
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

    @staticmethod
    def mostrar_tabela_produtos():
        mydb.connect()
        query = 'select * from produtos'

        mycursor.execute(query)
        myresult = mycursor.fetchall()
        return myresult

    @staticmethod
    def buscar_nf_pelo_cnpj(cnpj):

        nfs_encontradas = []
        print('metodo buscar nf pelo cnpj')
        print(f'buscar pelo cnpj >> {cnpj}')


        for root, dirs, files in os.walk(pasta_xml):
            for file in files:
                if file.endswith('.xml'):
                    caminho_arquivo = os.path.join(root, file)
                    try:
                        tree = ET.parse(caminho_arquivo)
                        root_element = tree.getroot()

                        # Ajuste o nome da tag conforme necessário
                        cnpj_element = root_element.find('.//CNPJ')
                        if cnpj_element is not None:
                            nfs_encontradas.append((file, cnpj_element.text))
                    except ET.ParseError:
                        print(f"Erro ao analisar o arquivo: {caminho_arquivo}")


class BancoDeDados:  # queries

    @staticmethod
    def listar_produtos():
        mydb.connect()
        query = 'select * from produtos'
        mycursor.execute(query)
        myresult = mycursor.fetchall()
        return myresult

    @staticmethod
    def inserir_item_ordem_compra():
        # mydb.connect()
        # query = 'insert into ordem_compra (CODIGO, DESCRICAO, UNIDADE, CATEGORIA, EAN) values (%s, %s, %s, %s, %s)'
        # mycursor.execute(query)
        pass

    @staticmethod
    def atualizar_ordem_compra():
        print('class BancoDeDados | metodo atualizar_ordem_compra')
        pass


class Estoque:
    @staticmethod
    def entrada_estoque():
        print('class Estoque | metodo EntradaEstoque')
        pass




def download_planilha():
    pasta = r'C:\Users\jean.lino\Downloads'  # Substitua pelo caminho da sua pasta
    file_name = 'planilha.xlsx'
    file_path = os.path.join(pasta, file_name)

    # Crie a pasta se ela não existir
    os.makedirs(pasta, exist_ok=True)

    # Crie uma nova planilha
    workbook = openpyxl.Workbook()
    sheet = workbook.active

    # Adicione as colunas à planilha
    columns = ['Fornecedor', 'EAN', 'Valor','Unidade', 'Quantidade']  # Substitua pelos nomes das suas colunas
    sheet.append(columns)

    # Salve a planilha na pasta específica
    workbook.save(file_path)

    print(f'Planilha salva em: {file_path}')

    pass

