
import pandas as pd
import plotly.express as px
from dash import callback, Output, Input
from dash import dcc, html
from dash import dash_table
import numpy as np
import plotly.graph_objs as go


# Análise dos Conhecimentos Prévios dos Alunos
# Lendo o arquivo CSV, que contem os dados sobre o conhecimentos prévios

df_habilidades_previas = pd.read_csv('conhecimentos_previos_com_nota.csv')

df_habilidades_previas['BASE_ALG'] = df_habilidades_previas['BASE_ALG'].str.replace(',', '.').astype(float)
df_habilidades_previas['BASE_DEC'] = df_habilidades_previas['BASE_DEC'].str.replace(',', '.').astype(float)
df_habilidades_previas['BASE_REC'] = df_habilidades_previas['BASE_REC'].str.replace(',', '.').astype(float)
df_habilidades_previas['BASE_ABS'] = df_habilidades_previas['BASE_ABS'].str.replace(',', '.').astype(float)
df_habilidades_previas['TOTAL_CP'] = df_habilidades_previas['TOTAL_CP'].str.replace(',', '.').astype(float)


data = {
    'ALUNO': df_habilidades_previas['Nome:'],
    'ALGORITMO': df_habilidades_previas['BASE_ALG'],
    'DECOMPOSIÇÃO': df_habilidades_previas['BASE_DEC'],
    'RECONHECIMENTO DE PADRÕES': df_habilidades_previas['BASE_REC'],
    'ABSTRAÇÃO': df_habilidades_previas['BASE_ABS'],
    'TOTAL': df_habilidades_previas['TOTAL_CP'],
}

df_notas = pd.DataFrame(data)

# Calcular as estatísticas descritivas

media_notas = df_habilidades_previas['TOTAL_CP'].mean()
desvio_notas = df_habilidades_previas['TOTAL_CP'].std()
percentil_25 = np.percentile(df_habilidades_previas['TOTAL_CP'], 25)
percentil_50 = np.percentile(df_habilidades_previas['TOTAL_CP'], 50)
percentil_75 = np.percentile(df_habilidades_previas['TOTAL_CP'], 75)

# Filtrar os alunos com notas maiores que 7
alunos_aprovados = df_habilidades_previas[df_habilidades_previas['TOTAL_CP'] >= 7]
alunos_repro = df_habilidades_previas[df_habilidades_previas['TOTAL_CP'] < 7]

# Contar quantas vezes cada nota aparece
contagem_Q1 = df_habilidades_previas['Q1'].value_counts().reset_index()
contagem_Q1.columns = ['Conhecimento Prévio', 'Número de Alunos']
contagem_Q2 = df_habilidades_previas['Q2'].value_counts().reset_index()
contagem_Q2.columns = ['Conhecimento Prévio', 'Número de Alunos']
contagem_Q3 = df_habilidades_previas['Q3'].value_counts().reset_index()
contagem_Q3.columns = ['Conhecimento Prévio', 'Número de Alunos']
contagem_Q4 = df_habilidades_previas['Q4'].value_counts().reset_index()
contagem_Q4.columns = ['Conhecimento Prévio', 'Número de Alunos']
contagem_Q5 = df_habilidades_previas['Q5'].value_counts().reset_index()
contagem_Q5.columns = ['Conhecimento Prévio', 'Número de Alunos']
contagem_Q6 = df_habilidades_previas['Q6'].value_counts().reset_index()
contagem_Q6.columns = ['Conhecimento Prévio', 'Número de Alunos']
contagem_Q7 = df_habilidades_previas['Q7'].value_counts().reset_index()
contagem_Q7.columns = ['Conhecimento Prévio', 'Número de Alunos']
contagem_Q8 = df_habilidades_previas['Q8'].value_counts().reset_index()
contagem_Q8.columns = ['Conhecimento Prévio', 'Número de Alunos']
contagem_Q9 = df_habilidades_previas['Q9'].value_counts().reset_index()
contagem_Q9.columns = ['Conhecimento Prévio', 'Número de Alunos']

# Criar o gráfico de pizza com Plotly Express
fig_q1 = px.pie(contagem_Q1, names='Conhecimento Prévio', values='Número de Alunos',
             title='Habilidades Questão 01')
fig_q2 = px.pie(contagem_Q2, names='Conhecimento Prévio', values='Número de Alunos',
             title='Habilidades Questão 02')
fig_q3 = px.pie(contagem_Q3, names='Conhecimento Prévio', values='Número de Alunos',
             title='Habilidades Questão 03')
fig_q4 = px.pie(contagem_Q4, names='Conhecimento Prévio', values='Número de Alunos',
             title='Habilidades Questão 04')
fig_q5 = px.pie(contagem_Q5, names='Conhecimento Prévio', values='Número de Alunos',
             title='Habilidades Questão 05')
fig_q6 = px.pie(contagem_Q6, names='Conhecimento Prévio', values='Número de Alunos',
             title='Habilidades Questão 06')
fig_q7 = px.pie(contagem_Q7, names='Conhecimento Prévio', values='Número de Alunos',
             title='Habilidades Questão 07')
fig_q8 = px.pie(contagem_Q8, names='Conhecimento Prévio', values='Número de Alunos',
             title='Habilidades Questão 08')
fig_q9 = px.pie(contagem_Q9, names='Conhecimento Prévio', values='Número de Alunos',
             title='Habilidades Questão 09')

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

layout = html.Div([
    html.H1("Análise dos Conhecimentos Prévios", style=style_h1),
    html.H2("Boletim Individual", style=style_h2),
    dcc.Dropdown(
        id='dropdown-aluno',
        options=[
            {'label': aluno, 'value': aluno}
            for aluno in df_notas['ALUNO']
        ],
        value=df_notas['ALUNO'].iloc[0],
    ),

    dcc.Graph(
        id='grafico-notas-cp',
    ),

    html.Hr(),
    html.H2("Estatísticas Descritivas das Notas", style=style_h2),
    html.P("Média das Notas: {:.2f}".format(media_notas)),
    html.P("Desvio Padrão das Notas: {:.2f}".format(desvio_notas)),
    html.P("25º Percentil das Notas: {:.2f}".format(percentil_25)),
    html.P("Mediana das Notas (50º Percentil): {:.2f}".format(percentil_50)),
    html.P("75º Percentil das Notas: {:.2f}".format(percentil_75)),

    html.Hr(),
    html.H2("Histograma das Notas", style=style_h2),
    dcc.Graph(
        id='histograma-notas',
        figure={
            'data': [
                go.Histogram(
                    x=df_habilidades_previas['TOTAL_CP'],
                    xbins=dict(
                        start=df_habilidades_previas['TOTAL_CP'].min(),
                        end=df_habilidades_previas['TOTAL_CP'].max(),
                        size=1
                    ),
                    marker=dict(color='blue'),
                    opacity=0.75,
                )
            ],
            'layout': go.Layout(
                xaxis={'title': 'Nota'},
                yaxis={'title': 'Quantidade de Alunos'},
                title='Distribuição das Notas',
            )
        }
    ),
    html.Hr(),
    html.H2("Relação entre Experiência em Programação e Notas", style=style_h2),
    dcc.Graph(
        id='boxplot-notas-experiencia',
        figure={
            'data': [
                go.Box(
                    x=df_habilidades_previas['Você possui alguma experiência na Área de Programação?'],
                    y=df_habilidades_previas['TOTAL_CP'],
                    boxpoints='outliers',
                    marker=dict(color='blue'),
                    opacity=0.75,
                )
            ],
            'layout': go.Layout(
                xaxis={'title': 'Experiência em Programação'},
                yaxis={'title': 'Nota'},
                title='Distribuição das Notas por Experiência em Programação',
            )
        }
    ),
    html.Hr(),
    html.H2("Alunos com Nota Maior que 7", style=style_h2),
    dash_table.DataTable(
        id='tabela-alunos',
        columns=[
            {'name': 'ID', 'id': 'ID'},
            {'name': 'Nome', 'id': 'Nome:'},
            {'name': 'Nota Total', 'id': 'TOTAL_CP'},
        ],
        data=alunos_aprovados.to_dict('records'),
    ),
html.Hr(),
    html.H2("Alunos com Nota Menor que 7", style=style_h2),
    dash_table.DataTable(
        id='tabela-alunos',
        columns=[
            {'name': 'ID', 'id': 'ID'},
            {'name': 'Nome', 'id': 'Nome:'},
            {'name': 'Nota Total', 'id': 'TOTAL_CP'},
        ],
        data=alunos_repro.to_dict('records'),
    ),



html.Div([
        html.Div([
            html.Div([dcc.Graph(id='Q1',figure=fig_q1)]),
            html.Div([dcc.Graph(id='Q2',figure=fig_q2)])], style={'display': 'flex'}),
        html.Div([
            html.Div([dcc.Graph(id='Q3',figure=fig_q3)]),
            html.Div([dcc.Graph(id='Q4',figure=fig_q4)])], style={'display': 'flex'}),
        html.Div([
            html.Div([dcc.Graph(id='Q5',figure=fig_q5)]),
            html.Div([dcc.Graph(id='Q6',figure=fig_q6)])], style={'display': 'flex'}),
        html.Div([
            html.Div([dcc.Graph(id='Q7',figure=fig_q7)]),
            html.Div([dcc.Graph(id='Q8',figure=fig_q9)])], style={'display': 'flex'}),
        html.Div([
            html.Div([dcc.Graph(id='Q9',figure=fig_q9)]),
            html.Div([])], style={'display': 'flex'}),

    ])

], style=style_div)
# Callback para atualizar o gráfico com base no aluno selecionado
@callback(
    Output('grafico-notas-cp', 'figure'),
    Input('dropdown-aluno', 'value')
)


def update_graph_boletim(selected_aluno):
    aluno_data = df_notas[df_notas['ALUNO'] == selected_aluno]

    # Defina um limite de nota baixa
    limite_nota_baixa = 6

    # Crie uma lista de cores com base nas notas
    cores = ['red' if nota < limite_nota_baixa else 'blue' for nota in aluno_data.iloc[0][1:]]

    figure = {
        'data': [
            {'x': aluno_data.columns[1:], 'y': aluno_data.iloc[0][1:],
             'type': 'bar', 'name': selected_aluno, 'marker': {'color': cores}},
        ],
        'layout': {
            'title': f'Notas do(a) Aluno(a): {selected_aluno}',
            'xaxis': {'title': 'Bases do Pensamento Computacional'},
            'yaxis': {'title': 'Nota'},
        }
    }
    return figure