from datetime import datetime, timedelta, date
import mysql.connector
from pycpfcnpj import cpfcnpj as validador_cnpj
from flask import session, redirect, url_for
from wtforms import FloatField, ValidationError

"""

CLASS Totais ???

CLASS AlertaMsg
    DEF CAD_FORNECEDOR_REALIZADO
    DEF CNPJ_INVALIDO
    DEF CNPJ_INEXISTENTE
    DEF CNPJ_JA_EXISTENTE
    DEF CADASTRO_INEXISTENTE
    
CLASS Formatadores
    DEF FORMATAR_DATA
    DEF DATA_FORMATO_DB
    DEF OS_DATA
    
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
        DEF ULTIMO_PRECO
        DEF BUSCAR_FORNECEDOR
        DEF BUSCAR_PRODUTO_PELO_EAN
        DEF BUSCAR_PRODUTO_PELO_CODIGO
        DEF BUSCAR_PRODUTO_PELA_DESCRICAO
        DEF VALIDAR_EAN (EM ABERTO)
        DEF MOSTRAR_TABELA_PRODUTOS ( PARA POPUP )
            
    

         

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
global mydb, mycursor, connect
mydb, mycursor, connect = acesso_db()


class AlertaMsg:
    def __init__(self):
        self.cnpj_invalido = self.cnpj_invalido
        self.cnpj_ja_existente = self.cnpj_ja_existente
        self.cad_fornecedor_realizado = self.cad_fornecedor_realizado

    @staticmethod
    def cad_fornecedor_realizado():
        session['alert'] = \
            '<div id = "alert" class="alert alert-success", role="alert">CADASTRO REALIZADO!</div>'
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


class Totais:
    @staticmethod
    def atualiza_total_ordem_compra():
        pass


class Formatadores:
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

    @staticmethod
    def preparar_item_ordem_compra():
        a = 'teste'
        return a


class Validadores:
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
            max = 0
            for x in myresult:
                max = x[0]
            max = int(max)
            max = max + 1
            max = str(max)
            if len(max) == 1:
                max = '00000' + max
            if len(max) == 2:
                max = '0000' + max
            if len(max) == 3:
                max = '000' + max
            if len(max) == 4:
                max = '00' + max
            if len(max) == 5:
                max = '0' + max
            return max
        except:
            max = '000001'
            return max

    @staticmethod
    def cod_fornecedor():
        try:
            query = "SELECT MAX(CODIGO) FROM fornecedores"
            mydb.connect()
            mycursor.execute(query)
            myresult = mycursor.fetchall()
            mydb.commit()
            tam_max = 0
            for x in myresult:
                tam_max = x[0]
            tam_max = int(tam_max)
            tam_max = tam_max + 1
            tam_max = str(tam_max)
            if len(tam_max) == 1:
                tam_max = '00000' + tam_max
            if len(tam_max) == 2:
                tam_max = '0000' + tam_max
            if len(tam_max) == 3:
                tam_max = '000' + tam_max
            if len(tam_max) == 4:
                tam_max = '00' + tam_max
            if len(tam_max) == 5:
                tam_max = '0' + tam_max
            return tam_max
        except:
            max = '000001'
            return max
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
        except:
            ordem_compra_atual = '000001'
            return



class Buscadores:
    def __init__(self):
        pass

    class OrdemCompra:
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

                if codigo == 0 :
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

    def buscar_produto_pelo_ean(self):
        print('metodo buscar pelo ean')
        try:
            query = f'select * from produtos where ean = "{self}"'
            mydb.connect()
            mycursor.execute(query)
            myresult = mycursor.fetchall()
            mydb.commit()
            mydb.close()
            print(myresult)
            return myresult
        except Exception as e:
            print(e)

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
           #geral.AlertaMsg.cadastro_inexistente()
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
