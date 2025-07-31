from flask import session, redirect, url_for
from modulos.utils.console import CorFonte
alert = None

class AlertaMsg:
    def __init__(self):
        self.cnpj_invalido = self.cnpj_invalido
        self.cnpj_ja_existente = self.cnpj_ja_existente
        self.cad_fornecedor_realizado = self.cad_fornecedor_realizado

    @staticmethod
    def cadastro_cliente_realizado():
        print("class AlertaMsg: cadastro_cliente_realizado()")
        session["alert"] = (
            f'<div id = "alert" class="alert alert-success", '
            f'role="alert">Cadastro Realizado Com Sucesso!</div>'
        )
        return redirect(url_for("cadastrar_fornecedores"))

    @staticmethod
    def erro_ao_cadastrar_cliente(msg_erro):
        print("class AlertaMsg: erro_ao_cadastrar_cliente()")
        session["alert"] = (
            f'<div id = "alert" class="alert alert-danger", '
            f'role="alert">Erro ao Cadastrar Cliente: {msg_erro}</div>'
        )
        return redirect(url_for("cadastrar_fornecedores"))

    @staticmethod
    def cep_invalido(cep):
        print("class AlertaMsg: cep_invalido()")
        session["alert"] = (
            f'<div id = "alert" class="alert alert-danger", '
            f'role="alert">CEP INVALIDO: CEP {cep}</div>'
        )
        return redirect(url_for("cadastrar_fornecedores"))

    @staticmethod
    def produto_ja_cadastrado(ean):
        print("class AlertaMsg: produto_ja_cadastrado()")
        session["alert"] = (
            f'<div id = "alert" class="alert alert-danger", '
            f'role="alert">PRODUTO JÁ CADASTRADO: EAN {ean}</div>'
        )
        return redirect(url_for("cadastrar_produtos"))

    @staticmethod
    def produto_incluido_na_tabela(ean, descricao):
        print("class AlertaMsg: produto_incluido_na_tabela()")
        session["alert"] = (
            f'<div id = "alert" class="alert alert-success", '
            f'role="alert">PRODUTO INCLUIDO NA TABELA: EAN {ean} | {descricao}</div>'
        )
        return redirect(url_for("cadastrar_produtos"))

    @staticmethod
    def produto_ja_digitado():
        print("class AlertaMsg: produto_ja_digitado()")
        session["alert"] = (
            f'<div id = "alert" class="alert alert-danger", role="alert">PRODUTO JÁ DIGITADO</div>'
        )
        # return redirect(url_for('cadastrar_produtos'))

    @staticmethod
    def campos_em_branco():
        print(
            CorFonte.fonte_amarela()
            + "class AlertaMsg: campos_em_branco()"
            + CorFonte.reset_cor()
        )
        session["alert"] = (
            f'<div id = "alert" class="alert alert-danger", '
            f'role="alert">TODOS OS CAMPOS DEVEM SER PREENCHIDOS</div>'
        )
        return redirect(url_for("cadastrar_produtos"))

    @staticmethod
    def campo_nf_em_branco():
        print(
            CorFonte.fonte_amarela()
            + "class AlertaMsg: campos_em_branco()"
            + CorFonte.reset_cor()
        )
        session["alert"] = (
            f'<div id = "alert" class="alert alert-danger", '
            f'role="alert">TODOS OS CAMPOS DEVEM SER PREENCHIDOS</div>'
        )
        return redirect(url_for("cadastrar_produtos"))

    @staticmethod
    def ean_ja_digitado(ean):
        print(
            CorFonte.fonte_amarela()
            + "class AlertaMsg: ean_ja_digitado()"
            + CorFonte.reset_cor()
        )
        session["alert"] = (
            f'<div id = "alert" class="alert alert-danger", '
            f'role="alert">EAN {ean} JÁ CONSTA NA TABELA DE ITENS A CADASTRAR</div>'
        )
        return redirect(url_for("cadastrar_produtos"))

    def item_disponivel(ean):
        print(
            CorFonte.fonte_amarela()
            + "class AlertaMsg: Item disponivel()"
            + CorFonte.reset_cor()
        )
        session["alert"] = (
            f'<div id = "alert" class="alert alert-danger", '
            f'role="alert">EAN {ean} JÁ CONSTA NA TABELA DE ITENS A CADASTRAR</div>'
        )
        return redirect(url_for("cadastrar_produtos"))


    @staticmethod
    def produto_cadastrado_com_sucesso():
        print(
            CorFonte.fonte_amarela()
            + "class AlertaMsg: produto_cadastrado_com_sucesso()"
            + CorFonte.reset_cor()
        )
        session["alert"] = (
            '<div id = "alert" class="alert alert-success", '
            'role="alert">PRODUTO CADASTRADO COM SUCESSO</div>'
        )
        return redirect(url_for("cadastrar_produtos"))

    @staticmethod
    def fornecedor_invalido_cad_prod():
        print(
            CorFonte.fonte_amarela()
            + "class AlertaMsg: fornecedor_invalido_cad_prod()"
            + CorFonte.reset_cor()
        )
        session["alert"] = (
            '<div id="alert" class="alert alert-danger" '
            'role="alert">INSIRA UM FORNECEDOR VÁLIDO</div>'
        )
        return redirect(url_for("cadastrar_produtos"))

    @staticmethod
    def cad_fornecedor_realizado():
        print(
            CorFonte.fonte_amarela()
            + "class AlertaMsg: cad_fornecedor_realizado()"
            + CorFonte.reset_cor()
        )
        session["alert"] = (
            '<div id="alert" class="alert alert-success", role="alert">CADASTRO REALIZADO!</div>'
        )
        return redirect(url_for("cadastrar_fornecedores"))

    @staticmethod
    def fornecedor_invalido():
        print(
            CorFonte.fonte_amarela()
            + "class AlertaMsg: fornecedor_invalido()"
            + CorFonte.reset_cor()
        )
        session["alert"] = (
            '<div id="alert" class="alert alert-danger" role="alert">INSIRA UM FORNECEDOR VÁLIDO</div>'
        )
        return redirect(url_for("cadastrar_fornecedores"))

    @staticmethod
    def cnpj_invalido():
        print(
            CorFonte.fonte_amarela()
            + "class AlertaMsg: cnpj_invalido()"
            + CorFonte.reset_cor()
        )
        session["alert"] = (
            '<div id = "alert" class="alert alert-danger" role="alert">CNPJ INVALIDO!</div>'
        )
        return redirect(url_for("cadastrar_fornecedores"))

    @staticmethod
    def cnpj_ja_existente():
        print(
            CorFonte.fonte_amarela()
            + "class AlertaMsg: cnpj_ja_existente()"
            + CorFonte.reset_cor()
        )
        session["alert"] = (
            '<div id = "alert" class="alert alert-danger" role="alert">CNPJ JA EXISTENTE!</div>'
        )
        return redirect(url_for("cadastrar_fornecedores"))

    @staticmethod
    def cadastro_inexistente():
        print(
            CorFonte.fonte_amarela()
            + "class AlertaMsg: cadastro_inexistente()"
            + CorFonte.reset_cor()
        )
        session["alert"] = (
            '<div id = "alert" class="alert alert-danger" role="alert">CADASTRO INEXISTENTE</div>'
        )
        return redirect(url_for("gerar_ordem_de_compra"))