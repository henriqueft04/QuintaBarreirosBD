""" Ficheiro com as funções que vão ser chamadas para criar as tabelas. """
from flask import Flask, render_template, request,jsonify, Request, Response
from database.connection import get_db_connection


def Search_Clients(search_param, page, per_page):
    query = """
    SELECT * 
    FROM QB.cliente
    WHERE (? IS NULL OR QB.cliente.telemovel LIKE ? OR QB.cliente.nome LIKE ?)
    ORDER BY nome
    OFFSET ? ROWS FETCH NEXT ? ROWS ONLY
    """
    params = [search_param if search_param else None, '%' + search_param + '%', '%' + search_param + '%', (page-1) * per_page, per_page]

    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute(query, params)
    clientes = cursor.fetchall()

    clientes_dict = []
    for row in clientes:
        cliente_dict = {
            'NIF': row[0], 
            'morada': row[1], 
            'nome': row[2],
            'telemovel': row[3],
            'tipo': row[4]
        }
        clientes_dict.append(cliente_dict)
    
    return clientes_dict

def Get_Num_Clients(search_param):
    query = "SELECT COUNT(*) FROM QB.cliente WHERE (? IS NULL OR nome LIKE ? OR telemovel LIKE ?)"
    search_param = f"%{search_param}%"
    params = (search_param, search_param, search_param)

    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute(query, params)
    num_clients = cursor.fetchone()[0]

    print(f"Número de clientes: {num_clients}")  # Debug

    return num_clients


def Insert_Cliente(nif, morada, nome, telemovel, tipo):
    db = get_db_connection()
    cursor = db.cursor()

    query = "{CALL QB.p_AdicionarCliente(?, ?, ?, ?, ?)}"

    cursor.execute(query, (nif, morada, nome, telemovel, tipo))
    db.commit()
    cursor.close()

def Get_Num_Garrafas_Cliente(NIF_cliente):
    query = "EXEC QB.GetTotalGarrafasCliente ?"

    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute(query, (NIF_cliente,))
    result = cursor.fetchone()

    total_garrafas = result[0] if result else 0

    print(f"Número de garrafas por cliente: {total_garrafas}")  # Debug


    return total_garrafas

def Get_Encomendas_Cliente(nif_cliente):
    query = "{CALL QB.p_DetalhesEcomendasPorCliente(?)}"
    
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute(query, nif_cliente)
    results = cursor.fetchall()

    encomendas = []
    for row in results:
        encomenda = {
            'nome': row[0],
            'numero': row[1],
            'data': row[2],
            'estadoPagamento': row[3],
            'fatura': row[4],
            'valor': row[5],
            'notas': row[6],
            'Denominacao': row[7],
            'QuantidadeItems': row[8]
        }

        encomendas.append(encomenda)
    
    return encomendas

def get_fornecimentos(nome_fornecedor=None):
    query = "{CALL QB.fornecimentos(?)}"
    params = (nome_fornecedor,)

    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute(query, params)
    
    # Primeiro conjunto de resultados
    fornecimentos = cursor.fetchall()
    print("fornecimentos: ", fornecimentos)

    cursor.nextset()
    
    # Segundo conjunto de resultados
    total_fornecedores = cursor.fetchone()[0]
    print("total fornecedores: ", total_fornecedores)

    cursor.nextset()
    
    # Terceiro conjunto de resultados
    tipos_rolhas = cursor.fetchall()
    print("tipos_rolhas: ", tipos_rolhas)

    return fornecimentos, total_fornecedores, tipos_rolhas


def get_engarrafamentos(orderBy):
    query = "EXEC QB.engarrafamentos ?"
    params = (orderBy,)
    print(f"QUERY: {query + str(params)}")

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute(query, params)

    engarrafamentos = cursor.fetchall()

    cursor.nextset()
    total_engarrafamentos = cursor.fetchone()

    total_engarrafamentos = total_engarrafamentos[0] if total_engarrafamentos else 0
    print(f"engarrafamentos: {engarrafamentos}")
    cursor.close()
    db.close()

    return engarrafamentos, total_engarrafamentos



def Search_Fornecedor(search_param):
    query = "{CALL QB.fornecimentos(?)}"
    params = (search_param,)

    print(f"QUERY: {query}")

    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute(query, params)
    fornecimentos = cursor.fetchall()

    fornecimentos_dict = []
    for row in fornecimentos:
        fornecimento_dict = {
            'nome': row[0],
            'morada': row[1],
            'telemovel': row[2],
            'material': row[3],
            'formato': row[4],
            'quantidade': row[5],
            'NIF': row[6],
            'quantidadeTotal': row[7],
        }
        fornecimentos_dict.append(fornecimento_dict)

    return fornecimentos_dict

def Insert_Fornecimento(nome, tipo, quantidade, data):
    db = get_db_connection()
    cursor = db.cursor()

    query = "{CALL QB.insert_fornecimento(?, ?, ?, ?)}"
    print(f"QUERY: {query}")

    cursor.execute(query, (nome, tipo, quantidade, data))
    db.commit()
    cursor.close()

def Insert_Fornecedor(nomeFornecedor, telemovelForn, NIF_forn, morada_forn):
    db = get_db_connection()
    cursor = db.cursor()

    query = "{CALL QB.insert_fornecedor(?, ?, ?, ?)}"

    cursor.execute(query, (nomeFornecedor, telemovelForn, NIF_forn, morada_forn))
    db.commit()
    cursor.close()

def get_TipoVinho():
    
    query = """SELECT denominacao, id FROM QB.tipoVinho"""
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute(query)
    tipos_vinho = cursor.fetchall()
    db.close()

    return tipos_vinho

def get_paginacao_clientes(search_param, page, per_page):
    db = get_db_connection()
    cursor = db.cursor()

    # Contar o número total de clientes que correspondem ao filtro
    count_query = """
    SELECT COUNT(*) 
    FROM QB.cliente
    WHERE (? IS NULL OR QB.cliente.telemovel LIKE ? OR QB.cliente.nome LIKE ?)
    """
    count_params = [search_param if search_param else None, '%' + search_param + '%', '%' + search_param + '%']
    cursor.execute(count_query, count_params)
    total_clients = cursor.fetchone()[0]

    # Calcular o número total de páginas
    total_pages = (total_clients + per_page - 1) // per_page

    # Obter os clientes com paginação
    clients = Search_Clients(search_param, page, per_page)

    return clients, per_page, page, total_pages


def Get_Vinho(id_vinho):
    db = get_db_connection()
    cursor = db.cursor()

    query = "SELECT * FROM QB.fn_detalhesVinhoID(?)"
    cursor.execute(query, (id_vinho,))
    vinho = cursor.fetchone()
    print(vinho)
    

    return vinho