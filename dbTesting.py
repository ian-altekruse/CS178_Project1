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

#--------------------------
# Display results as html
#--------------------------
def display_html(rows):
    html = ""
    html += """<table><tr><th>Tables</th></tr>"""

    for r in rows:
        html += "<tr><td>" + str(r[0])
    html += "</table></body>"
    return html