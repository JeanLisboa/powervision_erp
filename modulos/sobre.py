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


from flask import render_template
import pandas as pd
import plotly.express as px

def cronograma():
    # Criando dados de exemplo
    dados = [
        dict(Tarefa="Planejamento", Início="2024-05-01", Fim="2024-05-20", Responsável="Jean"),
        dict(Tarefa="Desenvolvimento", Início="2024-05-21", Fim="2026-03-31", Responsável="Jean"),
        dict(Tarefa="Testes", Início="2026-05-01", Fim="2026-05-30", Responsável="Jean"),
        dict(Tarefa="Implantação", Início="2026-06-01", Fim="2026-06-15", Responsável="Jean"),
        dict(Tarefa="Refatoração", Início="2026-07-01", Fim="2026-12-31", Responsável="Jean")
    ]

    df = pd.DataFrame(dados)

    # Criando o gráfico de Gantt
    fig = px.timeline(
        df,
        x_start="Início",
        x_end="Fim",
        y="Tarefa",
        color="Responsável",
        title="Gráfico de Gantt - Projeto",
        text="Responsável"
    )

    fig.update_yaxes(autorange="reversed")

    # Exporta o gráfico para HTML
    grafico_html = fig.to_html(full_html=False)

    # Passa o gráfico como variável para o template
    return render_template('sobre/cronograma.html', grafico=grafico_html)
