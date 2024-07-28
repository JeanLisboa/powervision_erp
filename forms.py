from wtforms import StringField, SubmitField, SelectField, IntegerField, FloatField, HiddenField
from wtforms.validators import DataRequired, Email, Disabled, Length, ReadOnly, NumberRange
from flask_wtf import FlaskForm
from datetime import date

import geral

os_date = date.today()


class ModAdmin:
    class RegraNegocio(FlaskForm):
        recebe_parcial_item = SelectField("Recebe Parcial do Item", choices=['Sim', 'Não'], validate_choice='sim')
        recebe_parcial_pedido = SelectField("Recebe Parcial do Pedido", choices=['Sim', 'Não'], validate_choice='sim')
        min_prazo_pag = IntegerField("Prazo Minimo de Pagamento (Em Dias)", validators=[DataRequired(), NumberRange(min=0)])
        maior_dif_permitida = FloatField("Maior diferença permitida", validators=[DataRequired(), NumberRange(min=0.01)])
        menor_dif_permitida = FloatField("Menor diferença permitida", validators=[DataRequired(), NumberRange(min=0.01)])

        botao_salvar = SubmitField('Salvar Alterações')
        botao_editar = SubmitField('Editar')


class ModCompras:
    class AnalisarOrdemCompra(FlaskForm):
        data = StringField("Data", validators=[DataRequired(), ReadOnly()])
        pesquisar_nf = StringField("Nota Fiscal")
        razao_social = StringField("Fornecedor")
        ordem_compra = StringField("Ordem")
        botao_pesquisar_notafiscal = SubmitField('Pesquisar Nota Fiscal')
        botao_pesquisar_ordem_de_compra = SubmitField('Pesquisar')
        botao_liberar_recebimento = SubmitField('Liberar Para Recebimento')
        botao_recusar_recebimento = SubmitField('Recusar')

    class CadFornecedores(FlaskForm):
        cod_fornecedor = StringField("Código", validators=[ReadOnly()])
        razao_social = StringField("Nome Fantasia", validators=[DataRequired()])
        # razao_social = StringField("Razão Social", validators=[DataRequired()])
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
        buscar_fornecedor = geral.Buscadores.OrdemCompra.buscar_fornecedor()
        cod_produto = StringField("Código: ", validators=[Disabled()])
        data = StringField("Data", validators=[DataRequired(), ReadOnly()])
        ean = StringField("EAN", validators=[Length(13)])
        descricao = StringField("Descrição")
        fornecedor = SelectField("Fornecedor", choices=['Selecionar um fornecedor'] + [f[0] for f in buscar_fornecedor], validators=[DataRequired()])
        unidade = SelectField(coerce=str, choices=['', 'KG', 'G', 'CX', 'UN', 'L', 'M', 'CM'],
                              validators=[ReadOnly()])

        valor = FloatField("Valor", validators=[NumberRange(min=0.01)])
        categoria = SelectField(coerce=str, choices=['','VESTUARIO', 'BEBIDAS', 'ALIMENTOS', 'HIGIENE', 'OUTROS'])
        botao_incluir_item = SubmitField('Incluir Item')
        botao_submit_cad_prod = SubmitField('Cadastrar')
        botao_cancelar_cad_prod = SubmitField('cancelar')
        botao_excluir_cad_prod = SubmitField('excluir')

        # esta linha serve para armazenar o valor do produto para utilizar no botao editar linha do cadastro produto
        botao_editar_cad_prod = SubmitField('Editar')
        valor_produto = HiddenField('Valor do Produto')

    class GerarOrdemCompra(FlaskForm):
        buscar_fornecedor = geral.Buscadores.OrdemCompra.buscar_fornecedor()
        data = StringField("Data", validators=[DataRequired(), ReadOnly()])
        ordem_compra = StringField("Ordem de Compra", validators=[ReadOnly()])
        codigo = StringField("Código")
        fornecedor = SelectField("Fornecedor", choices=['Selecionar um fornecedor'] + [f[0] for f in buscar_fornecedor],
                                 validators=[DataRequired()])
        # fornecedor = StringField("Fornecedor")
        ean = StringField("EAN")
        descricao = StringField("Descrição", validators=[ReadOnly()])
        unidade = StringField("Un", validators=[ReadOnly()])
        categoria = StringField("Categoria", validators=[ReadOnly()])
        quantidade = IntegerField("Quantidade", validators=[DataRequired(), NumberRange(min=1)])
        preco_unitario = FloatField("Preço Unitário", validators=[NumberRange(min=1.00)])
        preco_historico = FloatField("Preço Histórico", validators=[DataRequired(), ReadOnly()])
        ultimo_preco = FloatField("Ultimo Preço", validators=[DataRequired(), ReadOnly()])
        preco_medio = FloatField("Preço Médio", validators=[DataRequired(), ReadOnly()])
        botao_consulta = SubmitField('Consulta')
        botao_limpar_ordem = SubmitField('Limpar Ordem')
        botao_pesquisar_item = SubmitField('Pesquisar Código')
        botao_pesquisar_fornecedor = SubmitField('Pesquisar Fornecedor')
        botao_incluir_item = SubmitField('Incluir Item')
        botao_selecionar_item = SubmitField('Selecionar')
        botao_submit_compra = SubmitField('Gerar Ordem de Compra')

    class BuscarItemOrdemCompra(FlaskForm):
        data = StringField("Data", validators=[DataRequired(), ReadOnly()])
        codigo = StringField("Código")
        ordem_compra = StringField("Ordem de Compra", validators=[ReadOnly()])
        fornecedor = StringField("Fornecedor", validators=[ReadOnly()])
        ean = StringField("EAN")
        descricao = StringField("Descrição", validators=[ReadOnly()])
        unidade = StringField("Unidade", validators=[ReadOnly()])
        categoria = StringField("Categoria", validators=[ReadOnly()])
        botao_pesquisar_item = SubmitField('Pesquisar')

    class RelatoriosCompras(FlaskForm):
        pass


class Mod_Comercial:

    class CadastrarCliente(FlaskForm):
        data = StringField("Data", validators=[DataRequired(), ReadOnly()])
        cod_cliente = StringField("Código", validators=[Disabled()])
        razao_social = StringField("Razão Social", validators=[DataRequired()])
        razao_social = StringField("Nome Fantasia", validators=[DataRequired()])
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
        razao_social = StringField("Nome Fantasia", validators=[ReadOnly()])
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

class Mod_Logistica:
    class EntradaOrdemCompra(FlaskForm):
        data = StringField("Data", validators=[DataRequired(), ReadOnly()])
        nf = IntegerField("NF", validators=[NumberRange(min=1)])
        razao_social = StringField("Nome Fantasia")
        ordem_compra = IntegerField("Ordem de Compra", validators=[NumberRange(min=1)])
        cnpj = IntegerField("CNPJ", validators=[Length(14, 14)])
        botao_pesquisar_ordem_compra = SubmitField('Pesquisar Ordem')
        botao_limpar_pesquisa = SubmitField('Limpar')

    class Realizar_conferencia(FlaskForm):
        ordem_compra = StringField("Ordem de Compra")
        fornecedor = StringField("Fornecedor")
        botao_pesquisar_ordem_compra = SubmitField('Pesquisar')
        botao_limpar_pesquisa = SubmitField('Limpar')