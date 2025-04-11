import mysql.connector
import creds

#--------------------------------------------------------------
#Establish connection with SQL using creds in creds.py folder
#--------------------------------------------------------------
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
    
    #Used ChatGPT here to automatically pull column names so they automatically update instead of manually having to change them
    columns = [desc[0] for desc in cursor.description]

    cursor.close()
    conn.close()

    return columns, results
