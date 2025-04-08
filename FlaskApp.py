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
    cur = get_conn().cursor()
    cur.execute(query, args)
    rows = cur.fetchall()
    cur.close()
    return rows


#display the sqlite query in a html table
def display_html(rows):
    html = ""
    html += """<table><tr><th>movie_id</th><th>title</th><th>release_date</th><th>revenue</th><th>budget</th></tr>"""

    for r in rows:
        html += "<tr><td>" + str(r[0]) + "</td><td>" + str(r[1]) + "</td><td>" + str(r[2]) + "</td><td>" + str(r[3]) + "</td><td>" + str(r[4]) + "</td></tr>"
    html += "</table></body>"
    return html


@app.route("/viewdb")
def viewdb():
    rows = execute_query("""SELECT movie_id, title, release_date, revenue, budget FROM movie limit 100""")
    return display_html(rows)

@app.route("/")
def test():
    return "Flask is running!"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)