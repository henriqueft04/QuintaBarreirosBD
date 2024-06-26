from flask import Flask, request, redirect, url_for, render_template, flash, session,get_flashed_messages
from database.connection import get_db_connection 
from app.models import *
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print('POST request received')
        username = request.form['username']
        password = request.form['password']

        db = get_db_connection()
        cursor = db.cursor()

        hashed_password_query = """SELECT QB.HashPassword(?)"""
        cursor.execute(hashed_password_query, (password,))
        hashed_password = cursor.fetchone()

        if hashed_password:
            hashed_password = hashed_password[0]

            query = """SELECT username, role FROM QB.utilizador WHERE username = ? AND password = ?"""
            cursor.execute(query, (username, hashed_password))
            user = cursor.fetchone()

            if user:
                print('user: %s' % user[0])
                print('role: %s' % user[1])
                session['username'] = user[0]
                session['role'] = user[1]
                flash('Login efetuado com sucesso!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Credenciais inválidas. Tente novamente.', 'error')
        else:
            flash('Erro ao processar a senha.', 'error')

    print('GET request or login failed')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Logout efetuado com sucesso!', 'success')
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_confirm = request.form['password-confirm']
        role = request.form['role']
        print(f"username: {username}, role: {role}")  # Avoid printing passwords

        if password != password_confirm:
            flash('As senhas não coincidem. Tente novamente.', 'error')
            return redirect(url_for('register'))

        db = get_db_connection()
        cursor = db.cursor()

        try:
            # Verificar se o utilizador já existe
            query = """SELECT * FROM QB.utilizador WHERE username = ?"""
            cursor.execute(query, (username,))
            user = cursor.fetchone()

            if user:
                flash('Utilizador já existe. Tente novamente.', 'error')
                return redirect(url_for('register'))

            # Hash the password
            hashed_password = cursor.execute("""SELECT QB.HashPassword(?)""", (password,)).fetchone()[0]

            # Inserir o novoutilizador 
            insert_query = """INSERT INTO QB.utilizador (username, password, role) VALUES (?, ?, ?)"""
            cursor.execute(insert_query, (username, hashed_password, role))
            db.commit()

            flash('Registo efetuado com sucesso! Faça login.', 'success')
            return redirect(url_for('login'))

        except Exception as e:
            db.rollback()  # Rollback in case of error
            print(f"Erro ao registar o utilizador: {e}")
            flash('Erro ao registar o utilizador. Tente novamente.', 'error')
            return redirect(url_for('register'))

        finally:
            cursor.close()
            db.close()  # Ensure the connection is closed

    return render_template('register.html')

@app.context_processor
def inject_user():
    print('session: %s' % session)
    return dict(username=session.get('username'), role=session.get('role'))

@app.route('/index')
def index():
    db = get_db_connection()
    cursor = db.cursor()

    count_query = """
        SELECT COUNT(*) AS total_encomendas_ultima_semana
        FROM QB.encomenda
        WHERE data >= DATEADD(WEEK, -1, GETDATE());
        """
    
    cursor.execute(count_query)
    num_encomendas = cursor.fetchone()[0]

    details_query = """
        SELECT e.*, c.nome
        FROM QB.encomenda e
        INNER JOIN QB.cliente c ON e.NIF_cliente = c.NIF
        WHERE e.data >= DATEADD(WEEK, -1, GETDATE())
        """
    
    cursor.execute(details_query)
    encomendas_detalhes = cursor.fetchall()

    return render_template('index.html', num_encomendas=num_encomendas, encomendas=encomendas_detalhes)

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
    if 'username' not in session or session.get('role') == 'Consultor':
        flash('É necessário ser Administrador para adicionar clientes.', 'error')
        return render_template('alertContainer.html')
    else:
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
    if 'username' not in session or session.get('role') == 'Consultor':
        flash('É necessário ser Administrador para adicionar fornecimentos.', 'error')
        return render_template('alertContainer.html')
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

@app.route('/novoFornecedor')
def novoFornecedor():
    if 'username' not in session or session.get('role') == 'Consultor':
        flash('É necessário ser Administrador para adicionar fornecedores.', 'error')
        return render_template('alertContainer.html')
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
        
        return render_template('/fornecedores', fornecedores=fornecedores)
    else:
        return render_template('forms/novoFornecedor.html')

@app.route('/nova-encomenda')
def nova_encomenda():
    if 'username' not in session or session.get('role') == 'Consultor':
        flash('É necessário ser Administrador para adicionar encomendas.', 'error')
        return redirect('encomendas')
    print("nova encomenda")
     
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
    print(orderBy)
    engarrafamentos, total_engarrafamentos = get_engarrafamentos(orderBy)
    if orderBy is not None:
        return render_template('tabelas/tabelaEngarrafamentos.html', engarrafamentos=engarrafamentos)
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
    orderBy = request.args.get('orderBy')

    db = get_db_connection()
    cursor = db.cursor()

    query = f"EXEC QB.cubaInfo @orderBy = '{orderBy}'"
    cursor.execute(query)

    columns = [column[0] for column in cursor.description]
    cubas = [dict(zip(columns, row)) for row in cursor.fetchall()]
    db.close()
    if orderBy is not None:
        return render_template('tabelas/tabelaCubas.html', cubas=cubas)
    return render_template('cubas.html', cubas=cubas)

@app.route('/cubaDelete', methods=['POST'])
def cubaDelete():
    print("entrou")
    if 'username' not in session or session.get('role') == 'Consultor':
        flash('É necessário ser Administrador para remover cubas.', 'error')
        return redirect(url_for('encomendas'))
    
    cuba_id = request.form.get('codigo')
    if cuba_id:
        query = "EXEC QB.deleteCuba ?"
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute(query, (cuba_id,))
        db.commit()
        db.close()
        flash('Cuba removida com sucesso.', 'success')
    else:
        flash('Erro ao tentar remover a cuba.', 'error')
    
    return redirect(url_for('cubas'))

@app.route('/novaForm')
def novaForm():

    if 'username' not in session or session.get('role') == 'Consultor':
        flash('É necessário ser Administrador para adicionar encomendas.', 'error')
        return render_template('alertContainer.html')
    tipos_vinho = get_TipoVinho()
    print("estou cá")

    return render_template('forms/novaForm.html', tipos_vinho=tipos_vinho)

@app.route('/novoEngarrafamento')
def novoEngarrafamento():
    
    if 'username' not in session or session.get('role') == 'Consultor':
        flash('É necessário ser Administrador para adicionar engarrafamentos.', 'error')
        return render_template('alertContainer.html')
    return render_template('forms/novoEngarrafamento.html')

@app.route('/novaCuba')
def novaCuba():
    
    if 'username' not in session or session.get('role') == 'Consultor':
        flash('É necessário ser Administrador para adicionar cubas.', 'error')
        return render_template('alertContainer.html')
    return render_template('forms/novaCuba.html')

@app.route('/novoVinho')
def novoVinho():
    if 'username' not in session or session.get('role') == 'Consultor':
        flash('É necessário ser Administrador para adicionar novos vinhos.', 'error')
        return redirect(url_for('cuba'))
    return render_template('forms/novoVinho.html')

@app.route('/novaRolha')
def novaRolha():
    if 'username' not in session or session.get('role') == 'Consultor':
        flash('É necessário ser Administrador para adicionar novas Rolhas.', 'error')
        return redirect(url_for('cuba'))
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

@app.route('/alertContainer')
def alertContainer():
    messages = get_flashed_messages(with_categories=True)
    return render_template('alertContainer.html', messages=messages)

@app.route('/inserir_encomenda', methods=['POST'])
def inserir_encomenda():
    nome = request.form.get('nome')
    estado = request.form.get('estado')
    notas = request.form.get('notas')
    valor = request.form.get('valor')
    data = request.form.get('data')
    faturada = request.form.get('faturada')

    items = request.form.getlist('items[]')
    quantities_caixas = request.form.getlist('quantities_caixas[]')
    quantities_garrafas = request.form.getlist('quantities_garrafas[]')
    quantities_garrafoes = request.form.getlist('quantities_garrafoes[]')

    estado_pagamento = 1 if estado == 'Pago' else 0
    faturada_bit = 1 if faturada == 'Sim' else 0

    # Prepare the items list
    items_list = []
    for i in range(len(items)):
        items_list.append({"quantidadeItems": int(quantities_caixas[i]), "id_stock": int(items[i]), "dataEng": data})
        items_list.append({"quantidadeItems": int(quantities_garrafas[i]), "id_stock": int(items[i]), "dataEng": data})
        items_list.append({"quantidadeItems": int(quantities_garrafoes[i]), "id_stock": int(items[i]), "dataEng": data})

    # Convert items list to JSON string
    items_json = json.dumps(items_list)

    db = get_db_connection()
    cursor = db.cursor()

    try:
        # Call the stored procedure
        cursor.execute("""
            EXEC QB.insertEncomenda @nomeCliente=?, @estadoPagamento=?, @notas=?, @valor=?, @fatura=?, @data=?, @items=?
        """, (nome, estado_pagamento, notas, valor, faturada_bit, data, items_json))

        db.commit()
    except Exception as e:
        db.rollback()
        print(f'Erro ao inserir encomenda: {str(e)}')
    finally:
        cursor.close()
        db.close()

    return redirect(url_for('engarrafamentos'))

if __name__ == "__main__":
    app.run(debug=True)
