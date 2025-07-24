import pymysql

def get_connection():
    return pymysql.connect(
        host="127.0.0.1",
        user="root",
        password="1234",
        database="cozy_comfort",
        connect_timeout=5
    )
