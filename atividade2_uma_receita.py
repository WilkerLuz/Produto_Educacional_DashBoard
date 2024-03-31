
import numpy as np
import pandas as pd
from dash import html, dcc, callback, Output, Input
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
from sklearn.cluster import KMeans

df_atividade_02 = pd.read_csv('atividade_02.csv')
df_atividade_01 = pd.read_csv('atividade_01.csv')
df_habilidades_previas = pd.read_csv('conhecimentos_previos_com_nota.csv')
df_engajamento = pd.read_csv('engajamento.CSV')

df_atividade_02['BASE_ALG_02'] = df_atividade_02['BASE_ALG_02'].str.replace(',','.').astype(float)
df_atividade_02['BASE_DEC_02'] = df_atividade_02['BASE_DEC_02'].str.replace(',','.').astype(float)
df_atividade_02['BASE_REC_02'] = df_atividade_02['BASE_REC_02'].str.replace(',','.').astype(float)
df_atividade_02['BASE_ABS_02'] = df_atividade_02['BASE_ABS_02'].str.replace(',','.').astype(float)
df_atividade_02['TOTAL_ATIVIDADE_02'] = df_atividade_02['TOTAL_ATIVIDADE_02'].str.replace(',','.').astype(float)

df_atividade_01['TOTAL_ATIVIDADE_01'] = df_atividade_01['TOTAL_ATIVIDADE_01'].str.replace(',','.').astype(float)
df_habilidades_previas['TOTAL_CP'] = df_habilidades_previas['TOTAL_CP'].str.replace(',', '.').astype(float)

data_n2 = {
    'Aluno': df_atividade_02['NOME'],
    'ALGORITMO': df_atividade_02['BASE_ALG_02'],
    'DECOMPOSIÇÃO': df_atividade_02['BASE_DEC_02'],
    'RECONHECIMENTO DE PADRÕES': df_atividade_02['BASE_REC_02'],
    'ABSTRAÇÃO': df_atividade_02['BASE_ABS_02'],
    'Total': df_atividade_02['TOTAL_ATIVIDADE_02'],
}

df_notas_n2 = pd.DataFrame(data_n2)

data_exp_n2 = {
   'Aluno': df_atividade_02['NOME'],
    'NotaCP': df_habilidades_previas['TOTAL_CP'],
    'Nota02': df_atividade_02['TOTAL_ATIVIDADE_02'],
    'Experiencia': df_atividade_02['EXPERIENCIA'],
}

data_eng_n2 = {
   'Aluno': df_atividade_02['NOME'],
    'NotaCP': df_habilidades_previas['TOTAL_CP'],
    'Nota01': df_atividade_01['TOTAL_ATIVIDADE_01'],
    'Nota02': df_atividade_02['TOTAL_ATIVIDADE_02'],
    'Experiencia': df_atividade_02['EXPERIENCIA'],
    'Engajamento': df_engajamento['ENGAJAMENTO_02'],
}


df_exp = pd.DataFrame(data_exp_n2)
df_exp['Experiencia'].fillna(0, inplace=True)

#Caso exista valores Null no DataFrame
df_eng_n2 = pd.DataFrame(data_eng_n2)
df_eng_n2['NotaCP'].fillna(0, inplace=True)
df_eng_n2['Nota01'].fillna(0, inplace=True)
df_eng_n2['Nota02'].fillna(0, inplace=True)
df_eng_n2['Experiencia'].fillna(0, inplace=True)
df_eng_n2['Engajamento'].fillna(0, inplace=True)

# Realize a clusterização com K-Means (por exemplo, com 3 clusters)
n_clusters = 3
kmeans = KMeans(n_clusters=n_clusters, n_init=10, random_state=0)
df_eng_n2['Cluster'] = kmeans.fit_predict(df_eng_n2[['NotaCP','Nota01','Nota02','Experiencia','Engajamento']])


# Calcular as estatísticas descritivas PAINEL DE INDICADORES

# Configurar o layout do painel
layout_painel = go.Layout(
    grid={'rows': 4, 'columns': 2},
    title='Painel de Indicadores e Alertas',
    template='plotly_white',
    margin=dict(l=70, r=50, t=80, b=80)  # Margens do painel
)

media_notas = df_atividade_02['TOTAL_ATIVIDADE_02'].mean()
desvio_notas = df_atividade_02['TOTAL_ATIVIDADE_02'].std()
percentil_25 = np.percentile(df_atividade_02['TOTAL_ATIVIDADE_02'], 25)
percentil_50 = np.percentile(df_atividade_02['TOTAL_ATIVIDADE_02'], 50)
percentil_75 = np.percentile(df_atividade_02['TOTAL_ATIVIDADE_02'], 75)
media_engajamento = df_eng_n2['Engajamento'].mean()
alerta_notas = (df_eng_n2['Nota02'] <= 5).sum()
alerta_engajamento = (df_eng_n2['Engajamento'] < 50).sum()

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
contagem_alg = df_atividade_02['ALG_02'].value_counts().reset_index()
contagem_alg.columns = ['Conhecimento Prévio', 'Número de Alunos']

fig_alg = px.pie(contagem_alg, names='Conhecimento Prévio', values='Número de Alunos',
             title='Base Algoritmo')

contagem_dec = df_atividade_02['DEC_02'].value_counts().reset_index()
contagem_dec.columns = ['Conhecimento Prévio', 'Número de Alunos']

fig_dec = px.pie(contagem_dec, names='Conhecimento Prévio', values='Número de Alunos',
             title='Base Decomposição')

contagem_rec = df_atividade_02['REC_02'].value_counts().reset_index()
contagem_rec.columns = ['Conhecimento Prévio', 'Número de Alunos']

fig_rec = px.pie(contagem_rec, names='Conhecimento Prévio', values='Número de Alunos',
             title='Base Reconhecimento de Padrões')

contagem_abs = df_atividade_02['ABS_02'].value_counts().reset_index()
contagem_abs.columns = ['Conhecimento Prévio', 'Número de Alunos']

fig_abs = px.pie(contagem_alg, names='Conhecimento Prévio', values='Número de Alunos',
             title='Base Abstração')


# Crie o gráfico de bolhas

fig_exp_dispersao =px.scatter(
            df_exp,
            x='NotaCP',
            y='Nota02',
            size='Experiencia',
            color='Experiencia',
            hover_name='Aluno',
            title='Gráfico de dispersão da relação entre Notas CP, Notas 1 e Experiência em Programação do Grupo de Alunos',
)

fig_dis = px.scatter(df_eng_n2, x="NotaCP", y="Nota02", color="Engajamento")

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
    html.H1("Análise da Atividade 2 - Uma Receita de Programação", style=style_h1),
    html.H2("Boletim Individual"),
    dcc.Dropdown(
        id='dropdown-aluno-boletin_n2',
        options=[
            {'label': aluno, 'value': aluno}
            for aluno in df_notas_n2['Aluno']
        ],
        value=df_notas_n2['Aluno'].iloc[0],
    ),

    dcc.Graph(
        id='grafico-notas-atividade-02',
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
                    x=df_notas_n2['Total'],
                    xbins=dict(
                        start=df_notas_n2['Total'].min(),
                        end=df_notas_n2['Total'].max(),
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
                    x=df_atividade_02['EXPERIENCIA'],
                    y=df_atividade_02['TOTAL_ATIVIDADE_02'],
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
    html.H2("Clusterização por notas e engajamento"),

    dcc.Graph(
        id='grafico_cluster_n2',
        config={'scrollZoom': False},
    ),

    dcc.Dropdown(
        id='cluster-dropdown_n2',
        options=[
            {'label': f'Cluster {i}', 'value': i}
            for i in range(n_clusters)
        ],
        value=0,  # Valor inicial
    ),

    html.Div([
        html.H3(id='cluster-title_n2'),
        html.Table(id='cluster-list_n2',
                   style={'width': '50%'})
    ]),
    html.Hr(),
    html.H2("Gráficos sobre as base do PC", style=style_h2),
    html.Div([
        html.Div([
            html.Div([dcc.Graph(id='alg', figure=fig_alg)]),
            html.Div([dcc.Graph(id='dec', figure=fig_dec)])], style={'display': 'flex'}),
        html.Div([
            html.Div([dcc.Graph(id='rec', figure=fig_rec)]),
            html.Div([dcc.Graph(id='abs', figure=fig_abs)])], style={'display': 'flex'}),
    ]),



], style=style_div)

# Callback para atualizar o gráfico com base no aluno selecionado
@callback(
    Output('grafico-notas-atividade-02', 'figure'),
    Input('dropdown-aluno-boletin_n2', 'value')
)

def update_graph_boletim(selected_aluno):
    aluno_data = df_notas_n2[df_notas_n2['Aluno'] == selected_aluno]

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
    Output('grafico_cluster_n2', 'figure'),
    Input('cluster-dropdown_n2', 'value')
)


def update_grouped_bar_chart(selected_cluster):
    df_filtered = df_eng_n2[df_eng_n2['Cluster'] == selected_cluster]

    # Crie um gráfico de barras agrupadas
    fig = go.Figure()

    # Adicione as barras para a nota 1
    fig.add_trace(go.Bar(
        x=df_filtered['Aluno'],
        y=df_filtered['Nota01'],
        name='Nota 1',
        hoverinfo='y+name',
        marker=dict(color='blue'),
    ))

    # Adicione as barras para a nota 2
    fig.add_trace(go.Bar(
        x=df_filtered['Aluno'],
        y=df_filtered['Nota02'],
        name='Nota 2',
        hoverinfo='y+name',
        marker=dict(color='green'),
    ))

    fig.update_layout(
        barmode='group',  # Barras agrupadas
        title=f'Cluster {selected_cluster}',
        xaxis=dict(title='Aluno'),
        yaxis=dict(title='Nota'),
        showlegend=True,
    )

    return fig

# Callback para atualizar a lista de alunos com base no cluster selecionado
@callback(
    [Output('cluster-title_n2', 'children'),
     Output('cluster-list_n2', 'children')],
    Input('cluster-dropdown_n2', 'value')
)
def update_cluster_list(selected_cluster):
    cluster_data = df_eng_n2[df_eng_n2['Cluster'] == selected_cluster]  # ['NOME_ALUNO']

    # Título do cluster
    cluster_title = f'Alunos no Cluster {selected_cluster}'

    # Lista de alunos em formato de tabela

    students_list = [
        html.Tr([
            html.Td(student),
            html.Td(cluster_data[cluster_data['Aluno'] == student]['Nota02'].values[0]),
            html.Td(cluster_data[cluster_data['Aluno'] == student]['Engajamento'].values[0])
        ])
        for student in cluster_data['Aluno']
    ]

    return cluster_title, students_list


