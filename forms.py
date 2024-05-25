from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, Disabled, Length, ReadOnly
from flask_wtf import FlaskForm
from datetime import date

import geral

os_date = date.today()


class Mod_Compras:

    class CadFornecedores(FlaskForm):
        cod_fornecedor = StringField("Código", validators=[ReadOnly()])
        nome_fantasia = StringField("Nome Fantasia", validators=[DataRequired()])
        razao_social = StringField("Razão Social", validators=[DataRequired()])
        data = StringField("Data", validators=[DataRequired(), ReadOnly()])
        cnpj = StringField("CNPJ", validators=[DataRequired(), Length(14)])
        insc_estadual = IntegerField("Insc. Estadual", validators=[DataRequired(), Length(9)])
        email = StringField("Email", validators=[DataRequired()])
        cep = IntegerField("CEP", validators=[DataRequired(), Length(8, 8)])
        telefone = IntegerField("Telefone", validators=[DataRequired(), Length(10, 11)])
        endereco = StringField("Endereço", validators=[DataRequired()])
        municipio = StringField("Municipio", validators=[DataRequired()])
        uf = StringField("UF", validators=[DataRequired(), Length(2)])
        botao_submit_cad_fornecedor = SubmitField('Cadastrar')

    class CadProduto(FlaskForm):
        buscar_fornecedor = geral.Buscadores.buscar_fornecedor()
        cod_produto = StringField("Código: ", validators=[Disabled()])
        data = StringField("Data", validators=[DataRequired(), ReadOnly()])
        ean = StringField("EAN", validators=[DataRequired(), Length(13)])
        descricao = StringField("Descrição", validators=[DataRequired()])
        fornecedor = SelectField("Fornecedor", choices=['Selecionar um fornecedor'] + [f[0] for f in buscar_fornecedor], validators=[DataRequired()])
        unidade = SelectField(coerce=str, choices=['', 'KG', 'G', 'CX', 'UN', 'L', 'M', 'CM'],
                                validators=[DataRequired(), ReadOnly()])
        categoria = SelectField(coerce=str, choices=['','VESTUARIO', 'BEBIDAS', 'ALIMENTOS', 'HIGIENE', 'OUTROS'])
        botao_submit_cad_prod = SubmitField('Cadastrar')

    class GerarOrdemCompra(FlaskForm):
        data = StringField("Data", validators=[DataRequired(), ReadOnly()])
        ordem_compra = StringField("Ordem de Compra", validators=[ReadOnly()])
        codigo = StringField("Código")
        fornecedor = StringField("Fornecedor", validators=[ReadOnly()])
        ean = StringField("EAN")
        descricao = StringField("Descrição", validators=[ReadOnly()])
        unidade = StringField("Unidade", validators=[ReadOnly()])
        categoria = StringField("Categoria", validators=[ReadOnly()])
        quantidade = IntegerField("Quantidade", validators=[DataRequired()])
        botao_incluir_item = SubmitField('Incluir Item')
        botao_submit_compra = SubmitField('Gerar Ordem de Compra')

    class RelatoriosCompras(FlaskForm):
          pass

class Mod_Comercial:

    class CadastrarCliente(FlaskForm):
        data = StringField("Data", validators=[DataRequired(), ReadOnly()])
        cod_cliente = StringField("Código", validators=[Disabled()])
        razao_social = StringField("Razão Social", validators=[DataRequired()])
        nome_fantasia = StringField("Nome Fantasia", validators=[DataRequired()])
        cnpj = IntegerField("CNPJ", validators=[DataRequired(), Length(11, 14)], render_kw={'placeholder': '__.___.___/____-__'})
        insc_estadual = IntegerField("Insc. Estadual", validators=[DataRequired(), Length(14)])
        email = StringField("Email", validators=[DataRequired(), Email()])
        cep = IntegerField("CEP", validators=[DataRequired(), Length(8, 8)], render_kw={'placeholder': '_____-___'})
        telefone = IntegerField("Telefone", validators=[DataRequired(), Length(10, 11)], render_kw={'placeholder': '(__)____-____'})
        endereco = StringField("Endereço", validators=[DataRequired()])
        municipio = StringField("Municipio", validators=[DataRequired()])
        uf = StringField("UF", validators=[DataRequired(), Length(2)])
        tabela = SelectField("Tabela", choices=[], validators=[DataRequired(), ReadOnly()])
        botao_submit_cad_fornecedor = SubmitField('Cadastrar')

    class IncluirPedidoVenda(FlaskForm):
        data = StringField("Data", validators=[DataRequired(), ReadOnly()])
        cod_pedido = StringField("Código", validators=[Disabled()])
        cliente = StringField("Cliente", validators=[ReadOnly()])
        nome_fantasia = StringField("Nome Fantasia", validators=[ReadOnly()])
        cod_produto = StringField("Código", validators=[])
        ean = StringField("EAN", validators=[])
        descricao = StringField("Descrição", validators=[])
        unidade = StringField("Unidade", validators=[])
        quantidade = IntegerField("Quantidade", validators=[DataRequired()])
        botao_submit_cad_fornecedor = SubmitField('Incluir')



    class RelatorioComercial(FlaskForm):
        pass



class Mod_Pricing:
    class CadastrarTabela(FlaskForm):
        data = StringField("Data", validators=[DataRequired(), ReadOnly()])
        cod_tabela = StringField("Código", validators=[ReadOnly()])
        nome_tabela = StringField("Nome da Tabela", validators=[DataRequired()])
        botao_incluir_tabela = SubmitField('Incluir Tabela')
        botao_submit_cad_fornecedor = SubmitField('Cadastrar')
