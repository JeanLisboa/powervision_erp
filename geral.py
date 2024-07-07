from datetime import date
import mysql.connector
from pycpfcnpj import cpfcnpj as validador_cnpj
from flask import session, redirect, url_for
import xml.etree.ElementTree as ET
import os
"""

CLASS Totais ???

CLASS AlertaMsg
    DEF CAD_FORNECEDOR_REALIZADO
    DEF CNPJ_INVALIDO
    DEF CNPJ_INEXISTENTE
    DEF CNPJ_JA_EXISTENTE
    DEF CADASTRO_INEXISTENTE
    
CLASS Formatadores
    DEF FORMATAR_XML
    DEF FORMATAR_DATA
    DEF DATA_FORMATO_DB
    DEF OS_DATA
    DEF FORMATAR_XML
    
CLASS Validadores
    DEF VALIDA_CNPJ
    DEF VALIDA_INSCRICAO_ESTADUAL
    
CLASS AtualizaCodigo  - TRATA INFORMAÇÕES INCREMENTAIS
    DEF COD_PRODUTO
    DEF COD_FORNECEDOR
    DEF ORDEM_COMPRA
    DEF CONTADOR ??
    
CLASS Buscadores
    CLASS OrdemCompra
        DEF PRECO_MEDIO 
        DEF BUSCAR_NF
        DEF ANALISAR_NF  ??
        DEF VISUALIZAR_NF ??
        DEF ORDEM_COMPRA_EM_ABERTO ??
        DEF ULTIMO_PRECO
        DEF BUSCAR_FORNECEDOR
    DEF BUSCAR_PRODUTO_PELO_EAN
    DEF BUSCAR_PRODUTO_PELO_CODIGO
    DEF BUSCAR_PRODUTO_PELA_DESCRICAO
    DEF VALIDAR_EAN (EM ABERTO)
    DEF MOSTRAR_TABELA_PRODUTOS ( PARA POPUP )
    DEF BUSCAR_FORNECEDOR
    DEF BUSCAR_PRODUTO_PELO_EAN
    DEF BUSCAR_PRODUTO_PELO_CODIGO
    DEF VALIDAR_EAN
    DEF MOSTRAR_TABELA_PRODUTOS
    
       
    
            
    

         

"""


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


class AlertaMsg:
    def __init__(self):
        self.cnpj_invalido = self.cnpj_invalido
        self.cnpj_ja_existente = self.cnpj_ja_existente
        self.cad_fornecedor_realizado = self.cad_fornecedor_realizado



    @staticmethod
    def produto_ja_cadastrado(ean):
        session['alert'] = f'<div id = "alert" class="alert alert-danger", role="alert">PRODUTO JÁ CADASTRADO EAN {ean}</div>'
        return redirect(url_for('cadastrar_produtos'))
    @staticmethod
    def produto_incluido_na_tabela(ean, descricao):
        session['alert'] = f'<div id = "alert" class="alert alert-success", role="alert">PRODUTO INCLUIDO NA TABELA: EAN {ean} | {descricao}</div>'
        return redirect(url_for('cadastrar_produtos'))


    @staticmethod
    def produto_ja_digitado():
        session['alert'] = f'<div id = "alert" class="alert alert-danger", role="alert">PRODUTO JÁ DIGITADO</div>'
        return redirect(url_for('cadastrar_produtos'))
    @staticmethod
    def campos_em_branco():
        session['alert'] = f'<div id = "alert" class="alert alert-danger", role="alert">TODOS OS CAMPOS DEVEM SER PREENCHIDOS</div>'
        return redirect(url_for('cadastrar_produtos'))

    @staticmethod
    def ean_ja_digitado(ean):
        session['alert'] = f'<div id = "alert" class="alert alert-danger", role="alert">EAN {ean} JÁ CONSTA NA TABELA DE ITENS A CADASTRAR</div>'
        return redirect(url_for('cadastrar_produtos'))

    @staticmethod
    def produto_cadastrado_com_sucesso():
        session['alert'] = \
            '<div id = "alert" class="alert alert-success", role="alert">PRODUTO CADASTRADO COM SUCESSO</div>'
        return redirect(url_for('cadastrar_produtos'))

    @staticmethod
    def fornecedor_invalido_cad_prod():
        session['alert'] = '<div id="alert" class="alert alert-danger" role="alert">INSIRA UM FORNECEDOR VÁLIDO</div>'
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
        # return redirect(url_for('gerar_ordem_de_compra'))


class Formatadores:

    @staticmethod
    def formatar_xml(nf):
        # Definir namespace
        namespace = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}

        # Definir o caminho da pasta onde o arquivo XML está localizado
        xml_directory = r'C:\relato\xml'
        xml_filename = f'{nf}.xml'
        # xml_filename = '25240543587344000909550040000020511198893573-nfe.xml'
        # Criar o caminho completo para o arquivo XML

        xml_path = os.path.join(xml_directory, xml_filename)

        # Verificar se o arquivo existe
        if not os.path.isfile(xml_path):
            print(f"Arquivo {xml_path} não encontrado.")
        else:
            try:
                # Carregar e analisar o arquivo XML
                tree = ET.parse(xml_path)
                root = tree.getroot()

                # Acessar informações gerais da nota fiscal
                ide = root.find('.//nfe:ide', namespace)
                emit = root.find('.//nfe:emit', namespace)
                dest = root.find('.//nfe:dest', namespace)

                #  nf_info = {uf, nf ,dta emissao, emitente{cnpj, nome}, destinatario {cnpj, nome}, produtos[] }
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
                # Extrair todos os produtos
                for det in root.findall('.//nfe:det', namespace):
                    prod = det.find('nfe:prod', namespace)
                    produto_info = {
                        'Ean': prod.find('nfe:cEAN', namespace).text,
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

                # Imprimir as informações extraídas
                for key, value in nf_info.items():
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


class Validadores:

    @staticmethod
    def valida_item_a_cadastrar(ean):
        print(f'função_item_a_cadastrar >>> {ean}')

        return False
        pass
    @staticmethod
    def analisar_nf_pedido():
        pass

    @staticmethod
    def valida_cnpj(cnpj):
        print(f'cnpj original {cnpj}')
        cnpj = (str(cnpj))
        print(f'cnpj convertido {cnpj}')
        return validador_cnpj.validate(cnpj)

    @staticmethod
    def valida_inscricao_estadual(insc_estadual):
        insc_estadual = (str(insc_estadual))
        if len(insc_estadual) != 9:
            return False
        else:
            return True


class AtualizaCodigo:
    @staticmethod
    def cod_produto():
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

    class OrdemCompra:

        @staticmethod
        def buscar_ordem_compra2(ordem_compra, razaosocial):
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
                # resultado = '0', '0', '0', '0', '0'
                return

        @staticmethod
        def buscar_ordem_compra(ordem_compra):
            try:
                query = f'select * from ordem_compra where ordem_compra = {ordem_compra}'
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
        def buscar_nf(nf):
            """
                O objetivo é buscar a NF na pasta especificada e retornar verdadeiro
            ou falso.
                1 - chamar a função buscar_cnpj
                caso verdadeiro:
                - chamar a função Formatadores.formatar_xml
                - chamar a funçao visualizar nf (logistica)  ** qual classe ?? **
                - chamar a função Validadores.analisar_nf
            """
            pass
        @staticmethod
        def analisar_nf(nf):

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
    def validar_ean():
        pass

    @staticmethod
    def mostrar_tabela_produtos():
        mydb.connect()
        query = 'select * from produtos'

        mycursor.execute(query)
        myresult = mycursor.fetchall()
        return myresult

class BancoDeDados:  # queries
    pass

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


def buscar_cnpj(cnpj):
    mydb.connect()
    query = f"SELECT * FROM fornecedores WHERE CNPJ = '{cnpj}'"
    mycursor.execute(query)
    myresult = mycursor.fetchall()

    if len(myresult) == 0:
        return False
    else:
        return True
