from modulos.utils.console import CorFonte
from modulos.utils.queries import mydb, mycursor

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
