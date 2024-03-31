import numpy as np
import pandas as pd
from dash import html, dcc, callback, Output, Input, dash
import plotly.graph_objs as go
import plotly.express as px
from sklearn.cluster import KMeans

df_boletim = pd.read_csv('analise_todas_atividades_vpl.csv')
df_av = pd.read_csv('vpl_avaliacao_limpo.csv')

df_boletim['NotaCP'] = df_boletim['NotaCP'].str.replace(',','.').astype(float)
df_boletim['Nota1'] = df_boletim['Nota1'].str.replace(',','.').astype(float)
df_boletim['Nota2'] = df_boletim['Nota2'].str.replace(',','.').astype(float)
df_boletim['Nota3'] = df_boletim['Nota3'].str.replace(',','.').astype(float)
df_boletim['Nota4'] = df_boletim['Nota4'].str.replace(',','.').astype(float)
#df_boletim['Nota5'] = df_boletim['Nota5'].str.replace(',','.').astype(float)
#df_boletim['Nota6'] = df_boletim['Nota6'].str.replace(',','.').astype(float)



data = {
    'Aluno': df_boletim['NOME_ALUNO'],
    'NotaCP': df_boletim['NotaCP'],
    'Nota1': df_boletim['Nota1'],
    'Nota2':  df_boletim['Nota2'],
    'Nota3':  df_boletim['Nota3'],
    'Nota4': df_boletim['Nota4'],
    'Nota5': df_boletim['Nota5'],
    'Nota6': df_boletim['Nota6'],
    'Avaliacao': df_av['NOTA'],
    'Engajamento': df_boletim['engajamento_n6_media'],
}

df_notas = pd.DataFrame(data)

df_notas['NotaCP'].fillna(0, inplace=True)
df_notas['Nota1'].fillna(0, inplace=True)
df_notas['Nota2'].fillna(0, inplace=True)
df_notas['Nota3'].fillna(0, inplace=True)
df_notas['Nota4'].fillna(0, inplace=True)
df_notas['Nota5'].fillna(0, inplace=True)
df_notas['Nota6'].fillna(0, inplace=True)
df_notas['Avaliacao'].fillna(0, inplace=True)
df_notas['Engajamento'].fillna(0, inplace=True)


# Realize a clusterização com K-Means (por exemplo, com 3 clusters)
n_clusters = 3
kmeans = KMeans(n_clusters=n_clusters, n_init=10, random_state=0)
df_notas['Cluster'] = kmeans.fit_predict(df_notas[['NotaCP','Nota1','Nota2','Nota3',
                                                   'Nota4','Nota5','Nota6','Avaliacao']])

# Crie um aplicativo Dash
app = dash.Dash(__name__)

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

# Layout do aplicativo
layout = html.Div([
    html.H1("Gráfico de Velocímetro", style=style_h1),

    dcc.Dropdown(
        id='aluno-dropdown-velo',
        options=[
            {'label': aluno, 'value': aluno}
            for aluno in df_boletim['NOME_ALUNO']
        ],
        value=df_boletim['NOME_ALUNO'].iloc[0],
    ),

    html.Div([
        html.Div([
            html.Div([dcc.Graph(id='velocimetro-engajamento')]),
            html.Div([dcc.Graph(id='velocimetro-notacp')])], style={'display': 'flex'}),
        html.Div(
            [
            html.Div([dcc.Graph(id='velocimetro-nota1')]),
            html.Div([dcc.Graph(id='velocimetro-nota2')])], style={'display': 'flex'}),
        html.Div(
            [
            html.Div([dcc.Graph(id='velocimetro-nota3')]),
            html.Div([dcc.Graph(id='velocimetro-nota4')])], style={'display': 'flex'}),
        html.Div(
            [
            html.Div([dcc.Graph(id='velocimetro-nota5')]),
            html.Div([dcc.Graph(id='velocimetro-nota6')])], style={'display': 'flex'}),
        html.Div(
            [
            html.Div([dcc.Graph(id='velocimetro-avaliacao')]),
            html.Div([])], style={'display': 'flex'}),
    ]),


    #Teste Clusterização por Notas
    html.Hr(),
    html.H2("Clusterização por notas e engajamento"),

    dcc.Graph(
        id='grafico_cluster_notas',
        config={'scrollZoom': False},
    ),

    dcc.Dropdown(
        id='cluster-dropdown_notas',
        options=[
            {'label': f'Cluster {i}', 'value': i}
            for i in range(n_clusters)
        ],
        value=0,  # Valor inicial
    ),

    html.Div([
        html.H3(id='cluster-title_notas'),
        html.Table(id='cluster-list_notas',
                   style={'width': '50%'})
    ]),
], style=style_div)

# Função para criar um gráfico de velocímetro
def create_velocimetro(value, title):
    cor = 'green'  # Cor padrão (verde)
    if value < 5:
        cor = 'red'  # Nota abaixo de 5, cor vermelha
    elif value < 7:
        cor = 'yellow'  # Nota entre 5 e 7, cor amarela

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title},
        gauge={'axis': {'range': [0, 10]}, 'bar': {'color': cor},
               'threshold': {'line': {'color': cor, 'width': 4}, 'thickness': 0.75, 'value': 7}},
        domain={'x': [0, 1], 'y': [0, 1]}
    ))
    return fig

def create_velocimetro_eng(value, title):
    cor = 'green'  # Cor padrão (verde)
    if value < 50:
        cor = 'red'  # Nota abaixo de 5, cor vermelha
    elif value < 70:
        cor = 'yellow'  # Nota entre 5 e 7, cor amarela

    fig_eng = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title},
        number={'suffix': '%'},
        gauge={'axis': {'range': [0, 100]}, 'bar': {'color': cor},
               'threshold': {'line': {'color': cor, 'width': 4}, 'thickness': 0.75, 'value': 70}},
        domain={'x': [0, 1], 'y': [0, 1]}
    ))
    return fig_eng


# Callback para atualizar o gráfico de velocímetro com base no aluno selecionado
@callback([Output('velocimetro-engajamento', 'figure'),
    Output('velocimetro-notacp', 'figure'),
     Output('velocimetro-nota1', 'figure'),
     Output('velocimetro-nota2', 'figure'),
     Output('velocimetro-nota3', 'figure'),
    Output('velocimetro-nota4', 'figure'),
    Output('velocimetro-nota5', 'figure'),
    Output('velocimetro-nota6', 'figure'),
    Output('velocimetro-avaliacao', 'figure')],
    Input('aluno-dropdown-velo', 'value')
)
def update_velocimetros(selected_aluno):
    # Obtém as notas do aluno selecionado
    aluno_data = df_notas[df_notas['Aluno'] == selected_aluno]
    engajamento = aluno_data['Engajamento'].values[0]
    nota_cp = aluno_data['NotaCP'].values[0]
    nota1 = aluno_data['Nota1'].values[0]
    nota2 = aluno_data['Nota2'].values[0]
    nota3 = aluno_data['Nota3'].values[0]
    nota4 = aluno_data['Nota4'].values[0]
    nota5 = aluno_data['Nota5'].values[0]
    nota6 = aluno_data['Nota6'].values[0]
    avaliacao = aluno_data['Avaliacao'].values[0]

    # Cria os gráficos de velocímetro para cada nota
    fig_eng = create_velocimetro_eng(engajamento, 'Engajamento')
    fig_notacp = create_velocimetro(nota_cp, 'NotaCP')
    fig_nota1 = create_velocimetro(nota1, 'Nota1')
    fig_nota2 = create_velocimetro(nota2, 'Nota2')
    fig_nota3 = create_velocimetro(nota3, 'Nota3')
    fig_nota4 = create_velocimetro(nota4, 'Nota4')
    fig_nota5 = create_velocimetro(nota5, 'Nota5')
    fig_nota6 = create_velocimetro(nota6, 'Nota6')
    fig_avaliacao = create_velocimetro(avaliacao, 'Avaliacao')


    return fig_eng, fig_notacp, fig_nota1, fig_nota2, fig_nota3, fig_nota4, fig_nota5, fig_nota6, fig_avaliacao

# Callback para atualizar o gráfico de dispersão
@callback(
    Output('grafico_cluster_notas', 'figure'),
    Input('cluster-dropdown_notas', 'value')
)

def update_scatter_plot(selected_cluster):
    fig = px.scatter(
        df_notas[df_notas['Cluster'] == selected_cluster],
        x='Nota6',
        y='Avaliacao',
        color='Avaliacao',
        size='Avaliacao',
        hover_name='Aluno',
        title=f'Cluster {selected_cluster}',
    )
    return fig


# Callback para atualizar a lista de alunos com base no cluster selecionado
@callback(
    [Output('cluster-title_notas', 'children'),
     Output('cluster-list_notas', 'children')],
    Input('cluster-dropdown_notas', 'value')
)
def update_cluster_list(selected_cluster):
    students_in_cluster = df_notas[df_notas['Cluster'] == selected_cluster]['Aluno']

    # Título do cluster
    cluster_title = f'Alunos no Cluster {selected_cluster}'

    # Lista de alunos em formato de tabela
    students_list = [html.Tr([html.Td(student)]) for student in students_in_cluster]

    return cluster_title, students_list


