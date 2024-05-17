from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/clientes')
def clientes():
    return render_template('clientes.html')

@app.route('/fornecedores')
def fornecedores():
    return render_template('fornecedores.html')

@app.route('/nova-encomenda')
def nova_encomenda():
    return render_template('nova-encomenda.html')

@app.route('/encomendas')
def encomendas():
    return render_template('encomendas.html')

@app.route('/engarrafamentos')
def engarrafamentos():
    return render_template('engarrafamentos.html')

@app.route('/stock')
def stock():
    return render_template('stock.html')

if __name__ == "__main__":
    app.run(debug=True)
