from flask import Flask
from dbTesting import execute_query, display_html

app = Flask(__name__)

#--------------------------------
# Flask Home Page
#_-------------------------------
@app.route("/")
def home():
    html = "<h2>Home</h2>"
    return html

#-------------------------------------------------------
# View Database Route using functions from dbTesting.py
#-------------------------------------------------------
@app.route("/viewdb")
def viewdb():
    rows = execute_query("""SHOW TABLES""")
    return display_html(rows)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)