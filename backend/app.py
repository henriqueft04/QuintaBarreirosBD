from flask import Flask, render_template, request,jsonify
from database.connection import get_db_connection 

app = Flask(__name__)

@app.route('/')
def index():

    return render_template('index.html')

@app.route('/clientes')
def clientes():

    search_param = request.args.get('nome', '')

    print(f"Recebendo parâmetro de busca: {search_param}")  # Debug


    query = "SELECT * FROM QB.cliente"
    params = []

    if search_param:
        if search_param.isdigit():
            query += " WHERE QB.cliente.telemovel LIKE '%" + search_param + "%'"
            params.append('%' + search_param + '%')
        else:
            query += " WHERE QB.cliente.nome LIKE '%" + search_param + "%'"
            params.append('%' + search_param + '%')


    
    print(f"Query SQL: {query}")  # Debug
    print(f"Parâmetros: {params}")  # Debug


    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute(query)
    clientes = cursor.fetchall()
    db.close()


    print(f"Clientes encontrados: {clientes}")  # Debug

    return render_template('clientes.html', clientes=clientes)

@app.route('/search', methods=['GET'])
def search_cliente():
    nome = request.args.get('nome', '')
    telemovel = request.args.get('telemovel', '')

    query = "SELECT * FROM Cliente WHERE nome LIKE ? OR telemovel LIKE ?"
    params = ['%' + nome + '%', '%' + telemovel + '%']

    cursor = get_db_connection().cursor()
    cursor.execute(query, params)
    result = cursor.fetchall()
    cursor.close()

    clientes = []
    for row in result:
        cliente = {
            'id': row.id,
            'nome': row.nome,
            'telemovel': row.telemovel,
            'nif': row.nif,
            'morada': row.morada,
            'total': row.total,
            'tipo': row.tipo
        }
        clientes.append(cliente)

    return jsonify(clientes)

@app.route('/fornecedores')
def fornecedores():
    return render_template('fornecedores.html')

@app.route('/nova-encomenda')
def nova_encomenda():
    return render_template('nova-encomenda.html')

@app.route('/encomendas')
def encomendas():

    query=""" 
        SELECT * FROM QB.encomenda
    """
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute(query)
    encomendas = cursor.fetchall()
    db.close()

    return render_template('encomendas.html', encomendas=encomendas)

@app.route('/engarrafamentos')
def engarrafamentos():
    return render_template('engarrafamentos.html')

@app.route('/stock')
def stock():
    return render_template('stock.html')

@app.route('/cubas')
def cubas():
    query = """
        SELECT * FROM QB.cuba
    """
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute(query)
    cubas = cursor.fetchall()
    db.close()

    return render_template('cubas.html', cubas=cubas)

@app.route('/novaForm')
def novaForm():
    return render_template('novaForm.html')

@app.route('/clienteForm')
def clientesForm():
    return render_template('clienteForm.html')

@app.route('/novoFornecimento')
def novoFornecimento():
    return render_template('novoFornecimento.html')

@app.route('/novoEngarrafamento')
def novoEngarrafamento():
    return render_template('novoEngarrafamento.html')

if __name__ == "__main__":
    app.run(debug=True)
