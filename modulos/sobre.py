from flask import render_template

def ajuda():
    video_id = "1idax6j0mlLy8YihkNCrSopzio6Cka26h"  # Substitua pelo ID do seu vídeo

    return render_template('sobre/ajuda.html', video_id=video_id)


def contato():
    return render_template('sobre/contato.html')

def sobre():
    return render_template('sobre/sobre.html')


def estrutura():
    return render_template('sobre/estrutura.html')


def backlog():
    return render_template('sobre/backlog.html')


def fluxograma():
    return render_template('sobre/fluxograma.html')
