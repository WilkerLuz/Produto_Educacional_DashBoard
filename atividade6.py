import numpy as np
import pandas as pd
from dash import html, dcc, callback, Output, Input, dash
import plotly.graph_objs as go
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

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



# DataFrame Usados
df_atividade_6 = pd.read_csv('vpl_atividade_06_com_engajamento.csv')
df_analise_06 = pd.read_csv('analise_todas_atividades_vpl.csv')
df_vpl_06 = pd.read_csv('vpl_03_limpo.csv')

df_analise_06['NotaCP'] = df_analise_06['NotaCP'].str.replace(',','.').astype(float)
df_analise_06['Nota1'] = df_analise_06['Nota1'].str.replace(',','.').astype(float)
df_analise_06['Nota2'] = df_analise_06['Nota2'].str.replace(',','.').astype(float)
df_analise_06['Nota3'] = df_analise_06['Nota3'].str.replace(',','.').astype(float)
df_analise_06['Nota4'] = df_analise_06['Nota4'].str.replace(',','.').astype(float)
# Calcular as estatísticas descritivas PAINEL DE INDICADORES

# Configurar o layout do painel
layout_painel = go.Layout(
    grid={'rows': 4, 'columns': 2},
    title='Painel de Indicadores e Alertas',
    template='plotly_white',
    margin=dict(l=70, r=50, t=80, b=80)  # Margens do painel
)


media_notas = df_atividade_6['Media_Notas'].mean()
desvio_notas = df_atividade_6['Media_Notas'].std()
percentil_25 = np.percentile(df_atividade_6['Media_Notas'], 25)
percentil_50 = np.percentile(df_atividade_6['Media_Notas'], 50)
percentil_75 = np.percentile(df_atividade_6['Media_Notas'], 75)
Media_Engajamento = df_analise_06['engajamento_n6'].mean()
alerta_notas = (df_atividade_6['Media_Notas'] < 7).sum()
alerta_engajamento = (df_analise_06['engajamento_n6'] < 70).sum()

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
    value=Media_Engajamento,
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


heatmap_data_n6 = pd.pivot_table(df_vpl_06, index='NOME', columns='NAME', values='CONTAGEM', aggfunc='mean')

# Crie o heatmap interativo
trace = go.Heatmap(z=heatmap_data_n6.values,
                   x=heatmap_data_n6.columns,
                   y=heatmap_data_n6.index,
                   colorscale='YlGnBu',
                   colorbar={"title": "Contagem"},
                   )

layout = go.Layout(
    title='Heatmap de ENVIOS por Aluno e Questão',
    xaxis=dict(title='Questão', tickangle=-45),  # Rotaciona os rótulos do eixo x
    yaxis=dict(title='Aluno'),
    width=900,  # Ajusta a largura do gráfico
    height=800,  # Ajusta a altura do gráfico
    margin=dict(l=140),  # Ajusta a margem esquerda para acomodar o título
)

fig_heapmap = go.Figure(data=[trace], layout=layout)


# Realize a clusterização com K-Means (por exemplo, com 3 clusters)

#Caso tenha valores NaN no df
df_analise_06['NotaCP'].fillna(0, inplace=True)
df_analise_06['Nota1'].fillna(0, inplace=True)
df_analise_06['Nota2'].fillna(0, inplace=True)
df_analise_06['Nota3'].fillna(0, inplace=True)
df_analise_06['Nota4'].fillna(0, inplace=True)
df_analise_06['Nota5'].fillna(0, inplace=True)
df_analise_06['Nota6'].fillna(0, inplace=True)
df_analise_06['Experiencia'].fillna(0, inplace=True)
df_analise_06['engajamento_n6_media'].fillna(0, inplace=True)

# Normalizar os dados
scaler = StandardScaler()
df_normalized = scaler.fit_transform(df_analise_06[['NotaCP', 'Nota1', 'Nota2', 'Nota3', 'Nota4', 'Nota5', 'Nota6', 'Experiencia', 'engajamento_n6_media']])

# Executar K-means nos dados normalizados

n_clusters = 3
kmeans = KMeans(n_clusters=n_clusters, n_init=10, random_state=0)
df_analise_06['Cluster'] = kmeans.fit_predict(df_normalized)

# Layout do aplicativo
layout = html.Div([

    html.H1("Atividade VPL - Estruturas de Repetição da Linguagem de Programação C", style=style_h1),

    dcc.Dropdown(
        id='aluno-dropdown_n6',
        options=[
            {'label': aluno, 'value': aluno}
            for aluno in df_atividade_6['NOME_ALUNO']
        ],
        value=df_atividade_6['NOME_ALUNO'][0]
    ),

    dcc.Graph(id='grafico_n6'),

    html.Hr(),
    html.H2("Estatísticas Descritivas das Notas", style=style_h2),
        dcc.Graph(
        id='abs',
        figure=fig_painel
    ),

    # Dropdown para selecionar um aluno
    html.H2("Atividade em Atraso!"),
    dcc.Dropdown(
        id='aluno-dropdown_atraso_n6',
        options=[{'label': str(aluno), 'value': aluno} for aluno in df_vpl_06['NOME'].unique()],
        value=df_vpl_06['NOME'].iloc[0]  # Defina o valor inicial do dropdown
    ),

    # Gráfico para mostrar as questões com atraso
    dcc.Graph(id='grafico-atraso_n6'),

    html.H2("Heatmap de ENVIOS por Aluno e Questão"),
    dcc.Graph(figure=fig_heapmap),

#Teste Clusterização ENGAJAMENTO

    html.Hr(),
    html.H2("Clusterização por notas e engajamento"),

    dcc.Graph(
        id='grafico_cluster_n6',
        config={'scrollZoom': False},

    ),

    dcc.Dropdown(
        id='cluster-dropdown_n6',
        options=[
            {'label': f'Cluster {i}', 'value': i}
            for i in range(n_clusters)
        ],
        value=0,  # Valor inicial
    ),

    html.Div([
        html.H3(id='cluster-title_n6'),
        html.Table(id='cluster-list_n6',
                   style={'width': '50%'})
    ]),


], style=style_div)

@callback(
    Output('grafico_n6', 'figure'),
    Input('aluno-dropdown_n6', 'value')
)
def update_graph_boletim(selected_aluno):
    aluno_data = df_atividade_6[df_atividade_6['NOME_ALUNO'] == selected_aluno]

    # Defina um limite de nota baixa
    limite_nota_baixa = 6

    # Selecione as colunas desejadas (excluindo as duas primeiras e as três últimas)
    colunas_selecionadas = aluno_data.columns[1:-5]

    # Crie uma lista de cores com base nas notas
    cores = ['red' if nota < limite_nota_baixa else 'blue' for nota in aluno_data.iloc[0][2:-3]]

    figure = {
        'data': [
            {'x': colunas_selecionadas, 'y': aluno_data.iloc[0][2:-3],
             'type': 'bar', 'name': selected_aluno, 'marker': {'color': cores}},
        ],
        'layout': {
            'title': f'Notas do(a) Aluno(a): {selected_aluno}',
            'xaxis': {'title': 'Atividade VPL - Conceitos Iniciais'},
            'yaxis': {'title': 'Nota'},
        }
    }
    return figure

def gera_grafico_atraso(selected_aluno):
    aluno_df = df_vpl_06[df_vpl_06['NOME'] == selected_aluno]
    fig = px.bar(aluno_df, x='NAME', color='ATRASO', title=f'Questões com Atraso para Aluno {selected_aluno}')
    return fig

@callback(
    Output('grafico-atraso_n6', 'figure'),
    [Input('aluno-dropdown_atraso_n6', 'value')]
)
def update_grafico(selected_aluno):
    return gera_grafico_atraso(selected_aluno)


# Callback para atualizar o gráfico de dispersão dos clusters
@callback(
    Output('grafico_cluster_n6', 'figure'),
    Input('cluster-dropdown_n6', 'value')
)

def update_line_chart(selected_cluster):
    df_filtered = df_analise_06[df_analise_06['Cluster'] == selected_cluster]

    fig = go.Figure()

    for index, row in df_filtered.iterrows():
        aluno = row['NOME_ALUNO']
        notas = row[['Nota1', 'Nota2', 'Nota3', 'Nota4', 'Nota5', 'Nota6']]

        fig.add_trace(go.Scatter(x=['Nota1', 'Nota2', 'Nota3', 'Nota4', 'Nota5', 'Nota6'],
                                  y=notas,
                                  mode='lines+markers',
                                  name=aluno,
                                  hovertemplate='Aluno: ' + aluno +
                                                '<br>Nota1: ' + str(row['Nota1']) +
                                                '<br>Nota2: ' + str(row['Nota2']) +
                                                '<br>Nota3: ' + str(row['Nota3']) +
                                                '<br>Nota4: ' + str(row['Nota4']) +
                                                '<br>Nota5: ' + str(row['Nota5']) +
                                                '<br>Nota6: ' + str(row['Nota6'])
                                  ))

    fig.update_layout(title=f'Cluster {selected_cluster}',
                      xaxis_title='Atividades',
                      yaxis_title='Pontuação',
                      legend_title='Alunos')

    return fig



# Callback para atualizar a lista de alunos com base no cluster selecionado
@callback(
    [Output('cluster-title_n6', 'children'),
     Output('cluster-list_n6', 'children')],
    Input('cluster-dropdown_n6', 'value')
)
def update_cluster_list(selected_cluster):
    cluster_data = df_analise_06[df_analise_06['Cluster'] == selected_cluster]

    # Título do cluster
    cluster_title = f'Alunos no Cluster {selected_cluster}'

    # Lista de alunos em formato de tabela
    students_list = html.Table([
        html.Thead(
            html.Tr([
                html.Th('Aluno', className='table-header'),
                html.Th('Nota1', className='table-header'),
                html.Th('Nota2', className='table-header'),
                html.Th('Nota3', className='table-header'),
                html.Th('Nota4', className='table-header'),
                html.Th('Nota5', className='table-header'),
                html.Th('Nota6', className='table-header'),
                html.Th('Engajamento Médio', className='table-header')
            ])
        ),
        html.Tbody([
            html.Tr([
                html.Td(student, className='table-cell'),
                html.Td(cluster_data[cluster_data['NOME_ALUNO'] == student]['Nota1'].values[0], className='table-cell'),
                html.Td(cluster_data[cluster_data['NOME_ALUNO'] == student]['Nota2'].values[0], className='table-cell'),
                html.Td(cluster_data[cluster_data['NOME_ALUNO'] == student]['Nota3'].values[0], className='table-cell'),
                html.Td(cluster_data[cluster_data['NOME_ALUNO'] == student]['Nota4'].values[0], className='table-cell'),
                html.Td(cluster_data[cluster_data['NOME_ALUNO'] == student]['Nota5'].values[0], className='table-cell'),
                html.Td(cluster_data[cluster_data['NOME_ALUNO'] == student]['Nota6'].values[0], className='table-cell'),
                html.Td(cluster_data[cluster_data['NOME_ALUNO'] == student]['engajamento_n6_media'].values[0], className='table-cell')
            ])
            for student in cluster_data['NOME_ALUNO']
        ])
    ], className='styled-table')

    return cluster_title, students_list

