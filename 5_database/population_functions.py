import mysql.connector
import pandas as pd

def connect_to_database(host, user, password, database):
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    return connection

def populate_table_from_csv(connection, table_name, csv_file_path):
    cursor = connection.cursor()

    # Load the CSV file into a DataFrame
    data = pd.read_csv(csv_file_path)
    
    # Remove duplicates based on the primary key column(s)
    if table_name == "Customers":
        data = data.drop_duplicates(subset=["customerid"])
    elif table_name == "Products":
        data = data.drop_duplicates(subset=["stockcode"])
    elif table_name == "Invoices":
        data = data.drop_duplicates(subset=["invoiceno"])
    
    # Prepare the SQL statement for data insertion
    placeholders = ', '.join(['%s'] * len(data.columns))
    columns = ', '.join(data.columns)
    sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    
    # Insert each row
    for row in data.itertuples(index=False, name=None):
        try:
            cursor.execute(sql, row)
        except mysql.connector.IntegrityError as e:
            print(f"Error inserting row {row}: {e}")
    
    # Commit the transaction
    connection.commit()
    cursor.close()


def close_connection(connection):
    connection.close()

