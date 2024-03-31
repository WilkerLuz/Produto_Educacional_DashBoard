import numpy as np
import pandas as pd
from dash import html, dcc, callback, Output, Input
import plotly.graph_objs as go
import plotly.express as px
from sklearn.cluster import KMeans



df_atividade_01 = pd.read_csv('atividade_01.csv')
df_habilidades_previas = pd.read_csv('conhecimentos_previos_com_nota.csv')
df_engajamento = pd.read_csv('engajamento.csv')

df_habilidades_previas['BASE_ALG'] = df_habilidades_previas['BASE_ALG'].str.replace(',', '.').astype(float)
df_habilidades_previas['BASE_DEC'] = df_habilidades_previas['BASE_DEC'].str.replace(',', '.').astype(float)
df_habilidades_previas['BASE_REC'] = df_habilidades_previas['BASE_REC'].str.replace(',', '.').astype(float)
df_habilidades_previas['BASE_ADS'] = df_habilidades_previas['BASE_ABS'].str.replace(',', '.').astype(float)
df_habilidades_previas['TOTAL_CP'] = df_habilidades_previas['TOTAL_CP'].str.replace(',', '.').astype(float)

df_atividade_01['BASE_ALG_01'] = df_atividade_01['BASE_ALG_01'].str.replace(',','.').astype(float)
df_atividade_01['BASE_DEC_01'] = df_atividade_01['BASE_DEC_01'].str.replace(',','.').astype(float)
df_atividade_01['BASE_REC_01'] = df_atividade_01['BASE_REC_01'].str.replace(',','.').astype(float)
df_atividade_01['BASE_ABS_01'] = df_atividade_01['BASE_ABS_01'].str.replace(',','.').astype(float)
df_atividade_01['TOTAL_ATIVIDADE_01'] = df_atividade_01['TOTAL_ATIVIDADE_01'].str.replace(',','.').astype(float)

data = {
    'Aluno': df_atividade_01['NOME'],
    'ALGORITMO': df_atividade_01['BASE_ALG_01'],
    'DECOMPOSIÇÃO': df_atividade_01['BASE_DEC_01'],
    'RECONHECIMENTO DE PADRÕES': df_atividade_01['BASE_REC_01'],
    'ABSTRAÇÃO': df_atividade_01['BASE_ABS_01'],
    'Total': df_atividade_01['TOTAL_ATIVIDADE_01'],
}

df_notas = pd.DataFrame(data)

data_exp = {
   'Aluno': df_atividade_01['NOME'],
    'NotaCP': df_habilidades_previas['TOTAL_CP'],
    'Nota01': df_atividade_01['TOTAL_ATIVIDADE_01'],
    'Experiencia': df_atividade_01['EXPERIENCIA'],
}

df_exp = pd.DataFrame(data_exp)

data_eng = {
   'Aluno': df_atividade_01['NOME'],
    'NotaCP': df_habilidades_previas['TOTAL_CP'],
    'Nota01': df_atividade_01['TOTAL_ATIVIDADE_01'],
    'Engajamento': df_engajamento['ENGAJAMENTO_01'],
}

df_eng = pd.DataFrame(data_eng)

df_exp['Experiencia'].fillna(0, inplace=True)
df_eng['NotaCP'].fillna(0, inplace=True)
df_eng['Nota01'].fillna(0, inplace=True)
df_eng['Engajamento'].fillna(0, inplace=True)

# Selecione as características para a clusterização
caracteristicas = ['NotaCP', 'Nota01', 'Engajamento']

# Realize a clusterização com K-Means (por exemplo, com 3 clusters)
n_clusters = 3
kmeans = KMeans(n_clusters=n_clusters, n_init=10, random_state=0)
df_eng['Cluster'] = kmeans.fit_predict(df_eng[caracteristicas])


# Calcular as estatísticas descritivas PAINEL DE INDICADORES

# Configurar o layout do painel
layout_painel = go.Layout(
    grid={'rows': 4, 'columns': 2},
    title='Painel de Indicadores e Alertas',
    template='plotly_white',
    margin=dict(l=70, r=50, t=80, b=80)  # Margens do painel
)

media_notas = df_atividade_01['TOTAL_ATIVIDADE_01'].mean()
desvio_notas = df_atividade_01['TOTAL_ATIVIDADE_01'].std()
percentil_25 = np.percentile(df_atividade_01['TOTAL_ATIVIDADE_01'], 25)
percentil_50 = np.percentile(df_atividade_01['TOTAL_ATIVIDADE_01'], 50)
percentil_75 = np.percentile(df_atividade_01['TOTAL_ATIVIDADE_01'], 75)
media_engajamento = df_eng['Engajamento'].mean()
alerta_notas = (df_eng['Nota01'] <= 5).sum()
alerta_engajamento = (df_eng['Engajamento'] < 50).sum()

# Criar figuras para os indicadores

fig_notas = go.Figure(go.Indicator(
    mode='number',
    value=media_notas,
    title={'text': 'Média de Notas'},
    domain={'x': [0, 0.45], 'y': [0, 0.3]}
))

#ok
fig_engajamento = go.Figure(go.Indicator(
    mode='number',
    value=media_engajamento,
    title={'text': 'Média de Engajamento'},
    number={'suffix': '%'},
    domain={'x': [0.55, 1], 'y': [0.35, 0.65]}
))
#ok
fig_alerta_notas = go.Figure(go.Indicator(
    mode='number',
    value=alerta_notas,
    title={'text': 'Alerta: Notas Baixas'},
    number={'suffix': ' alunos'},
    domain={'x': [0, 0.45], 'y': [0.7, 1]}
))
#ok
fig_alerta_engajamento = go.Figure(go.Indicator(
    mode='number',
    value=alerta_engajamento,
    title={'text': 'Alerta: Engajamento Baixo'},
    domain={'x': [0.55, 1], 'y': [0.7, 1]}
))

fig_painel = go.Figure(
    data=[
        fig_notas.data[0],
        fig_engajamento.data[0],
        fig_alerta_notas.data[0],
        fig_alerta_engajamento.data[0]
    ],
    layout=layout_painel
)
#Bases do Pensamento Computacional
contagem_alg = df_atividade_01['ALG_01'].value_counts().reset_index()
contagem_alg.columns = ['Conhecimento Prévio', 'Número de Alunos']

fig_alg = px.pie(contagem_alg, names='Conhecimento Prévio', values='Número de Alunos',
             title='Base Algoritmo')

contagem_dec = df_atividade_01['DEC_01'].value_counts().reset_index()
contagem_dec.columns = ['Conhecimento Prévio', 'Número de Alunos']

fig_dec = px.pie(contagem_dec, names='Conhecimento Prévio', values='Número de Alunos',
             title='Base Decomposição')

contagem_rec = df_atividade_01['REC_01'].value_counts().reset_index()
contagem_rec.columns = ['Conhecimento Prévio', 'Número de Alunos']

fig_rec = px.pie(contagem_rec, names='Conhecimento Prévio', values='Número de Alunos',
             title='Base Reconhecimento de Padrões')

contagem_abs = df_atividade_01['ABS_01'].value_counts().reset_index()
contagem_abs.columns = ['Conhecimento Prévio', 'Número de Alunos']

fig_abs = px.pie(contagem_alg, names='Conhecimento Prévio', values='Número de Alunos',
             title='Base Abstração')


# Crie o gráfico de bolhas

fig_exp_dispersao =px.scatter(
            df_exp,
            x='NotaCP',
            y='Nota01',
            size='Experiencia',
            color='Experiencia',
            hover_name='Aluno',
            title='Gráfico de dispersão da relação entre Notas CP, Notas 1 e Experiência em Programação do Grupo de Alunos',
)

fig_dis = px.scatter(df_eng, x="NotaCP", y="Nota01", color="Engajamento")

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
    html.H1("Análise da Atividade 1 - Um Robô Aspirador", style=style_h1),
    html.H2("Boletim Individual", style=style_h2),
    dcc.Dropdown(
        id='dropdown-aluno-boletin',
        options=[
            {'label': aluno, 'value': aluno}
            for aluno in df_notas['Aluno']
        ],
        value=df_notas['Aluno'].iloc[0],
    ),

    dcc.Graph(
        id='grafico-notas-atividade-01',
    ),

    html.Hr(),
    html.H2("Estatísticas Descritivas das Notas", style=style_h2),
    dcc.Graph(
        id='abs',
        figure=fig_painel
    ),

    html.Hr(),
    html.H2("Histograma das Notas", style=style_h2),
    dcc.Graph(
        id='histograma-notas',
        figure={
            'data': [
                go.Histogram(
                    x=df_atividade_01['TOTAL_ATIVIDADE_01'],
                    xbins=dict(
                        start=df_atividade_01['TOTAL_ATIVIDADE_01'].min(),
                        end=df_atividade_01['TOTAL_ATIVIDADE_01'].max(),
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
                    x=df_atividade_01['EXPERIENCIA'],
                    y=df_atividade_01['TOTAL_ATIVIDADE_01'],
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
    html.H2("Relação entre as notas do Conhecimento Prévio, Atividade 01 e Experiência em Programação", style=style_h2),

    dcc.Graph(
        id='scatter-plot',
        figure=fig_exp_dispersao
    ),

    dcc.Graph(
        id='eng_dis',
        figure=fig_dis
    ),
    html.Hr(),
    html.H2("Clusterização por notas e engajamento", style=style_h2),
    dcc.Graph(
        id='grafico_cluster',
        config={'scrollZoom': False},
    ),

    dcc.Dropdown(
        id='cluster-dropdown',
        options=[
            {'label': f'Cluster {i}', 'value': i}
            for i in range(n_clusters)
        ],
        value=0,  # Valor inicial
    ),

    html.Div([
        html.H3(id='cluster-title'),
        html.Table(id='cluster-list',
                   style={'width': '50%'})
    ]),
    html.Hr(),
    html.H2("Gráficos sobre as base do PC", style=style_h2),

    html.Div([
        html.Div([
            html.Div([dcc.Graph(id='alg',figure=fig_alg)]),
            html.Div([dcc.Graph(id='dec',figure=fig_dec)])], style={'display': 'flex'}),
        html.Div([
            html.Div([dcc.Graph(id='rec',figure=fig_rec)]),
            html.Div([dcc.Graph(id='abs',figure=fig_abs)])], style={'display': 'flex'}),
    ]),


], style=style_div)

# Callback para atualizar o gráfico com base no aluno selecionado
@callback(
    Output('grafico-notas-atividade-01', 'figure'),
    Input('dropdown-aluno-boletin', 'value')
)

def update_graph_boletim(selected_aluno):
    aluno_data = df_notas[df_notas['Aluno'] == selected_aluno]

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

# Callback para atualizar o gráfico de dispersão
@callback(
    Output('grafico_cluster', 'figure'),
    Input('cluster-dropdown', 'value')
)

def update_scatter_plot(selected_cluster):
    fig = px.scatter(
        df_eng[df_eng['Cluster'] == selected_cluster],
        x='NotaCP',
        y='Nota01',
        color='Engajamento',
        size='Engajamento',
        hover_name='Aluno',
        title=f'Cluster {selected_cluster}',
    )
    return fig


# Callback para atualizar a lista de alunos com base no cluster selecionado
@callback(
    [Output('cluster-title', 'children'),
     Output('cluster-list', 'children')],
    Input('cluster-dropdown', 'value')
)
def update_cluster_list(selected_cluster):
    students_in_cluster = df_eng[df_eng['Cluster'] == selected_cluster]['Aluno']

    # Título do cluster
    cluster_title = f'Alunos no Cluster {selected_cluster}'

    # Lista de alunos em formato de tabela
    students_list = [html.Tr([html.Td(student)]) for student in students_in_cluster]

    return cluster_title, students_list

def update_cluster_list(selected_cluster):
    students_in_cluster = df_eng[df_eng['Cluster'] == selected_cluster]['Aluno']
    students_list = [html.P(student) for student in students_in_cluster]
    return students_list

