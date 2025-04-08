from flask import Flask, render_template
from dbCode import *

app = Flask(__name__)

@app.route("/viewdb")
def viewdb():
    rows, columns = display_database()
    return render_template('index.html', rows=rows, columns = columns)


@app.route("/")
def test():
    return "Flask is running!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)