from datetime import datetime, timedelta, date
import mysql.connector
from pycpfcnpj import cpfcnpj as validador_cnpj
from flask import session, redirect, url_for


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


class Buscadores:
    @staticmethod
    def buscar_fornecedor():
        try:
            query = f"select razaosocial from fornecedores"
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







def buscar_cnpj(cnpj):
    query = f"SELECT * FROM fornecedores WHERE CNPJ = '{cnpj}'"
    mycursor.execute(query)
    myresult = mycursor.fetchall()

    if len(myresult) == 0:
        return False
    else:
        return True
