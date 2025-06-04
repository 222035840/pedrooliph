import dash
from dash import dcc, html, Input, Output, State, callback
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Carregar os dados
df = pd.read_csv('dados.csv')

# Inicializar o aplicativo Dash
app = dash.Dash(__name__, meta_tags=[
    {"name": "viewport", "content": "width=device-width, initial-scale=1"}
])
server = app.server

# Definir cores e estilo
colors = {
    'background': '#f8f9fa',
    'text': '#343a40',
    'primary': '#007bff',
    'secondary': '#6c757d',
    'success': '#28a745',
    'info': '#17a2b8',
    'warning': '#ffc107',
    'danger': '#dc3545',
    'light': '#f8f9fa',
    'dark': '#343a40'
}

# Preparar opções para os dropdowns
numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
categorical_columns = df.select_dtypes(include=['object']).columns.tolist()

# Layout do aplicativo
app.layout = html.Div(style={'backgroundColor': colors['background'], 'padding': '20px'}, children=[
    html.H1(
        children='Dashboard Interativo - Ames Housing Dataset',
        style={
            'textAlign': 'center',
            'color': colors['primary'],
            'marginBottom': '30px',
            'fontFamily': 'Arial, sans-serif'
        }
    ),
    
    html.Div([
        html.Div([
            html.H3('Filtros', style={'color': colors['text'], 'marginBottom': '15px'}),
            html.Label('Selecione a variável X (numérica):'),
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': col, 'value': col} for col in numeric_columns],
                value='GrLivArea' if 'GrLivArea' in numeric_columns else numeric_columns[0],
                clearable=False
            ),
            
            html.Label('Selecione a variável Y (numérica):', style={'marginTop': '15px'}),
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': col, 'value': col} for col in numeric_columns],
                value='SalePrice' if 'SalePrice' in numeric_columns else numeric_columns[1],
                clearable=False
            ),
            
            html.Label('Selecione a variável para cor (categórica):', style={'marginTop': '15px'}),
            dcc.Dropdown(
                id='color-column',
                options=[{'label': col, 'value': col} for col in categorical_columns],
                value=None
            ),
            
            html.Label('Tipo de gráfico:', style={'marginTop': '15px'}),
            dcc.RadioItems(
                id='chart-type',
                options=[
                    {'label': 'Dispersão', 'value': 'scatter'},
                    {'label': 'Histograma', 'value': 'histogram'},
                    {'label': 'Boxplot', 'value': 'box'}
                ],
                value='scatter',
                labelStyle={'display': 'block', 'marginBottom': '5px'}
            ),
            
            html.Button(
                'Atualizar Gráfico',
                id='update-button',
                n_clicks=0,
                style={
                    'backgroundColor': colors['primary'],
                    'color': 'white',
                    'border': 'none',
                    'padding': '10px 15px',
                    'marginTop': '20px',
                    'borderRadius': '5px',
                    'cursor': 'pointer'
                }
            )
        ], style={'width': '25%', 'float': 'left', 'padding': '20px', 'backgroundColor': colors['light'], 'borderRadius': '10px', 'boxShadow': '0px 0px 10px rgba(0,0,0,0.1)'}),
        
        html.Div([
            dcc.Graph(id='main-graph'),
            html.Div(id='stats-container', style={'marginTop': '20px'})
        ], style={'width': '70%', 'float': 'right', 'padding': '20px', 'backgroundColor': colors['light'], 'borderRadius': '10px', 'boxShadow': '0px 0px 10px rgba(0,0,0,0.1)'})
    ], style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'space-between'}),
    
    html.Div([
        html.H3('Estatísticas Descritivas', style={'color': colors['text'], 'marginTop': '30px', 'marginBottom': '15px'}),
        html.Div(id='descriptive-stats')
    ], style={'clear': 'both', 'padding': '20px', 'marginTop': '20px', 'backgroundColor': colors['light'], 'borderRadius': '10px', 'boxShadow': '0px 0px 10px rgba(0,0,0,0.1)'}),
    
    html.Div([
        html.H3('Distribuição das Variáveis Categóricas', style={'color': colors['text'], 'marginTop': '30px', 'marginBottom': '15px'}),
        html.Label('Selecione a variável categórica:'),
        dcc.Dropdown(
            id='categorical-column',
            options=[{'label': col, 'value': col} for col in categorical_columns],
            value=categorical_columns[0] if categorical_columns else None,
            clearable=False
        ),
        dcc.Graph(id='categorical-graph')
    ], style={'clear': 'both', 'padding': '20px', 'marginTop': '20px', 'backgroundColor': colors['light'], 'borderRadius': '10px', 'boxShadow': '0px 0px 10px rgba(0,0,0,0.1)'}),
    
    html.Div([
        html.H3('Matriz de Correlação', style={'color': colors['text'], 'marginTop': '30px', 'marginBottom': '15px'}),
        html.Label('Selecione as variáveis numéricas (máximo 10):'),
        dcc.Dropdown(
            id='correlation-columns',
            options=[{'label': col, 'value': col} for col in numeric_columns],
            value=numeric_columns[:5] if len(numeric_columns) > 5 else numeric_columns,
            multi=True
        ),
        dcc.Graph(id='correlation-graph')
    ], style={'clear': 'both', 'padding': '20px', 'marginTop': '20px', 'backgroundColor': colors['light'], 'borderRadius': '10px', 'boxShadow': '0px 0px 10px rgba(0,0,0,0.1)'}),
    
    html.Footer([
        html.P('Dashboard Interativo para Análise de Dados Imobiliários - Ames Housing Dataset', 
               style={'textAlign': 'center', 'color': colors['secondary'], 'marginTop': '30px'})
    ])
])

# Callback para atualizar o gráfico principal
@callback(
    Output('main-graph', 'figure'),
    Input('update-button', 'n_clicks'),
    State('xaxis-column', 'value'),
    State('yaxis-column', 'value'),
    State('color-column', 'value'),
    State('chart-type', 'value')
)
def update_graph(n_clicks, xaxis_column, yaxis_column, color_column, chart_type):
    if chart_type == 'scatter':
        fig = px.scatter(
            df, 
            x=xaxis_column, 
            y=yaxis_column,
            color=color_column,
            title=f'Relação entre {xaxis_column} e {yaxis_column}',
            labels={xaxis_column: xaxis_column, yaxis_column: yaxis_column},
            hover_data=['Order'] + ([color_column] if color_column else [])
        )
    elif chart_type == 'histogram':
        fig = px.histogram(
            df, 
            x=xaxis_column,
            color=color_column,
            title=f'Distribuição de {xaxis_column}',
            labels={xaxis_column: xaxis_column},
            marginal="box"
        )
    elif chart_type == 'box':
        if color_column:
            fig = px.box(
                df, 
                x=color_column, 
                y=yaxis_column,
                title=f'Boxplot de {yaxis_column} por {color_column}',
                labels={color_column: color_column, yaxis_column: yaxis_column}
            )
        else:
            fig = px.box(
                df, 
                y=yaxis_column,
                title=f'Boxplot de {yaxis_column}',
                labels={yaxis_column: yaxis_column}
            )
    
    fig.update_layout(
        plot_bgcolor=colors['light'],
        paper_bgcolor=colors['light'],
        font_color=colors['text'],
        margin=dict(l=40, r=40, t=50, b=40),
        hovermode='closest'
    )
    
    return fig

# Callback para atualizar as estatísticas descritivas
@callback(
    Output('descriptive-stats', 'children'),
    Input('update-button', 'n_clicks'),
    State('xaxis-column', 'value'),
    State('yaxis-column', 'value')
)
def update_stats(n_clicks, xaxis_column, yaxis_column):
    stats_x = df[xaxis_column].describe().reset_index()
    stats_y = df[yaxis_column].describe().reset_index()
    
    stats_x.columns = ['Estatística', xaxis_column]
    stats_y.columns = ['Estatística', yaxis_column]
    
    stats_combined = pd.merge(stats_x, stats_y, on='Estatística')
    
    table_header = [html.Tr([html.Th('Estatística'), html.Th(xaxis_column), html.Th(yaxis_column)])]
    
    table_rows = []
    for i, row in stats_combined.iterrows():
        table_rows.append(html.Tr([
            html.Td(row['Estatística']),
            html.Td(f"{row[xaxis_column]:.2f}" if isinstance(row[xaxis_column], (int, float)) else row[xaxis_column]),
            html.Td(f"{row[yaxis_column]:.2f}" if isinstance(row[yaxis_column], (int, float)) else row[yaxis_column])
        ]))
    
    table = html.Table(table_header + table_rows, style={
        'width': '100%',
        'borderCollapse': 'collapse',
        'marginTop': '15px'
    })
    
    return table

# Callback para atualizar o gráfico categórico
@callback(
    Output('categorical-graph', 'figure'),
    Input('categorical-column', 'value')
)
def update_categorical_graph(categorical_column):
    if not categorical_column:
        return go.Figure()
    
    value_counts = df[categorical_column].value_counts().reset_index()
    value_counts.columns = [categorical_column, 'Count']
    
    # Limitar a 15 categorias para melhor visualização
    if len(value_counts) > 15:
        top_values = value_counts.head(14)
        other_count = value_counts.iloc[14:]['Count'].sum()
        other_row = pd.DataFrame({categorical_column: ['Outros'], 'Count': [other_count]})
        value_counts = pd.concat([top_values, other_row], ignore_index=True)
    
    fig = px.bar(
        value_counts, 
        x=categorical_column, 
        y='Count',
        title=f'Distribuição de {categorical_column}',
        labels={categorical_column: categorical_column, 'Count': 'Contagem'},
        color='Count',
        color_continuous_scale=px.colors.sequential.Blues
    )
    
    fig.update_layout(
        plot_bgcolor=colors['light'],
        paper_bgcolor=colors['light'],
        font_color=colors['text'],
        margin=dict(l=40, r=40, t=50, b=100),
        xaxis={'categoryorder': 'total descending'}
    )
    
    # Rotacionar os rótulos do eixo x para melhor legibilidade
    fig.update_xaxes(tickangle=45)
    
    return fig

# Callback para atualizar a matriz de correlação
@callback(
    Output('correlation-graph', 'figure'),
    Input('correlation-columns', 'value')
)
def update_correlation_graph(selected_columns):
    if not selected_columns or len(selected_columns) < 2:
        return go.Figure()
    
    # Limitar a 10 colunas para melhor visualização
    if len(selected_columns) > 10:
        selected_columns = selected_columns[:10]
    
    corr_matrix = df[selected_columns].corr().round(2)
    
    fig = px.imshow(
        corr_matrix,
        text_auto=True,
        color_continuous_scale=px.colors.diverging.RdBu_r,
        title='Matriz de Correlação',
        aspect="auto"
    )
    
    fig.update_layout(
        plot_bgcolor=colors['light'],
        paper_bgcolor=colors['light'],
        font_color=colors['text'],
        margin=dict(l=40, r=40, t=50, b=40)
    )
    
    return fig

# Executar o servidor
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
