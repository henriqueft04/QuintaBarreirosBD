from flask import Flask, request, redirect, url_for, render_template
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
    return render_template('tabelaClientes.html', clientes=clientes)

@app.route('/clientesForm', methods=['GET', 'POST'])
def clientesForm():
        if request.method == 'POST':
            try:
                nif = request.form['nif']
                nif = int(nif)
                morada = request.form['morada']
                nome = request.form['nome']
                telemovel = request.form['telemovel']
                telemovel = int(telemovel)
                tipo = request.form['tipo']

                print(f"Recebido: NIF={nif}, Morada={morada}, Nome={nome}, Telemovel={telemovel}, Tipo={tipo}")

                Insert_Cliente(nif, morada, nome, telemovel, tipo)

                print(f"Cliente inserido com sucesso: {nif}, {morada}, {nome}, {telemovel}, {tipo}")

                clientes = Search_Clients("")
                print("AAAAAAAAAAAAAAAAAAAAAAAAAAAA")
                
            except Exception as e:
                # Log do erro
                print("ola sou eu o erro")
                print(f"Erro ao inserir cliente: {e}")
                return render_template('clienteForm.html', error=str(e))
            
            return render_template('tabelaClientes.html', clientes=clientes)
        else:
            return render_template('clienteForm.html')


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

@app.route('/novoFornecimento')
def novoFornecimento():
    return render_template('novoFornecimento.html')

@app.route('/novoEngarrafamento')
def novoEngarrafamento():
    return render_template('novoEngarrafamento.html')

@app.route('/novaCuba')
def novaCuba():
    return render_template('novaCuba.html')

@app.route('/novoVinho')
def novoVinho():
    return render_template('novoVinho.html')

@app.route('/novaRolha')
def novaRolha():
    return render_template('novaRolha.html')

@app.route('/novoFornecedor')
def novoFornecedor():
    return render_template('novoFornecedor.html')

@app.route('/encomendaDetalhes')
def encomendasDetalhes():
    return render_template('encomendaDetalhes.html')

if __name__ == "__main__":
    app.run(debug=True)
