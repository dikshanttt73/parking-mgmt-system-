import mysql.connector

def get_connection():
    """Return a new MySQL connection.
    Edit the credentials below to match your local setup.
    """
    return mysql.connector.connect(
        host="localhost",
        user="your_mysql_user",
        password="your_mysql_password",
        database="parking_db"
    )
