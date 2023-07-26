import mysql.connector

def dbconfig():
    try:
        db=mysql.connector.connect(
            host="localhost",
            user="root",
            password=""
            )
    except Exception as e:
        print("Connection Failed")

    return db

