import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc

from src.services.data_processing import get_summary_stats, get_subsystems, get_months
from src.services.visualization import (
    create_cost_histogram, 
    create_time_series, 
    create_cost_boxplot, 
    create_cost_by_plant_bar
)


def create_dashboard(data):
    # Função principal que integra todos os componentes visuais, filtros e callbacks para construir o dashboard interativo
    app = dash.Dash(__name__, 
                   external_stylesheets=[dbc.themes.FLATLY],
                   meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1'}])
    
    subsystems = get_subsystems(data)
    months = get_months(data)
    plants = sorted(data['usina'].unique())
    stats_df = get_summary_stats(data)
    
    app.layout = dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H1("Dashboard de Custos do SIN", 
                       className="text-primary text-center my-4"),
                html.H4("Análise de Custos Variáveis Unitários de Usinas Térmicas",
                       className="text-secondary text-center mb-4")
            ], width=12)
        ]),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H4("Filtros", className="text-center")
                    ], className="bg-primary text-white"),
                    dbc.CardBody([
                        html.Label("Subsistema:", className="fw-bold mt-2"),
                        dcc.Dropdown(
                            id='subsystem-filter',
                            options=[{'label': sub, 'value': sub} for sub in subsystems],
                            value=None,
                            placeholder="Todos os Subsistemas",
                            className="mb-3"
                        ),
                        
                        html.Label("Período:", className="fw-bold mt-2"),
                        dcc.Dropdown(
                            id='month-filter',
                            options=[{'label': month, 'value': month} for month in months],
                            value=months[-1] if months else None,
                            placeholder="Escolha um mês",
                            className="mb-3"
                        ),
                        
                        html.Label("Usina (Série Temporal):", className="fw-bold mt-2"),
                        dcc.Dropdown(
                            id='plant-filter',
                            options=[{'label': plant, 'value': plant} for plant in plants],
                            value=None,
                            placeholder="Escolha uma usina",
                            className="mb-3"
                        ),
                        
                        html.Label("Agrupar Boxplot por:", className="fw-bold mt-2"),
                        dbc.RadioItems(
                            id='boxplot-group',
                            options=[
                                {'label': 'Subsistema', 'value': 'subsistema'},
                                {'label': 'Categoria de Custo', 'value': 'categoria_custo'}
                            ],
                            value='subsistema',
                            inline=True,
                            className="mb-3"
                        ),
                        
                        html.Label(f"Top Usinas:", className="fw-bold mt-2"),
                        dcc.Slider(
                            id='top-n-slider',
                            min=5,
                            max=20,
                            step=5,
                            value=10,
                            marks={i: {'label': str(i), 'style': {'font-weight': 'bold'}} for i in range(5, 25, 5)},
                            className="mb-3"
                        ),
                    ]),
                ], className="shadow"),
                
                dbc.Card([
                    dbc.CardHeader([
                        html.H4("Estatísticas", className="text-center")
                    ], className="bg-primary text-white mt-4"),
                    dbc.CardBody([
                        html.Div(id='summary-stats')
                    ])
                ], className="shadow mt-3")
            ], width=12, lg=3),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dbc.Tabs([
                            dbc.Tab([
                                dcc.Graph(id='histogram-plot', style={'height': '65vh'})
                            ], label="Distribuição", tab_id="tab-1", tab_style={"margin": "0 0.5rem"}),
                            
                            dbc.Tab([
                                dcc.Graph(id='time-series-plot', style={'height': '65vh'})
                            ], label="Evolução Temporal", tab_id="tab-2", tab_style={"margin": "0 0.5rem"}),
                            
                            dbc.Tab([
                                dcc.Graph(id='boxplot', style={'height': '65vh'})
                            ], label="Boxplot", tab_id="tab-3", tab_style={"margin": "0 0.5rem"}),
                            
                            dbc.Tab([
                                dcc.Graph(id='barplot', style={'height': '65vh'})
                            ], label="Top Usinas", tab_id="tab-4", tab_style={"margin": "0 0.5rem"})
                        ], id="tabs", active_tab="tab-1")
                    ])
                ], className="shadow h-100")
            ], width=12, lg=9)
        ], className="g-4")
    ], fluid=True, className="px-4 py-3")
    
    @app.callback(
        Output('histogram-plot', 'figure'),
        [Input('subsystem-filter', 'value'),
         Input('month-filter', 'value')]
    )
    def update_histogram(subsystem, month):
        # Callback que atualiza o histograma dinamicamente conforme o usuário seleciona diferentes subsistemas ou períodos
        filtered_data = data
        
        if month:
            filtered_data = filtered_data[filtered_data['ano_mes'] == month]
            
        return create_cost_histogram(filtered_data, subsystem)
    
    @app.callback(
        Output('time-series-plot', 'figure'),
        [Input('plant-filter', 'value')]
    )
    def update_time_series(plant):
        # Callback que atualiza o gráfico de série temporal quando o usuário seleciona uma usina específica para análise
        return create_time_series(data, plant)
    
    @app.callback(
        Output('boxplot', 'figure'),
        [Input('boxplot-group', 'value'),
         Input('month-filter', 'value')]
    )
    def update_boxplot(group_by, month):
        # Callback que reconfigura o boxplot baseado no critério de agrupamento e período selecionados pelo usuário
        filtered_data = data
        
        if month:
            filtered_data = filtered_data[filtered_data['ano_mes'] == month]
            
        return create_cost_boxplot(filtered_data, group_by)
    
    @app.callback(
        Output('barplot', 'figure'),
        [Input('subsystem-filter', 'value'),
         Input('top-n-slider', 'value'),
         Input('month-filter', 'value')]
    )
    def update_barplot(subsystem, top_n, month):
        # Callback que filtra e atualiza o gráfico de barras conforme o usuário ajusta o subsistema, número de usinas ou período
        filtered_data = data
        
        if month:
            filtered_data = filtered_data[filtered_data['ano_mes'] == month]
            
        return create_cost_by_plant_bar(filtered_data, subsystem, top_n)
    
    @app.callback(
        Output('summary-stats', 'children'),
        [Input('subsystem-filter', 'value'),
         Input('month-filter', 'value')]
    )
    def update_stats(subsystem, month):
        # Callback que recalcula as estatísticas descritivas baseadas nos filtros aplicados, mantendo coerência com os gráficos
        filtered_data = data
        
        if subsystem:
            filtered_data = filtered_data[filtered_data['subsistema'] == subsystem]
            
        if month:
            filtered_data = filtered_data[filtered_data['ano_mes'] == month]
            
        stats = get_summary_stats(filtered_data)
        
        table = html.Table([
            html.Thead(html.Tr([
                html.Th("Estatística", className="text-primary"),
                html.Th("Valor", className="text-primary")
            ])),
            html.Tbody([
                html.Tr([html.Td("Média", className="fw-bold"), html.Td(f"{stats.loc['mean', 'custo_variavel_unitario']:.2f}")]),
                html.Tr([html.Td("Mediana", className="fw-bold"), html.Td(f"{stats.loc['median', 'custo_variavel_unitario']:.2f}")]),
                html.Tr([html.Td("Mínimo", className="fw-bold"), html.Td(f"{stats.loc['min', 'custo_variavel_unitario']:.2f}")]),
                html.Tr([html.Td("Máximo", className="fw-bold"), html.Td(f"{stats.loc['max', 'custo_variavel_unitario']:.2f}")]),
                html.Tr([html.Td("Desvio Padrão", className="fw-bold"), html.Td(f"{stats.loc['std', 'custo_variavel_unitario']:.2f}")])
            ])
        ], className="table table-hover table-striped table-bordered w-100")
        
        return table
    
    return app