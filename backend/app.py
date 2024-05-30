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
    total_garrafas_cliente = Get_Num_Garrafas_Cliente()
    #print(total_clients)
    print(total_garrafas_cliente)
    return render_template('clientes.html', clientes=clientes, total_clients=total_clients, total_garrafas_cliente=total_garrafas_cliente)

@app.route('/searchClientes')
def searchClientes():
    search_param = request.args.get('nome', 'telemovel')

    clientes = Search_Clients(search_param)
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
                # Log do erro
                print("ola sou eu o erro")
                print(f"Erro ao inserir cliente: {e}")
                return render_template('forms/clienteForm.html', error=str(e))
            
            return render_template('tabelas/tabelaClientes.html', clientes=clientes)
        else:
            return render_template('forms/clienteForm.html')


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
    ano = request.args.get('ano', type=int)
    mes = request.args.get('mes', type=int)
    semana = request.args.get('semana', type=int)
    dia = request.args.get('dia', type=int)

    print(ano)
    
    db = get_db_connection()
    cursor = db.cursor()

    # Calcular o total de registros
    total_query = "SELECT QB.fn_AtualizaContagemEncomendas()"
    cursor.execute(total_query)
    total_records = cursor.fetchone()[0]

    # Calcular o número total de páginas
    total_pages = (total_records + per_page - 1) // per_page

    # Chamar a stored procedure
    query = """EXEC GetEncomendasPaginadas @PageNumber=?, @RowsPerPage=?, @ano=?, @mes=?, @semana=?, @dia=?"""
    cursor.execute(query, (page, per_page, ano, mes, semana, dia))
    encomendas = cursor.fetchall()
    db.close()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render_template('tabelas/tabelaEncomendas.html', encomendas=encomendas)

    return render_template('encomendas.html', encomendas=encomendas, page=page, per_page=per_page, total_pages=total_pages, total_records=total_records)


@app.route('/encomendas/total')
def encomendas_total():
    db = get_db_connection()
    cursor = db.cursor()

    total_query = "SELECT QB.fn_AtualizaContagemEncomendas()"
    cursor.execute(total_query)
    total_records = cursor.fetchone()[0]
    db.close()

    return f'<span id="total-encomendas" class="px-3 py-1 text-xs text-green-600 bg-green-100 rounded-full dark:bg-gray-800 dark:text-green-400">{total_records} Encomendas</span>'


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
