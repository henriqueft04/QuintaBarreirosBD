from flask import Blueprint, render_template, jsonify

main_blueprint = Blueprint('main', __name__, template_folder='../templates')

@main_blueprint.route('/')
def index():
    return render_template('index.html')

@main_blueprint.route('/data')
def get_data():
    data = {
        'message': 'Dados carregados com sucesso!',
        'items': ['Item 1', 'Item 2', 'Item 3']
    }
    return jsonify(data)
