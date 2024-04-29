from flask import Flask, render_template, redirect, url_for, request, jsonify, send_file, session, get_flashed_messages, flash
from modulos import compras, comercial, fiscal, financeiro, logistica

app = Flask(__name__)
@app.route('/')
def main():
    return render_template('homepage.html')


@app.route('/admin', methods=['POST', 'GET'])
def admin():
    return render_template('admin.html')


@app.route('/cadastrar_fornecedores', methods=['POST', 'GET'])
def cadastrar_fornecedores():
    compras.Compras.cadastrar_fornecedores(self="Compras")

    return render_template('cadastrar_fornecedores.html')

@app.route('/cadastrar_produtos', methods=['POST', 'GET'])
def cadastrar_produtos():
    return render_template('cadastrar_produtos.html')

@app.route('/cadastrar_compras', methods=['POST', 'GET'])
def cadastrar_compras():
    return render_template('cadastrar_compras.html')

@app.route('/relatorios_compras', methods=['POST', 'GET'])
def relatorios_compras():
    return render_template('relatorios_compras.html')


@app.route('/comercial', methods=['POST', 'GET'])
def comercial():
    return render_template('comercial.html')


@app.route('/fiscal', methods=['POST', 'GET'])
def fiscal():
    return render_template('fiscal.html')

@app.route('/financeiro', methods=['POST', 'GET'])
def financeiro():
    return render_template('financeiro.html')

@app.route('/logistica', methods=['POST', 'GET'])
def logistica():
    return render_template('logistica.html')

@app.route('/pricing', methods=['POST', 'GET'])
def pricing():
    return render_template('pricing.html')

@app.route('/ajuda', methods=['POST', 'GET'])
def ajuda():
    return render_template('ajuda.html')

@app.route('/sobre', methods=['POST', 'GET'])
def sobre():
    return render_template('sobre.html')

@app.route('/contato', methods=['POST', 'GET'])
def contato():
    return render_template('contato.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    return render_template('login.html')

@app.route('/teste', methods=['POST', 'GET'])
def teste():
    return render_template('teste.html')


if __name__ == "__main__":
    app.run(debug=True)
