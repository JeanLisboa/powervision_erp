from modulos.utils.console import CorFonte
from modulos.utils.queries import mydb, mycursor
from pycpfcnpj import cpfcnpj as validador_cnpj
from modulos.utils.buscadores import Buscadores


class Validadores:


    @staticmethod
    def valida_pedido_recebido(pedido):
        # 1 faz a query no banco de dados e retorna uma lista com os itens do pedido
        print(
            CorFonte.fonte_amarela()
            + "class Validadores | metodo valida_pedido_recebido"
            + CorFonte.reset_cor()
        )

        lista_itens = []
        query = f"SELECT * FROM ORDEM_COMPRA WHERE ORDEM_COMPRA  = '{pedido}'"
        mydb.connect()
        mycursor.execute(query)
        itens_ordem_de_compra = mycursor.fetchall()
        mydb.commit()
        valida_itens = ""

        try:
            if itens_ordem_de_compra:
                for i in itens_ordem_de_compra:
                    item_zip = (i[7], i[9])
                    lista_itens.append(item_zip)

            return lista_itens
        except Exception as e:
            print(f"Erro: {e}")
            return False

    @staticmethod
    def valida_status_pedido(pedido):
        print(CorFonte.fonte_amarela() + "class Validadores | metodo valida_status_pedido" + CorFonte.reset_cor())
        lista_itens = []
        # 1 faz a query no banco de dados e retorna uma lista com os itens do pedido

        query = f"SELECT * FROM ORDEM_COMPRA WHERE ORDEM_COMPRA  = '{pedido}'"
        mydb.connect()
        mycursor.execute(query)
        itens_ordem_de_compra = mycursor.fetchall()
        mydb.commit()
        valida_itens = ""
        for i in itens_ordem_de_compra:
            print(i)
        print("-------------------------------")
        try:
            return itens_ordem_de_compra
        except Exception as e:
            print(f"Erro: {e}")
            return False

    ordem_compra = ""

    @staticmethod
    def valida_cnpj(cnpj):
        print(
            CorFonte.fonte_amarela()
            + "class Validadores | metodo valida_cnpj"
            + CorFonte.reset_cor()
        )
        print("class Validadores | método valida_cnpj")
        print(f"cnpj original {cnpj}")
        cnpj = str(cnpj)
        print(f"cnpj convertido {cnpj}")
        return validador_cnpj.validate(cnpj)

    @staticmethod
    def valida_inscricao_estadual(insc_estadual):
        print(
            CorFonte.fonte_amarela()
            + "class Validadores | metodo valida_inscricao_estadual"
            + CorFonte.reset_cor()
        )

        insc_estadual = str(insc_estadual)
        if len(insc_estadual) != 9:
            return False
        else:
            return True

    class ValidaStatusPedido:

        def __init__(self):
            pass

        @staticmethod
        def validacao_1(status_ordem):
            print(
                CorFonte.fonte_amarela()
                + "class ValidaStatusPedido | metodo validacao_1"
                + CorFonte.reset_cor()
            )
            print(
                "class ValidaStatusPedido | metodo validacao_1"
                "Objetivo: Verificar se o xml está no servidor"
            )

            if status_ordem is True:
                return True
            else:  # xml nao localizado
                return False

        @staticmethod
        def validacao_2(cnpj):
            print(
                CorFonte.fonte_amarela()
                + "class ValidaStatusPedido | metodo validacao_2"
                + CorFonte.reset_cor()
            )
            print(
                "class ValidaStatusPedido | metodo validacao_2"
                "Objetivo: Verificar se o fornecedor está cadastrado"
            )
            # print(fonte_amarela + 'VALIDAÇÃO 2: VERIFICAR SE O FORNECEDOR ESTÁ CADASTRADO' + reset_cor)
            if Buscadores.buscar_cnpj(cnpj) is True:
                print(
                    CorFonte.fonte_azul()
                    + f"cnpj encontrado: {cnpj}"
                    + CorFonte.reset_cor()
                )
                # print(fonte_verde + 'VALIDAÇÃO 2 concluída' + reset_cor)
                return True
            else:
                print("cnpj não encontrado")
                # lst_nf = ['Fornecedor não encontrado']
                return False

        @staticmethod
        def validacao_3(status_ordem, ordem):
            print(
                CorFonte.fonte_amarela()
                + "class ValidaStatusPedido | metodo validacao_3"
                + CorFonte.reset_cor()
            )
            print(
                "class ValidaStatusPedido | metodo validacao_3"
                "Objetivo: Verificar se o pedido está aberto"
            )
            # print(fonte_amarela + 'VALIDÇÃO 3: VERIFICAR SE O PEDIDO ESTÁ EM ABERTO' + reset_cor)
            if status_ordem is True:
                # print(CorFonte.fonte_azul() + f'Pedido {ordem} aberto' + CorFonte.fonte_azul())
                # print(fonte_verde + 'VALIDAÇÃO 3 concluída' + reset_cor)
                return True
            else:
                print(
                    CorFonte.fonte_vermelha()
                    + "Pedido encerrado ou cancelado"
                    + CorFonte.reset_cor()
                )
                return False

        @staticmethod
        def validacao_4(nf, ordem):
            print(
                CorFonte.fonte_amarela()
                + "class ValidaStatusPedido | metodo validacao_4"
                + CorFonte.reset_cor()
            )
            print(
                "class ValidaStatusPedido | metodo validacao_4"
                "Objetivo: Verificar ordem x nf"
            )
            # print(fonte_amarela + 'VALIDAÇÃO 4: VALIDAR PEDIDO X NF' + reset_cor)
            itens_nf = Buscadores.Xml.buscar_linhas_nf(str(nf))
            # print(f'itens_nf = {itens_nf}')
            # print(fonte_amarela + 'VALIDAÇÃO 4: (2) RECEBER OC, CRIAR LISTA DE EAN E PRECO' + reset_cor)
            itens_oc = Validadores.valida_pedido_recebido(ordem)
            # print(f'itens_oc = {itens_oc}')
            # print(fonte_amarela + 'VALIDAÇÃO 4: (3) COMPARAR AS DUAS LISTAS' + reset_cor)
            # maior_dif_permitida = modulos.admin.maior_dif_permitida
            maior_dif_permitida = 0.2
            # print(f'maior_dif_permitida = {maior_dif_permitida}')
            cont_preco_fora_politica = 0

            # print('for ean_oc in itens_oc:')
            for ean_oc in itens_oc:  # 'oc' = 'ordem de compra'
                # print(f'ean pesquisado: {ean_oc[0]}')

                for ean_nf in itens_nf:
                    # print(f'ean_nf = {ean_nf[0]}')
                    if ean_oc[0] == ean_nf[0]:
                        # print(CorFonte.fonte_azul() + f'ean_oc[0] = {ean_oc[0]} || ean_oc[1] = {ean_oc[1]}'
                        #                    f'ean_nf[0] = {ean_nf[0]} || ean_nf[1] = {ean_nf[1]}' + CorFonte.reset_cor())
                        if (ean_oc[1] - ean_nf[1]) <= maior_dif_permitida:
                            print(
                                CorFonte.fonte_verde()
                                + f"preco dentro da politica"
                                + CorFonte.reset_cor()
                            )
                        else:
                            print(
                                CorFonte.fonte_vermelha()
                                + f"preco fora da politica"
                                + CorFonte.reset_cor()
                            )
                            cont_preco_fora_politica += 1

            if cont_preco_fora_politica == 0:
                return True
            else:
                return False

class ValidaStatusPedido:

    def __init__(self):
        pass

    @staticmethod
    def validacao_1(status_ordem):
        print(
            CorFonte.fonte_amarela()
            + "class ValidaStatusPedido | metodo validacao_1"
            + CorFonte.reset_cor()
        )
        print(
            "class ValidaStatusPedido | metodo validacao_1"
            "Objetivo: Verificar se o xml está no servidor"
        )

        if status_ordem is True:
            return True
        else:  # xml nao localizado
            return False

    @staticmethod
    def validacao_2(cnpj):
        print(
            CorFonte.fonte_amarela()
            + "class ValidaStatusPedido | metodo validacao_2"
            + CorFonte.reset_cor()
        )
        print(
            "class ValidaStatusPedido | metodo validacao_2"
            "Objetivo: Verificar se o fornecedor está cadastrado"
        )
        # print(fonte_amarela + 'VALIDAÇÃO 2: VERIFICAR SE O FORNECEDOR ESTÁ CADASTRADO' + reset_cor)
        if Buscadores.buscar_cnpj(cnpj) is True:
            print(
                CorFonte.fonte_azul()
                + f"cnpj encontrado: {cnpj}"
                + CorFonte.reset_cor()
            )
            # print(fonte_verde + 'VALIDAÇÃO 2 concluída' + reset_cor)
            return True
        else:
            print("cnpj não encontrado")
            # lst_nf = ['Fornecedor não encontrado']
            return False

    @staticmethod
    def validacao_3(status_ordem, ordem):
        print(
            CorFonte.fonte_amarela()
            + "class ValidaStatusPedido | metodo validacao_3"
            + CorFonte.reset_cor()
        )
        print(
            "class ValidaStatusPedido | metodo validacao_3"
            "Objetivo: Verificar se o pedido está aberto"
        )
        # print(fonte_amarela + 'VALIDÇÃO 3: VERIFICAR SE O PEDIDO ESTÁ EM ABERTO' + reset_cor)
        if status_ordem is True:
            # print(CorFonte.fonte_azul() + f'Pedido {ordem} aberto' + CorFonte.fonte_azul())
            # print(fonte_verde + 'VALIDAÇÃO 3 concluída' + reset_cor)
            return True
        else:
            print(
                CorFonte.fonte_vermelha()
                + "Pedido encerrado ou cancelado"
                + CorFonte.reset_cor()
            )
            return False

    @staticmethod
    def validacao_4(nf, ordem):
        print(
            CorFonte.fonte_amarela()
            + "class ValidaStatusPedido | metodo validacao_4"
            + CorFonte.reset_cor()
        )
        print(
            "class ValidaStatusPedido | metodo validacao_4"
            "Objetivo: Verificar ordem x nf"
        )
        # print(fonte_amarela + 'VALIDAÇÃO 4: VALIDAR PEDIDO X NF' + reset_cor)
        itens_nf = Buscadores.Xml.buscar_linhas_nf(str(nf))
        # print(f'itens_nf = {itens_nf}')
        # print(fonte_amarela + 'VALIDAÇÃO 4: (2) RECEBER OC, CRIAR LISTA DE EAN E PRECO' + reset_cor)
        itens_oc = Validadores.valida_pedido_recebido(ordem)
        # print(f'itens_oc = {itens_oc}')
        # print(fonte_amarela + 'VALIDAÇÃO 4: (3) COMPARAR AS DUAS LISTAS' + reset_cor)
        # maior_dif_permitida = modulos.admin.maior_dif_permitida
        maior_dif_permitida = 0.2
        # print(f'maior_dif_permitida = {maior_dif_permitida}')
        cont_preco_fora_politica = 0

        # print('for ean_oc in itens_oc:')
        for ean_oc in itens_oc:  # 'oc' = 'ordem de compra'
            # print(f'ean pesquisado: {ean_oc[0]}')

            for ean_nf in itens_nf:
                # print(f'ean_nf = {ean_nf[0]}')
                if ean_oc[0] == ean_nf[0]:
                    # print(CorFonte.fonte_azul() + f'ean_oc[0] = {ean_oc[0]} || ean_oc[1] = {ean_oc[1]}'
                    #                    f'ean_nf[0] = {ean_nf[0]} || ean_nf[1] = {ean_nf[1]}' + CorFonte.reset_cor())
                    if (ean_oc[1] - ean_nf[1]) <= maior_dif_permitida:
                        print(
                            CorFonte.fonte_verde()
                            + f"preco dentro da politica"
                            + CorFonte.reset_cor()
                        )
                    else:
                        print(
                            CorFonte.fonte_vermelha()
                            + f"preco fora da politica"
                            + CorFonte.reset_cor()
                        )
                        cont_preco_fora_politica += 1

        if cont_preco_fora_politica == 0:
            return True
        else:
            return False

class ValidacoesCadastroProduto:
    """

    """
    @staticmethod
    def valida_ean_na_lista(lista_cadastro_produto, ean):
        print(CorFonte.fonte_amarela()
            + "função valida_ean_na_lista"
            + CorFonte.reset_cor())

        try:
            if not lista_cadastro_produto:  # ou if lista_cadastro_produto == []
                print("lista vazia")
                return True

            for i in lista_cadastro_produto:  # verifica se o item ja existe no pedido
                print(f"informações para incluir na tabela\n {i}")
                if i[1][1] == ean:
                    print(f"ean {ean} ja existente na lista de itens a cadastrar")
                    return False
                else:
                    print("ean ainda nao digitado.")
                    return True
        except Exception as e:
            print(e)

    @staticmethod
    def valida_campos(fornecedor, ean, descricao, unidade, valor, categoria, usuario):
        print("função valida_campos (verifica se todos os campos foram preenchidos)")
        if (
            fornecedor == "Selecionar um fornecedor"
            or ean == ""
            or ean is None
            or descricao == ""
            or descricao is None
            or unidade == ""
            or unidade is None
            or valor == ""
            or valor is None
            or categoria == ""
            or categoria is None
            or usuario == ""
            or usuario is None
        ):
            print("há um ou mais campos em branco ")
            return False
        else:
            print("todos os campos preenchidos")
            return True

    @staticmethod
    def valida_ean_no_banco(ean):
        print("função valida_ean_no_banco")
        # valida se o ean existe no banco de dados
        if Buscadores.buscar_produto_pelo_ean(ean) is False:
            print(">>ean ja existente no banco de dados")
            return False
        else:
            print(">>ean disponível para cadastro")
            return True

