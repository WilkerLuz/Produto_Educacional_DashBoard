import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px

# Importe as páginas separadas
from perfil_alunos import layout as layout_page1
from conhecimentos_previos import layout as layout_page2
from atividade1_robo_aspirador import layout as layout_page3
from atividade2_uma_receita import layout as layout_page4
from atividade3 import layout as layout_page6
from boletim import layout as layout_page5
from atividade4 import layout as layout_page7
from atividade5 import layout as layout_page8
from atividade6 import layout as layout_page9


# Inicialize a aplicação Dash
app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=['styles.css'])

# Estilo para os links do menu
link_style = {
    'color': '#FFF',  # Cor do texto dos links
    'text-decoration': 'none',  # Remover sublinhado
    'fontSize': '18px',  # Tamanho da fonte: 18px
    'textDecoration': 'none',  # Remova a sublinhado
    'borderBottom': '2px solid #555',  # Estilo da borda inferior: 2px sólido cinza mais escuro
    'margin': '0 10px',  # Espaçamento entre os links
    'display': 'inline-block',  # Exibir elementos na mesma linha
    'vertical-align': 'bottom',  # Alinhar elementos na parte inferior
}


# Defina o layout da página inicial com links para as páginas
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.H1(
        "LEARNING ANALYTICS NO ENSINO DE PROGRAMAÇÃO",
        style={
            'font-family': 'arial,helvetica',  # Fonte
            'textAlign': 'center',  # Alinhar o texto ao centro
            'color': '#555',  # Cor do texto: cinza mais escuro
            'fontSize': '30px',  # Tamanho da fonte: 24px
            'marginTop': '20px',  # Margem superior: 20px
        }
    ),
    html.Div([
        html.Nav([
            dcc.Link('Boletim Individual', href='/page-5', style=link_style),
            dcc.Link('Perfil dos Alunos', href='/page-1', style=link_style),
            dcc.Link('Conhecimentos Prévios', href='/page-2', style=link_style),
            dcc.Link('Atividade 1', href='/page-3', style=link_style),
            dcc.Link('Atividade 2', href='/page-4', style=link_style),
            dcc.Link('Atividade 3', href='/page-6', style=link_style),
            dcc.Link('Atividade 4', href='/page-7', style=link_style),
            dcc.Link('Atividade 5', href='/page-8', style=link_style),
            dcc.Link('Atividade 6', href='/page-9', style=link_style),
            dcc.Link('Avaliação', href='/page-10', style=link_style),

        ],
            style={
                'background-color': '#333',
                'padding': '20px',
                'text-align': 'center',
                'font-size': '18px',
                'font-family': 'arial,helvetica',  # Fonte
                'border-bottom': '2px solid #555'
            }
        )
    ]),
    html.Div(id='page-content')
])


# Callback para atualizar o conteúdo da página com base na URL
@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-1':
        return layout_page1
    elif pathname == '/page-2':
        return layout_page2
    elif pathname == '/page-3':
        return layout_page3
    elif pathname == '/page-4':
        return layout_page4
    elif pathname == '/page-5':
        return layout_page5
    elif pathname == '/page-6':
        return layout_page6
    elif pathname == '/page-7':
        return layout_page7
    elif pathname == '/page-8':
        return layout_page8
    elif pathname == '/page-9':
        return layout_page9
    else:
        return "Página não encontrada"


if __name__ == '__main__':
    app.run_server(debug=True)
