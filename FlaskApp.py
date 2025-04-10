from flask import Flask, render_template_string
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
    sql = "SELECT * FROM Track LIMIT 10;"
    columns, rows = query(sql)
    
    #Used ChatGPT for html formatting for SQL results
    html = '''
    <h2>Query Results</h2>
    <table border="1" cellpadding="5">
        <thead>
            <tr>{% for col in columns %}
                <th>{{ col }}</th>
            {% endfor %}</tr>
        </thead>
        <tbody>
            {% for row in rows %}
            <tr>{% for item in row %}
                <td>{{ item }}</td>
            {% endfor %}</tr>
            {% endfor %}
        </tbody>
    </table>
    '''

    return render_template_string(html, columns=columns, rows=rows)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)