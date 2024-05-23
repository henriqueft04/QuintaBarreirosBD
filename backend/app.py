from flask import Flask, render_template, request,jsonify
from database.connection import get_db_connection 

app = Flask(__name__)

@app.route('/')
def index():

    return render_template('index.html')

@app.route('/clientes')
def clientes():

    query=""" 
        SELECT * FROM QB.cliente
    """
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute(query)
    clientes = cursor.fetchall()
    db.close()
    return render_template('clientes.html', clientes=clientes)

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
