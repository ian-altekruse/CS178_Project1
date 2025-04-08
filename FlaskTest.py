from flask import Flask

app = Flask(__name__)

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
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(query, args)
    rows = cur.fetchall()
    col_names = [desc[0] for desc in cur.description]
    cur.close()
    conn.close()
    return col_names, rows




#display the sqlite query in a html table
def display_html(columns, rows):
    html = "<table><tr>"
    for col in columns:
        html += f"<th>{col}</th>"
    html += "</tr>"

    for row in rows:
        html += "<tr>" + "".join(f"<td>{str(cell)}</td>" for cell in row) + "</tr>"

    html += "</table></body>"
    return html




@app.route("/viewdb")
def viewdb():
    columns, rows = execute_query("""SELECT movie_id, title, release_date, revenue FROM movie WHERE revenue > 1000000000 ORDER BY release_date desc LIMIT 1000""")
    return display_html(columns, rows)

@app.route("/")
def test():
    return "Flask is running!"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)