from flask import Flask, request, redirect, url_for, render_template
from database.connection import get_db_connection 
from app.models import *
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():

    return render_template('index.html')

@app.route('/clientes')
def clientes():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    search_param = request.args.get('search_param', '')

    clientes, per_page, page, total_pages = get_paginacao_clientes(search_param, page, per_page)

    for cliente in clientes:
        cliente_nif = cliente['NIF']
        cliente['num_garrafas'] = Get_Num_Garrafas_Cliente(cliente_nif)
    
    num_garrafas_cliente = Get_Num_Garrafas_Cliente(search_param)

    total_clients = Get_Num_Clients(search_param)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render_template('tabelas/tabelaClientes.html', clientes=clientes)

    return render_template('clientes.html', 
                           clientes=clientes, 
                           total_clients=total_clients, 
                           total_garrafas_cliente=num_garrafas_cliente, 
                           page=page, 
                           per_page=per_page, 
                           search_param=search_param,
                           total_pages=total_pages, 
                           endpoint='clientes')

@app.route('/clientes/total')
def clientes_total():
    search_param = request.args.get('search_param', '')
    total_clients = Get_Num_Clients(search_param)
    print("clientes agora ", total_clients)
    return str(total_clients)


@app.route('/searchClientes', methods=['GET'])
def searchClientes():
    search_param = request.args.get('nome', '')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    clientes, per_page, page, total_pages = get_paginacao_clientes(search_param, page, per_page)

    for cliente in clientes:
        cliente_nif = cliente['NIF']
        cliente['num_garrafas'] = Get_Num_Garrafas_Cliente(cliente_nif)

    print(f"Clientes: {clientes}")
    print(page, per_page, total_pages)
    return render_template('tabelas/tabelaClientes.html', clientes=clientes)



@app.route('/clientes/paginacao')
def clientes_paginacao():
    search_param = request.args.get('search_param', '')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    clients, per_page, page, total_pages = get_paginacao_clientes(search_param, page, per_page)

    # Depuração para garantir que a paginação está funcionando corretamente
    print(f"Clientes: {clients}")
    print(f"Página atual: {page}")
    print(f"Total de páginas: {total_pages}")
    print(f"Parâmetro de busca: {search_param}")

    return render_template('pagination.html', page=page, per_page=per_page, total_pages=total_pages, endpoint='clientes')



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

@app.route('/encomendaMultiplas', methods=['GET'])
def encomendaMultiplas():
    nif_cliente = request.args.get('nif')
    encomendas = Get_Encomendas_Cliente(nif_cliente)
    print(f"Encomendas do cliente {nif_cliente}: {encomendas}")
    return render_template('tabelas/tabelaEncomendas.html', encomendas=encomendas)


@app.route('/vinhoUnico', methods=['GET'])
def vinhoUnico():
    id_vinho = request.args.get('id')
    vinho = Get_Vinho(id_vinho)
    print(f"Vinho {id_vinho}: {vinho}")
    return render_template('tabelas/vinhoDetalhes.html', vinho=vinho)


@app.route('/fornecedores')
def fornecedores():
    search_param = request.args.get('search_param', None)
    if search_param:
        fornecimentos = Search_Fornecedor(search_param)

        return render_template('fornecedores.html', fornecimentos=fornecimentos)
    else:
        fornecimentos, total_fornecedores, tipos_rolhas = get_fornecimentos()

        return render_template('fornecedores.html', fornecimentos=fornecimentos, total_fornecedores=total_fornecedores, tipos_rolhas=tipos_rolhas)

@app.route('/searchFornecedores', methods=['GET'])
def searchFornecedores():
    search_param = request.args.get('nome', '')
    print(f"Search param: {search_param}")
    fornecimentos = Search_Fornecedor(search_param)

    print(f"Fornecedores: {fornecimentos}")
    return render_template('tabelas/tabelaFornecimentos.html', fornecimentos=fornecimentos)

@app.route('/novoFornecimento', methods=['GET', 'POST'])
def novoFornecimento():
    print("Entrou no novo fornecimento")
    print(request.method)
    try:
        if request.method == 'POST':
            fornecimentos, total_fornecedores, tipos_rolhas = get_fornecimentos()
            print("Recebendo dados do formulário...")
            nome = request.form['nome']
            print(nome)
            tipo = request.form['tipo']
            print(tipo)
            quantidade = request.form['quantidade']
            quantidade = int(quantidade)
            print(quantidade)
            data = request.form['data']
            data = datetime.strptime(data, '%Y-%m-%d').date()

            print(f"Recebido: Nome={nome}, TipoRolha={tipo}, Quantidade={quantidade}, Data={data}")
            if not tipo:
                raise ValueError("Tipo de rolha não foi selecionado.")


            Insert_Fornecimento(nome, tipo, quantidade, data)

            print(f"Fornecimento inserido com sucesso: {nome}, {tipo}, {quantidade}, {data}")

            return redirect(url_for('fornecedores'))
        
        fornecimentos, total_fornecedores, tipos_rolhas = get_fornecimentos()

        print(f"Tipos de rolhas: {tipos_rolhas}")
        return render_template('forms/novoFornecimento.html', tipos_rolhas=tipos_rolhas, fornecimentos=fornecimentos, total_fornecedores=total_fornecedores)
        
        
    except Exception as e:
        print(f"ERRO: {e}")
        return render_template('forms/novoFornecimento.html', error=str(e))

@app.route('/novoFornecedor', methods=['GET', 'POST'])
def novoFornecedor():
    if request.method == 'POST':
        try:
            nomeFornecedor = request.form['nomeFornecedor']
            telemovelForn = request.form['telemovelForn']
            telemovelForn = int(telemovelForn)
            NIF_forn = request.form['NIF_forn']
            NIF_forn = int(NIF_forn)
            morada_forn = request.form['morada_forn']

            print(f"Recebido: Nome={nomeFornecedor}, Telemovel={telemovelForn}, NIF={NIF_forn}, Morada={morada_forn}")
            Insert_Fornecedor(nomeFornecedor, telemovelForn, NIF_forn, morada_forn)


            fornecedores = Search_Fornecedor("")
            print(f"Fornecedor inserido com sucesso: {nomeFornecedor}, {telemovelForn}, {NIF_forn}, {morada_forn}")

        except Exception as e:
            print(f"Erro ao inserir fornecedor: {e}")
            return render_template('forms/novoFornecedor.html', error=str(e))
        
        return render_template('tabelas/tabelaFornecimentos.html', fornecedores=fornecedores)
    else:
        return render_template('forms/novoFornecedor.html')

@app.route('/nova-encomenda')
def nova_encomenda():

    tipos_vinho = get_TipoVinho()

    return render_template('nova-encomenda.html', tipos_vinho=tipos_vinho)

@app.route('/encomendas')
def encomendas():
    # Obter a página atual e o número de registros por página da query string
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    ano = request.args.get('ano', type=int)
    mes = request.args.get('mes', type=int)
    semana = request.args.get('semana', type=int)
    dia = request.args.get('dia', type=str)

    if dia:
        try:
            dia = datetime.strptime(dia, '%Y-%m-%d').date()
        except ValueError:
            dia = None
    else:
        dia = None

    db = get_db_connection()
    cursor = db.cursor()

    # Calcular o total de registros
    total_query = """SELECT QB.fn_AtualizaContagemEncomendas(?,?,?,?)"""
    cursor.execute(total_query, (ano, mes, semana, dia))
    total_records = cursor.fetchone()[0]

    # Calcular o número total de páginas
    total_pages = (total_records + per_page - 1) // per_page

    # Chamar a stored procedure
    query = """EXEC QB.GetEncomendasPaginadas @PageNumber=?, @RowsPerPage=?, @ano=?, @mes=?, @semana=?, @dia=?"""
    cursor.execute(query, (page, per_page, ano, mes, semana, dia))
    encomendas = cursor.fetchall()
    db.close()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        print(ano , "\n" , mes , "\n" , semana , "\n" , dia)
        print(encomendas)
        table_html = render_template('tabelas/tabelaEncomendas.html', encomendas=encomendas)
        return table_html
    
    

    return render_template('encomendas.html', encomendas=encomendas, page=page, per_page=per_page, total_pages=total_pages, total_records=total_records, endpoint='encomendas')


@app.route('/encomendas/paginacao')
def encomendas_paginacao():
    # Obter a página atual e o número de registros por página da query string
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    ano = request.args.get('ano', type=int)
    mes = request.args.get('mes', type=int)
    semana = request.args.get('semana', type=int)
    dia = request.args.get('dia', type=str)

    if dia:
        try:
            dia = datetime.strptime(dia, '%Y-%m-%d').date()
        except ValueError:
            dia = None
    else:
        dia = None

    db = get_db_connection()
    cursor = db.cursor()

    # Calcular o total de registros
    total_query = """SELECT QB.fn_AtualizaContagemEncomendas(?,?,?,?)"""
    cursor.execute(total_query, (ano, mes, semana, dia))
    total_records = cursor.fetchone()[0]

    # Calcular o número total de páginas
    total_pages = (total_records + per_page - 1) // per_page

    pagination_html = render_template('pagination.html', page=page, per_page=per_page, total_pages=total_pages, endpoint='encomendas')
    return pagination_html

@app.route('/encomendas/total')
def encomendas_total():
    ano = request.args.get('ano', type=int)
    mes = request.args.get('mes', type=int)
    semana = request.args.get('semana', type=int)
    dia = request.args.get('dia', type=str)

    if dia:
        try:
            dia = datetime.strptime(dia, '%Y-%m-%d').date()
        except ValueError:
            dia = None
    else:
        dia = None

    db = get_db_connection()
    cursor = db.cursor()
    print(ano)
    total_query = "SELECT QB.fn_AtualizaContagemEncomendas(?,?,?,?)"
    cursor.execute(total_query, (ano, mes, semana, dia))
    total_records = cursor.fetchone()[0]
    print("total", total_records)
    db.close()

    return str(total_records)


@app.route('/engarrafamentos')
def engarrafamentos():
    orderBy = request.args.get('orderBy')
    engarrafamentos, total_engarrafamentos = get_engarrafamentos(orderBy)
    return render_template('engarrafamentos.html', engarrafamentos=engarrafamentos, total_engarrafamentos=total_engarrafamentos)

@app.route('/stock')
def stock():
    query = """EXEC QB.stockInfo"""
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute(query)
    columns = [column[0] for column in cursor.description]
    stock = [dict(zip(columns, row)) for row in cursor.fetchall()]
    db.close()

    return render_template('stock.html', stocks=stock)

@app.route('/cubas')
def cubas():
    query = "EXEC QB.cubaInfo"
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute(query)
    columns = [column[0] for column in cursor.description]
    cubas = [dict(zip(columns, row)) for row in cursor.fetchall()]
    db.close()
    return render_template('cubas.html', cubas=cubas)

@app.route('/cubaDelete', methods=['POST'])
def cubaDelete():
    cuba_id = request.form.get('codigo')
    query = "EXEC QB.deleteCuba ?"
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute(query, (cuba_id,))
    db.commit()
    db.close()
    return redirect(url_for('cubas'))

@app.route('/novaForm')
def novaForm():

    tipos_vinho = get_TipoVinho()

    return render_template('forms/novaForm.html', tipos_vinho=tipos_vinho)

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
