import mysql.connector

def acesso_db():

    mydb = mysql.connector.connect(
        host="localhost", user="admin2024", password="204619", database="projeto_erp"
    )
    connect = mydb.connect()
    mycursor = mydb.cursor()
    return mydb, mycursor, connect


mydb, mycursor, connect = acesso_db()

