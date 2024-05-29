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

    print(f"Recebendo parâmetro de busca: {search_param}")  # Debug
    print(f"Query SQL: {query}")  # Debug
    print(f"Parâmetros: {params}")  # Debug
    
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
    query = "{CALL QB.p_getNumberOfClients}"

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

    cursor.close()
    db.close()

    return fornecimentos, total_fornecedores, tipos_rolhas

def get_engarrafamentos():
    query = "{CALL QB.engarrafamentos}"
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute(query)
    engarrafamentos = cursor.fetchall()
    cursor.nextset()
    total_engarrafamentos = cursor.fetchone()[0]
    cursor.close()
    db.close()

    return engarrafamentos, total_engarrafamentos


