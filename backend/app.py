from flask import Flask, request, redirect, url_for, render_template
from database.connection import get_db_connection 
from app.models import *

app = Flask(__name__)

@app.route('/')
def index():

    return render_template('index.html')

@app.route('/clientes')
def clientes():
    search_param = request.args.get('search_param', '')
    
    if search_param:
        clientes = Search_Clients(search_param)
    else:
        clientes = Search_Clients("")

    total_clients = Get_Num_Clients()
    num_garrafas_cliente = Get_Num_Garrafas_Cliente()

    # Adicionar o número de garrafas aos dados dos clientes usando o NIF
    for cliente in clientes:
        cliente_nif = cliente['NIF']  # Supondo que a chave primária do cliente seja 'NIF'
        cliente['num_garrafas'] = num_garrafas_cliente.get(cliente_nif, 0)

    return render_template('clientes.html', clientes=clientes, total_clients=total_clients, total_garrafas_cliente=num_garrafas_cliente)


@app.route('/searchClientes', methods=['GET'])
def searchClientes():
    search_param = request.args.get('nome', '')
    clientes = Search_Clients(search_param)
    num_garrafas_cliente = Get_Num_Garrafas_Cliente()

    for cliente in clientes:
        cliente_nif = cliente['NIF']  
        cliente['num_garrafas'] = num_garrafas_cliente.get(cliente_nif, 0)

    return render_template('tabelas/tabelaClientes.html', clientes=clientes)

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

                
            except Exception as e:
                print(f"Erro ao inserir cliente: {e}")
                return render_template('forms/clienteForm.html', error=str(e))
            
            return render_template('tabelas/tabelaClientes.html', clientes=clientes)
        else:
            return render_template('forms/clienteForm.html')

@app.route('/encomendaDetalhes', methods=['GET'])
def encomendaDetalhes():
    nif_cliente = request.args.get('nif')
    encomendas = Get_Encomendas_Cliente(nif_cliente)
    return render_template('tabelas/tabelaEncomendas.html', encomendas=encomendas)


@app.route('/fornecedores')
def fornecedores():
    fornecimentos, total_fornecedores, tipos_rolhas = get_fornecimentos()
    return render_template('fornecedores.html', fornecimentos=fornecimentos, total_fornecedores=total_fornecedores, tipos_rolhas=tipos_rolhas)

@app.route('/nova-encomenda')
def nova_encomenda():
    return render_template('nova-encomenda.html')

@app.route('/encomendas')
def encomendas():
    # Obter a página atual e o número de registros por página da query string
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    db = get_db_connection()
    cursor = db.cursor()

    # Calcular o total de registros
    total_query = "SELECT COUNT(*) FROM QB.encomenda"
    cursor.execute(total_query)
    total_records = cursor.fetchone()[0]

    # Calcular o número total de páginas
    total_pages = (total_records + per_page - 1) // per_page

    # Chamar a stored procedure
    query = """EXEC GetEncomendasPaginadas @PageNumber=?, @RowsPerPage=?"""
    cursor.execute(query, (page, per_page))
    encomendas = cursor.fetchall()
    db.close()

    return render_template('encomendas.html', encomendas=encomendas, page=page, per_page=per_page, total_pages=total_pages, total_records=total_records)



@app.route('/engarrafamentos')
def engarrafamentos():
    engarrafamentos, total_engarrafamentos = get_engarrafamentos()
    return render_template('engarrafamentos.html', engarrafamentos=engarrafamentos, total_engarrafamentos=total_engarrafamentos)

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

@app.route('/tabelaFornecimentos')
def tabelaFornecimentos():
    return render_template('tabelas/tabelaFornecimentos.html')

@app.route('/vinhoDetalhes')
def tabelaTipoVinho():
    return render_template('tabelas/vinhoDetalhes.html')

@app.route('/tabelaEngarramentos')
def tabelaEngarrafamentos():
    return render_template('tabelas/tabelaEngarrafamentos.html')

if __name__ == "__main__":
    app.run(debug=True)
