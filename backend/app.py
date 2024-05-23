from flask import Flask, render_template, request,jsonify
from database.connection import get_db_connection 
from app.models import *

app = Flask(__name__)

@app.route('/')
def index():

    return render_template('index.html')

@app.route('/clientes')
def clientes():
    clientes = Search_Clients("")
    total_clients = Get_Num_Clients()
    #print(total_clients)
    return render_template('clientes.html', clientes=clientes, total_clients=total_clients)

@app.route('/searchClientes')
def searchClientes():
    search_param = request.args.get('nome', 'telemovel')
    clientes = Search_Clients(search_param)
    return render_template('tabelas/tabelaClientes.html', clientes=clientes)




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
    return render_template('forms/novaForm.html')

@app.route('/clienteForm')
def clientesForm():
    return render_template('clienteForm.html')

@app.route('/novoFornecimento')
def novoFornecimento():
    return render_template('forms/novoFornecimento.html')

@app.route('/novoEngarrafamento')
def novoEngarrafamento():
    return render_template('forms/novoEngarrafamento.html')

@app.route('/novaCuba')
def novaCuba():
    return render_template('forms/novaCuba.html')

@app.route('/novoVinho')
def novoVinho():
    return render_template('forms/novoVinho.html')

@app.route('/novaRolha')
def novaRolha():
    return render_template('forms/novaRolha.html')

@app.route('/novoFornecedor')
def novoFornecedor():
    return render_template('forms/novoFornecedor.html')

@app.route('/encomendaDetalhes')
def encomendasDetalhes():
    return render_template('tabelas/encomendaDetalhes.html')

@app.route('/tabelaEncomendas')
def tabelaEncomendas():
    return render_template('tabelas/tabelaEncomendas.html')

if __name__ == "__main__":
    app.run(debug=True)
