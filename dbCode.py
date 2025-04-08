import pymysql
import creds 

def get_conn():
    conn = pymysql.connect(
        host= creds.host,
        user= creds.user, 
        password = creds.password,
        db=creds.db,
        )
    return conn

def execute_query(query, args=()):
    cur = get_conn().cursor()
    cur.execute(query, args)
    rows = cur.fetchall()
    #Used ChatGPT here to add columns
    columns = [desc[0] for desc in cur.description]  # Extract column names
    cur.close()
    return rows, columns

def display_database():
    query = """SELECT movie_id, title, release_date, revenue, budget FROM movie limit 100"""
    return execute_query(query)
    