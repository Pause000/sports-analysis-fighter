import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="192.168.50.26",
        port=3306,
        user="sbunpa",
        password="1234",
        database="sbunpa",
        charset="utf8mb4"
    )
