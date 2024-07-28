# CRIAR, EDITAR E REMOVER USUÁRIOS, PERMISSOES E REGISTROS
from flask import render_template, request
from wtforms import StringField, SubmitField, SelectField, IntegerField, FloatField, HiddenField
from forms import ModAdmin

# CADASTRO DE USUÁRIO
# CODIGO(INCREMENTAL)
# NOME DO USUÁRIO
# MATRICULA
# LOGIN
# SENHA
# PERFIL (ADMINISTRADOR, VENDEDOR, COMPRAS, FINANCEIRO, LOGISTICA, GERAL(TODOS, EXCETO O ADMINISTRADOR))
# DATA DE CADASTRO
# ATIVO
# OBSERVAÇÕES

usuario = 'admin'
maior_dif_permitida = 0.2


def regra_negocio():
    form_regra_negocio = ModAdmin.RegraNegocio()
    min_prazo_pag = ModAdmin.RegraNegocio.min_prazo_pag
    recebe_parcial_pedido = ModAdmin.RegraNegocio.recebe_parcial_pedido
    recebe_parcial_item = ModAdmin.RegraNegocio.recebe_parcial_item
    maior_dif_permitida = ModAdmin.RegraNegocio.maior_dif_permitida
    menor_dif_permitida = ModAdmin.RegraNegocio.menor_dif_permitida

    try:
        if 'botao_salvar' in request.form:
            print('Botão Salvar acionado')

    except Exception as e:
        print(e)

    try:
        if 'botao_editar' in request.form:
            print('Botão Editar acionado')

    except Exception as e:
        print(e)




    return render_template('admin/regra_negocio.html',
                           form_regra_negocio=form_regra_negocio,
                           min_prazo_pag=min_prazo_pag,
                           recebe_parcial_pedido=recebe_parcial_pedido,
                           recebe_parcial_item=recebe_parcial_item,
                           maior_dif_permitida=maior_dif_permitida,
                           menor_dif_permitida=menor_dif_permitida
                                    )
