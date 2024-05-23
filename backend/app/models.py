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
    
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute(query, params)
    clientes = cursor.fetchall()
    db.close()

    print(f"Clientes encontrados: {clientes}")  # Debug

    return clientes


