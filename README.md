# Dashboard de Análise de Custos Variáveis Unitários - SIN

## Descrição do Projeto

Este dashboard interativo foi desenvolvido para analisar os custos variáveis unitários das usinas térmicas do Sistema Interligado Nacional (SIN) brasileiro. A ferramenta permite visualizar, filtrar e explorar dados de custos operacionais, oferecendo insights importantes para a tomada de decisões no setor energético.

## Objetivo

O principal objetivo deste dashboard é facilitar a análise e compreensão dos padrões de custos operacionais das usinas térmicas, permitindo identificar:

- Distribuição geral dos custos variáveis unitários
- Evolução temporal dos custos
- Comparação entre diferentes subsistemas
- Identificação das usinas com maiores custos médios
- Análise estatística detalhada dos dados

## Conjunto de Dados

Os dados utilizados neste projeto contêm informações sobre os custos variáveis unitários das usinas térmicas do SIN, incluindo:

- Datas de início e fim dos períodos de análise
- Identificação das usinas e subsistemas
- Valores dos custos variáveis unitários
- Informações sobre semanas operativas e revisões

## Requisitos

- Python 3.11 ou superior
- Poetry (gerenciador de dependências Python)

## Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/seu-usuario/atividade-avaliativa-dashboard-unit-variable-cost.git
   cd atividade-avaliativa-dashboard-unit-variable-cost
   ```

2. Instale as dependências com Poetry:

   ```bash
   poetry install
   ```

3. Ative o ambiente virtual:
   ```bash
   poetry shell
   ```

## Execução

Para iniciar o dashboard, execute:

```bash
python src/main.py
```

O dashboard estará disponível no navegador através do endereço: `http://127.0.0.1:8080`

## Como Utilizar o Dashboard

### Painel de Filtros

O dashboard possui vários filtros interativos que permitem personalizar a análise:

- **Subsistema**: Selecione um subsistema específico para filtrar os dados (ex: NORTE, SUL)
- **Período**: Escolha um mês específico para analisar dados daquele período
- **Usina**: Selecione uma usina específica para visualizar sua evolução temporal de custos
- **Agrupar Boxplot por**: Alterne entre agrupar os boxplots por subsistema ou categoria de custo
- **Top Usinas**: Defina quantas usinas devem aparecer no ranking de maiores custos médios (5 a 20)

### Visualizações Disponíveis

O dashboard apresenta quatro visualizações principais, acessíveis através de abas:

1. **Distribuição**: Histograma mostrando a distribuição de frequência dos custos variáveis unitários
2. **Evolução Temporal**: Gráfico de linha que mostra como os custos variaram ao longo do tempo
3. **Boxplot**: Exibe a distribuição estatística (mediana, quartis e outliers) dos custos por grupo
4. **Top Usinas**: Gráfico de barras identificando as usinas com maiores custos médios

### Estatísticas

O painel de estatísticas exibe métricas descritivas importantes sobre os dados filtrados:

- Média
- Mediana
- Valor mínimo
- Valor máximo
- Desvio padrão

Todas as estatísticas são atualizadas dinamicamente quando você aplica filtros.
