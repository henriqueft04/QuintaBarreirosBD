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
    return render_template('encomendas.html')

@app.route('/engarrafamentos')
def engarrafamentos():
    return render_template('engarrafamentos.html')

@app.route('/stock')
def stock():
    return render_template('stock.html')

@app.route('/cubas')
def cubas():
    return render_template('cubas.html')

if __name__ == "__main__":
    app.run(debug=True)
