import mysql.connector as db

def get_db():
    conn = db.connect(host='localhost', user='root', password='root', database='client_query_management')
    return conn, conn.cursor(dictionary=True)
