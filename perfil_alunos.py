
import dash
import pandas as pd
import plotly.express as px
from dash import dcc, Output, callback, Input
from dash import html

"""
Análise Perfil dos Alunos
"""

df_perfil_alunos = pd.read_csv('perfil_alunos.csv')

# Analise dos dados

faixa_etaria = df_perfil_alunos['Qual sua faixa etária (idade)?'].value_counts().reset_index()
faixa_etaria.columns = ['Qual sua faixa etária (idade)?', 'Número de Alunos']

genero = df_perfil_alunos['Gênero:'].value_counts().reset_index()
genero.columns = ['Gênero:', 'Número de Alunos']

sabe_programar = df_perfil_alunos['Você possui alguma experiência na Área de Programação?'].value_counts().reset_index()
sabe_programar.columns = ['Você possui alguma experiência na Área de Programação?', 'Número de Alunos']

pri_vez = df_perfil_alunos['É a primeira vez que você cursa a disciplina de Programação Estruturada?'].value_counts().reset_index()
pri_vez.columns = ['É a primeira vez que você cursa a disciplina de Programação Estruturada? ', 'Número de Alunos']

motivo = df_perfil_alunos['Qual o principal motivo para você ter escolhido o curso de Bacharelado em Ciência da Computação?'].value_counts().reset_index()
motivo.columns = ['Qual o principal motivo para você ter escolhido o curso de Bacharelado em Ciência da Computação? ', 'Número de Alunos']

tempo_dedicacao = df_perfil_alunos['Quantas horas por semana, aproximadamente, você pode dedicar aos estudos (excetuando as horas de aula)?'].value_counts().reset_index()
tempo_dedicacao.columns = ['Quantas horas por semana, aproximadamente, você pode dedicar aos estudos (excetuando as horas de aula)?', 'Número de Alunos']

# Geraçao dos gráficos
fig_idade = px.pie(faixa_etaria, names='Qual sua faixa etária (idade)?', values='Número de Alunos',
             title='Faixa Etária dos Alunos')

fig_genero = px.pie(genero, names='Gênero:', values='Número de Alunos',
             title='Gênero')

fig_sabe_programar = px.pie(sabe_programar, names='Você possui alguma experiência na Área de Programação?', values='Número de Alunos',
             title='Experiência com Programação')

fig_pri_vez = px.pie(pri_vez, names='É a primeira vez que você cursa a disciplina de Programação Estruturada? ', values='Número de Alunos',
             title='Primeira vez na Disciplina?')

fig_motivo = px.pie(motivo, names='Qual o principal motivo para você ter escolhido o curso de Bacharelado em Ciência da Computação? ', values='Número de Alunos',
             title='Motivação para Fazer o Curso')

fig_tempo_dedicacao = px.pie(tempo_dedicacao, names='Quantas horas por semana, aproximadamente, você pode dedicar aos estudos (excetuando as horas de aula)?', values='Número de Alunos',
             title='Tempo de Dedicação aos Estudos')

style_h1 = {
    'font-family': 'arial,helvetica',  # Fonte
    'color': '#555',  # Cor do texto: cinza mais escuro
    'fontSize': '24px',  # Tamanho da fonte: 24px
    'marginTop': '20px'
}

style_h2 = {
    'font-family': 'arial,helvetica',  # Fonte
    'color': '#555',  # Cor do texto: cinza mais escuro
    'fontSize': '24px',  # Tamanho da fonte: 24px
    'marginTop': '20px'
}

style_div = {
    'font-family': 'arial,helvetica',  # Fonte
    'color': '#1C1C1C',  # Cor do texto: cinza mais escuro
    'fontSize': '18px',  # Tamanho da fonte: 24px
    'marginTop': '20px',
    'padding': '10px',
}

# Layout da Página

layout = html.Div([

    html.H1("Perfil dos Alunos", style=style_h1),

    html.Div([
        html.Div([
            html.Div([dcc.Graph(id='idade',figure=fig_idade)]),
            html.Div([dcc.Graph(id='genero',figure=fig_genero)])], style={'display': 'flex'}),
        html.Div(
            [html.Div([dcc.Graph(id='experiencia',figure=fig_sabe_programar)]),
             html.Div([dcc.Graph(id='experiencia',figure=fig_pri_vez)])], style={'display': 'flex'}),
        html.Div(
            [html.Div([dcc.Graph(id='motivo', figure=fig_motivo)]),
             html.Div([dcc.Graph(id='tempo_dedicacao', figure=fig_tempo_dedicacao)]),
             html.Div()], style={'display': 'flex'}),
    ]),

], style=style_div)
