from flask import Flask, render_template
from dbTesting import query

app = Flask(__name__)

#-----------------------------------------------------
#Route to Main page (nothing here yet except "Hello")
#-----------------------------------------------------
@app.route('/')
def hello():
    return '<h1>Hello</h1>'

#-----------------------------------------------------
#Route to View Database
#-----------------------------------------------------
@app.route('/viewdb')
def viewdb():
    sql = "SHOW TABLES;"
    columns, rows = query(sql)

    return render_template('test.html', columns=columns, rows=rows)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)