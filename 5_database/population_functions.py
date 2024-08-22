import mysql.connector

def connect_to_database():
    """Establish a connection to the MySQL database."""
    connection = mysql.connector.connect(
        host='localhost',  # Replace with your host
        user='root',       # Replace with your MySQL username
        password='password', # Replace with your MySQL password
        database='inventory_management'  # Replace with your database name
    )
    return connection

def insert_into_table(connection, table_name, columns, data):
    """Insert data into a specified table."""
    cursor = connection.cursor()
    placeholders = ', '.join(['%s'] * len(columns))
    columns = ', '.join(columns)
    sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    cursor.executemany(sql, data)
    connection.commit()
    cursor.close()

def close_connection(connection):
    """Close the database connection."""
    connection.close()