# CRIAR, EDITAR E REMOVER USUÁRIOS, PERMISSOES E REGISTROS

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

class Admin:
    def __init__(self, nome, matricula, login, senha, perfil, datacadastro, ativo, observacoes):
        self.nome = nome
        self.matricula = matricula
        self.login = login
        self.senha = senha
        self.perfil = perfil
        self.datacadastro = datacadastro
        self.ativo = ativo
        self.observacoes = observacoes
