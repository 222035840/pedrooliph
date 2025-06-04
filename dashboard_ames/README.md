# Instruções para o Dashboard Interativo - Ames Housing Dataset

## Sobre o Dashboard

Este dashboard interativo foi desenvolvido para explorar e visualizar os dados do Ames Housing Dataset. Ele permite analisar diferentes variáveis do conjunto de dados, criar visualizações personalizadas e explorar estatísticas descritivas.

## Funcionalidades

1. **Gráfico Principal**: Permite selecionar variáveis para os eixos X e Y, escolher uma variável categórica para colorir os pontos e alternar entre diferentes tipos de gráficos (dispersão, histograma, boxplot).

2. **Estatísticas Descritivas**: Exibe estatísticas básicas das variáveis selecionadas.

3. **Distribuição de Variáveis Categóricas**: Visualiza a distribuição de frequência das variáveis categóricas.

4. **Matriz de Correlação**: Permite selecionar múltiplas variáveis numéricas para visualizar suas correlações.

## Como Acessar

O dashboard está disponível temporariamente através do link:
https://8050-ijkan2ydagwta4wtb20aq-bc096365.manusvm.computer

**Observação**: Este link é temporário e ficará disponível apenas durante esta sessão.

## Como Usar

1. Acesse o link fornecido em qualquer navegador web.
2. Use os controles no painel esquerdo para selecionar as variáveis e o tipo de gráfico desejado.
3. Clique no botão "Atualizar Gráfico" para aplicar as alterações.
4. Explore as diferentes seções do dashboard para análises adicionais.

## Arquivos Incluídos

- `app.py`: Código principal do dashboard
- `dados.csv`: Amostra de dados do Ames Housing Dataset
- `assets/style.css`: Estilos personalizados para o dashboard

## Executando Localmente

Para executar o dashboard localmente, você precisará:

1. Python 3.6 ou superior
2. Pacotes: dash, pandas, plotly

Instale as dependências:
```
pip install dash pandas plotly
```

Execute o dashboard:
```
python app.py
```

Acesse em seu navegador: http://localhost:8050
