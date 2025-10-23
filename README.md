# QuintaBarreirosBD
Gestão de stocks e de clientes de uma Adega

## Nota 
A análise de requisitos no relatório não é uma análise de requisitos, está errada. O projeto foi submetido a alterações, devido a isso a demo será diferente da apresentada.
Foi implementado mais o login, com a palavra-passe encriptada atraves de hash.

## Setup do Projeto

### 1. Clone o repositório
```bash
git clone https://github.com/henriqueft04/QuintaBarreirosBD
ou
abrir a pasta QUINTABARREIROSBD e abrir o terminal nesse repositorio
```
### 2. Configurar o ambiente virtual
```
windows -> python -m venv venv
linux/Mac -> python3 -m venv venv
```
### 3. Ativar o ambiente virtual
```
windows -> ./venv/Scripts/activate
linux/Mac -> source venv/bin/activate
```
### 4. Instalar as dependências
```
pip install -r backend/requirements.txt
```
### 5. Criar config.py na pasta backend/database
```
DATABASE_CONFIG = {
    'server': 'tcp:mednat.ieeta.pt\SQLSERVER,8101',
    'database': 'p8g4',
    'username': 'your_username',
    'password': 'your_password',
    'driver': 'ODBC Driver 17 for SQL Server'
}
```
### 6. Correr o projeto 
```
python backend/app.py
```

## Demo
https://youtu.be/ameYtxM-Pw8?si=nmC15kzUjyJjZP6c

## Evaluation
17.4

## Authors
* [Henrique Teixeira] - [@henriqueft04]
* [Maria Linhares] - [@MariaLinhares]

---

Universidade de Aveiro, Ano letivo 2023/2024
