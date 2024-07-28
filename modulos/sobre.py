from flask import render_template

def ajuda():
    return render_template('sobre/ajuda.html')


def contato():
    return render_template('sobre/contato.html')

def sobre():
    return render_template('sobre/sobre.html')

