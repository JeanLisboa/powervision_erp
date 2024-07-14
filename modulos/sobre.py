
"""



import random

def gera_cnpj():
    # Gera os 8 primeiros dígitos do CNPJ
    n = [random.randint(0, 9) for _ in range(8)]

    # Primeiro dígito verificador
    n.append((n[0] * 6 + n[1] * 7 + n[2] * 8 + n[3] * 9 + n[4] * 2 + n[5] * 3 + n[6] * 4 + n[7] * 5) % 11)
    if n[-1] == 10:
        n[-1] = 0

    # Segundo dígito verificador
    n.append((n[0] * 5 + n[1] * 6 + n[2] * 7 + n[3] * 8 + n[4] * 9 + n[5] * 2 + n[6] * 3 + n[7] * 4 + n[8] * 5) % 11)
    if n[-1] == 10:
        n[-1] = 0

    # Formata o CNPJ
    cnpj = ''.join(map(str, n[:8])) + '.' + ''.join(map(str, n[8:12])) + '/0001-' + ''.join(map(str, n[12:]))

    return cnpj

# Exemplo de uso
cnpj = gera_cnpj()
print("CNPJ gerado:", cnpj)
class Teste:

    class SubClass(object):
        def teste(self):
            print("teste")
        def teste2(self):
            print("teste2")

"""

from datetime import date

data = date.today()

print(data)
print(type(data))




