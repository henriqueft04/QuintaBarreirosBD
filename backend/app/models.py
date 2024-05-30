""" Ficheiro com as funções que vão ser chamadas para criar as tabelas. """
from flask import Flask, render_template, request,jsonify, Request, Response
from database.connection import get_db_connection



def Search_Clients(search_param):
    query = "SELECT * FROM QB.cliente"
    params = []

    if search_param:
        if search_param.isdigit():
            query += " WHERE QB.cliente.telemovel LIKE ?"
            params.append('%' + search_param + '%')
        else:
            query += " WHERE QB.cliente.nome LIKE ?"
            params.append('%' + search_param + '%')
    
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

def Get_Num_Clients():
    query = "SELECT COUNT(*) AS TotalClientes FROM QB.cliente"

    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute(query)
    num_clients = cursor.fetchone()
    num_clients = num_clients[0]


    print(f"Número de clientes: {num_clients}")  # Debug

    return num_clients

def Insert_Cliente(nif, morada, nome, telemovel, tipo):
    db = get_db_connection()
    cursor = db.cursor()

    query = "{CALL QB.p_AdicionarCliente(?, ?, ?, ?, ?)}"

    cursor.execute(query, (nif, morada, nome, telemovel, tipo))
    db.commit()
    cursor.close()

def Get_Num_Garrafas_Cliente():
    query = "{CALL QB.p_NumberOfBottlesPerClient}"

    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute(query)
    results = cursor.fetchall()

    # Acessar elementos pelo índice
    num_garrafas = {row[0]: row[2] for row in results}  # Usando ClienteNIF (índice 0) como chave e TotalGarrafas (índice 2) como valor

    print(f"Número de garrafas por cliente: {num_garrafas}")  # Debug

    return num_garrafas

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




def get_fornecimentos():
    query = "{CALL QB.fornecimentos}"

    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute(query)
    fornecimentos = cursor.fetchall()

    cursor.nextset()
    total_fornecedores = cursor.fetchone()[0]

    cursor.nextset()
    tipos_rolhas = cursor.fetchall()

    return fornecimentos, total_fornecedores, tipos_rolhas

def get_engarrafamentos():
    query = "{CALL QB.engarrafamentos}"

    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute(query)
    engarrafamentos = cursor.fetchall()


    total_engarrafamentos = cursor.fetchone()[0]


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