from flask import Flask, render_template_string
from dbTesting import query  # import your improved query function

app = Flask(__name__)

@app.route('/viewdb')
def viewdb():
    sql = "SELECT * FROM Track LIMIT 10;"
    columns, rows = query(sql)

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
    app.run(debug=True)