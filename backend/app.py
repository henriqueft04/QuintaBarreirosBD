from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/clientes')
def clientes():
    return render_template('clientes.html')

@app.route('/fornecedores')
def fornecedores():
    return render_template('fornecedores.html')

@app.route('/nova-encomenda')
def nova_encomenda():
    return render_template('nova-encomenda.html')

@app.route('/encomendas')
def encomendas():
    return render_template('encomendas.html')

@app.route('/engarrafamentos')
def engarrafamentos():
    return render_template('engarrafamentos.html')

@app.route('/stock')
def stock():
    return render_template('stock.html')

@app.route('/apply-filters', methods=['POST'])
def apply_filters():
    data = request.json
    selected_day = data.get('day')
    selected_week = data.get('week')
    selected_month = data.get('month')
    selected_year = data.get('year')

    # Conecte-se ao seu banco de dados
    conn = sqlite3.connect('database.db')  # Substitua pelo seu banco de dados
    cursor = conn.cursor()

    # Crie uma consulta SQL com base nos filtros recebidos
    query = "SELECT * FROM encomendas WHERE 1=1"
    params = []

    if selected_day:
        query += " AND strftime('%d-%m-%Y', data) = ?"
        params.append(selected_day)
    if selected_week:
        query += " AND strftime('%W-%m-%Y', data) = ?"
        params.append(selected_week)
    if selected_month:
        query += " AND strftime('%m-%Y', data) = ?"
        params.append(selected_month)
    if selected_year:
        query += " AND strftime('%Y', data) = ?"
        params.append(selected_year)

    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()

    # Retorne os resultados como JSON
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
