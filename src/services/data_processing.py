import pandas as pd

def load_data(filepath):
    # Carrega o arquivo CSV com dados de custos das usinas térmicas para análise posterior
    df = pd.read_csv(filepath)
    return df


def process_data(df):
    # Transforma os dados brutos: converte datas, trata valores nulos, cria categorias de custo e colunas derivadas para análise
    df['data_inicio'] = pd.to_datetime(df['data_inicio'])
    df['data_fim'] = pd.to_datetime(df['data_fim'])
    
    df['semana_do_ano'] = df['data_inicio'].dt.isocalendar().week
    
    df['custo_variavel_unitario'] = df['custo_variavel_unitario'].fillna(0)
    
    df = df.drop_duplicates()
    
    df['categoria_custo'] = pd.cut(
        df['custo_variavel_unitario'],
        bins=[0, 100, 300, 600, float('inf')],
        labels=['Baixo', 'Médio', 'Alto', 'Muito Alto']
    )
    
    df['ano_mes'] = df['data_inicio'].dt.strftime('%Y-%m')
    
    df = df.sort_values('data_inicio')
    
    return df


def get_summary_stats(df):
    # Calcula estatísticas descritivas como média, mediana e variância para oferecer uma visão quantitativa dos custos
    numeric_cols = ['custo_variavel_unitario']
    stats = df[numeric_cols].describe()
    
    stats.loc['median'] = df[numeric_cols].median()
    stats.loc['variance'] = df[numeric_cols].var()
    
    return stats


def get_subsystems(df):
    # Extrai a lista de subsistemas únicos presentes no dataset para uso nos filtros do dashboard
    return sorted(df['subsistema'].unique())


def get_months(df):
    # Obtém a lista de períodos (ano-mês) disponíveis para análise temporal nos filtros do dashboard
    return sorted(df['ano_mes'].unique())