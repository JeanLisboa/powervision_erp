from flask import Flask, render_template, redirect, url_for, request, jsonify, send_file, session, get_flashed_messages, flash
from modulos import compras, comercial, fiscal, financeiro, logistica
from flask_wtf.csrf import CSRFProtect
from forms import Mod_Compras, Mod_Comercial, Mod_Pricing
app = Flask(__name__)
app.config['SECRET_KEY'] = "f92ed5835155e99cc60e328de2cce349830e28984c160jj3gg2"
csrf = CSRFProtect(app)
@app.route('/')
def main():
    return render_template('homepage.html')


@app.route('/admin', methods=['POST', 'GET'])
def admin():
    return render_template('admin.html')



@app.route('/cadastrar_fornecedores', methods=['POST', 'GET'])
def cadastrar_fornecedores():
    form_fornecedores = Mod_Compras.CadFornecedores()
    return render_template('compras/cadastrar_fornecedores.html', form_fornecedores=form_fornecedores)

@app.route('/cadastrar_produtos', methods=['POST', 'GET'])
def cadastrar_produtos():
    form_cad_produtos = Mod_Compras.CadProduto()
    return render_template('compras/cadastrar_produtos.html', form_cad_produtos=form_cad_produtos)

@app.route('/gerar_ordem_compra', methods=['POST', 'GET'])
def gerar_ordem_compra():
    form_gerar_ordem_compra = Mod_Compras.GerarOrdemCompra()
    return render_template('compras/gerar_ordem_compra.html', form_gerar_ordem_compra=form_gerar_ordem_compra)

@app.route('/relatorios_compras', methods=['POST', 'GET'])
def relatorios_compras():
    return render_template('compras/relatorios_compras.html')


@app.route('/cadastrar_clientes', methods=['POST', 'GET'])
def cadastrar_clientes():
    form_cad_clientes = Mod_Comercial.CadastrarCliente()
    return render_template('comercial/cadastrar_clientes.html', form_cad_clientes=form_cad_clientes)


@app.route('/incluir_pedido_venda', methods=['POST', 'GET'])
def incluir_pedido_venda():
    form_incluir_pedido_venda = Mod_Comercial.IncluirPedidoVenda()
    return render_template('comercial/incluir_pedido_venda.html', form_incluir_pedido_venda=form_incluir_pedido_venda)


@app.route('/cadastrar_tabela', methods=['POST', 'GET'])
def cadastrar_tabela():
    form_cadastrar_tabela = Mod_Pricing.CadastrarTabela()
    return render_template('pricing/cadastrar_tabela.html', form_cadastrar_tabela=form_cadastrar_tabela)

@app.route('/financeiro', methods=['POST', 'GET'])
def financeiro():
    return render_template('financeiro.html')

@app.route('/logistica', methods=['POST', 'GET'])
def logistica():
    return render_template('logistica.html')

@app.route('/fiscal', methods=['POST', 'GET'])
def fiscal():
    return render_template('fiscal.html')

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
