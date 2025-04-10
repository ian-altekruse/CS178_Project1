import mysql.connector
import creds

import mysql.connector
import creds

# Establish connection and return column names and results
def query(query):
    conn = mysql.connector.connect(
        host=creds.host,
        user=creds.user,
        password=creds.password,
        database=creds.db
    )
    cursor = conn.cursor()
    cursor.execute(query)

    results = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]

    cursor.close()
    conn.close()

    return columns, results
