import mysql.connector
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Ma204619@",
    database="projeto_erp"
)
mycursor = mydb.cursor()


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="user",
        password="senha",
        database="erp"
    )
