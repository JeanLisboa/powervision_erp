class CorFonte:
    """
        # configura cor de fonte no terminal

    """
    """
            # 38;2 especifica que o rgb será aplicado à cor da fonte e ';2' especifica que será aplicado a cor pelo rgb
        # 48;2 especifica que o rgb será aplicado à cor ao background e ';2' especifica que será aplicado a cor pelo rgb

    """


    @staticmethod
    def fonte_vermelha():
        return "\033[38;2;255;0;0;48;2;0;0;0m"  # erro

    @staticmethod
    def fonte_verde():  #
        return "\033[92m"

    @staticmethod
    def fonte_amarela():  # interação do usuário
        return "\033[93m"

    @staticmethod
    def fonte_azul():
        return "\033[34m"

    @staticmethod
    def fonte_azul_claro():  # acionamento de função
        return "\033[36m"

    @staticmethod
    def reset_cor():
        return "\033[0m"

