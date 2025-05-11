import plotly.express as px
import plotly.graph_objects as go

TEMPLATE = "plotly_white"
COLOR_SCALE = px.colors.sequential.Teal
DISCRETE_COLORS = px.colors.qualitative.Safe


def create_cost_histogram(df, subsystem=None):
    # Gera um histograma da distribuição de custos variáveis unitários, permitindo análise da frequência dos valores
    filtered_df = df if subsystem is None else df[df['subsistema'] == subsystem]
    
    fig = px.histogram(
        filtered_df, 
        x='custo_variavel_unitario',
        nbins=20,
        title=f'Distribuição de Custos Variáveis Unitários {subsystem or ""}',
        labels={'custo_variavel_unitario': 'Custo Variável Unitário (R$)'},
        color_discrete_sequence=[COLOR_SCALE[5]],
        template=TEMPLATE,
        opacity=0.8
    )
    
    fig.update_layout(
        xaxis_title='Custo Variável Unitário (R$)',
        yaxis_title='Frequência',
        bargap=0.1,
        title_x=0.5,
        legend_title_text='',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12)
    )
    
    return fig


def create_time_series(df, plant=None):
    # Cria um gráfico de linha que mostra a evolução dos custos ao longo do tempo, por usina ou média geral
    if plant:
        filtered_df = df[df['usina'] == plant]
        title = f'Evolução do Custo Variável Unitário - {plant}'
        
        fig = px.line(
            filtered_df, 
            x='data_inicio', 
            y='custo_variavel_unitario',
            title=title,
            labels={
                'data_inicio': 'Data',
                'custo_variavel_unitario': 'Custo Variável Unitário (R$)'
            },
            template=TEMPLATE,
            line_shape='spline',
            markers=True,
            color_discrete_sequence=[COLOR_SCALE[3]]
        )
    else:
        grouped_df = df.groupby('data_inicio')['custo_variavel_unitario'].mean().reset_index()
        title = 'Evolução da Média de Custos Variáveis Unitários'
        
        fig = px.line(
            grouped_df, 
            x='data_inicio', 
            y='custo_variavel_unitario',
            title=title,
            labels={
                'data_inicio': 'Data',
                'custo_variavel_unitario': 'Custo Médio Variável Unitário (R$)'
            },
            template=TEMPLATE,
            line_shape='spline',
            markers=True,
            color_discrete_sequence=[COLOR_SCALE[3]]
        )
    
    fig.update_layout(
        xaxis_title='Data',
        yaxis_title='Custo Variável Unitário (R$)',
        title_x=0.5,
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12)
    )
    
    return fig


def create_cost_boxplot(df, group_by='subsistema'):
    # Produz boxplots que revelam a distribuição estatística dos custos por subsistema ou categoria, mostrando outliers e quartis
    fig = px.box(
        df, 
        x=group_by, 
        y='custo_variavel_unitario',
        title=f'Distribuição de Custos por {group_by}',
        labels={
            group_by: group_by.capitalize(),
            'custo_variavel_unitario': 'Custo Variável Unitário (R$)'
        },
        color=group_by,
        color_discrete_sequence=DISCRETE_COLORS,
        template=TEMPLATE,
        notched=True
    )
    
    fig.update_layout(
        xaxis_title=group_by.capitalize(),
        yaxis_title='Custo Variável Unitário (R$)',
        title_x=0.5,
        legend_title_text='',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12)
    )
    
    return fig


def create_cost_by_plant_bar(df, subsystem=None, top_n=10):
    # Gera um gráfico de barras que identifica as usinas com maiores custos médios, destacando pontos críticos para análise
    filtered_df = df if subsystem is None else df[df['subsistema'] == subsystem]
    
    plant_avg = filtered_df.groupby('usina')['custo_variavel_unitario'].mean().reset_index()
    
    plant_avg = plant_avg.sort_values('custo_variavel_unitario', ascending=False).head(top_n)
    
    fig = px.bar(
        plant_avg, 
        x='usina', 
        y='custo_variavel_unitario',
        title=f'Top {top_n} Usinas com Maior Custo Médio {subsystem or ""}',
        labels={
            'usina': 'Usina',
            'custo_variavel_unitario': 'Custo Médio Variável Unitário (R$)'
        },
        color='custo_variavel_unitario',
        color_continuous_scale=COLOR_SCALE,
        template=TEMPLATE,
        text_auto='.0f'
    )
    
    fig.update_layout(
        xaxis_title='Usina',
        yaxis_title='Custo Médio Variável Unitário (R$)',
        xaxis={'categoryorder': 'total descending', 'tickangle': -45},
        title_x=0.5,
        coloraxis_colorbar=dict(title="Custo (R$)"),
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12)
    )
    
    fig.update_traces(textposition='outside')
    
    return fig


def create_stats_table(stats_df):
    # Cria uma tabela visual com estatísticas descritivas do custo variável unitário para facilitar análises quantitativas
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=['Estatística', 'Valor'],
            fill_color='#086788',
            font=dict(color='white', size=14),
            align='center',
            height=40
        ),
        cells=dict(
            values=[
                stats_df.index,
                stats_df['custo_variavel_unitario'].round(2)
            ],
            fill_color=[['#f0f5fa', '#ffffff']*10],
            font=dict(size=12),
            align='left',
            height=30
        )
    )])
    
    fig.update_layout(
        title={
            'text': 'Estatísticas Descritivas - Custo Variável Unitário',
            'x': 0.5
        },
        margin=dict(t=40, b=10, l=10, r=10),
        font=dict(size=12)
    )
    
    return fig