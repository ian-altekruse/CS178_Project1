import pymysql
import creds 

#-------------------
# Connect to mysql
#-------------------
def get_conn():
    conn = pymysql.connect(
        host= creds.host,
        user= creds.user, 
        password = creds.password,
        db=creds.db,
        )
    return conn

#------------------------------------------
# Execute queries through mysql connection
#------------------------------------------
def execute_query(query, args=()):
    cur = get_conn().cursor()
    cur.execute(query, args)
    rows = cur.fetchall()
    cur.close()
    return rows


#------------------------------------------
# Check if movie is in movies DB
#------------------------------------------
def test_movie(title):
    query = f"SELECT * FROM movie WHERE title = '{title}'"
    result = execute_query(query)
    return bool(result)





