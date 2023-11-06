# Projeto Mercado Livre - Airflow Data Pipeline para Web Scraping + BigQuery e Looker Studio

## Visão Geral
Este projeto implementa uma pipeline de dados automatizada que executa o web scraping de ofertas no site Mercado Livre, processa esses dados e os carrega no Google Cloud Storage e no BigQuery para análises e visualizações. Os dados extraídos incluem o nome do produto, o preço e o link para a oferta.

## Ferramentas Utilizadas
As principais ferramentas e tecnologias empregadas neste projeto são:
- Apache Airflow
  * Orquestração e agendamento de tarefas de ETL
- Python
  * Desenvolvimento das tarefas de ETL
- Bibliotecas Python como Requests, BeautifulSoup, Pandas, e Google Cloud para interação com GCS e BigQuery

## Estrutura da Pipeline
A pipeline segue as etapas clássicas de ETL:
1. **Extração**: Scraping do site do Mercado Livre para obter dados de ofertas.
2. **Transformação**: Limpeza e formatação dos dados.
3. **Carga para GCS**: Armazenamento dos dados em formato Parquet no GCS.
4. **Carga para BigQuery**: Inserção dos dados em uma tabela do BigQuery.

## Análise e Visualização de Dados
Além da pipeline de ETL, este projeto também inclui uma etapa de análise de dados utilizando SQL no BigQuery, seguida da criação de um dashboard interativo no Looker Studio. Este dashboard permite visualizar os produtos, incluindo informações sobre preços e links diretos para as páginas de compra, facilitando a tomada de decisão e o acompanhamento das ofertas do Mercado Livre.

## Próximos Passos
Algumas melhorias planejadas para o futuro incluem:
- Monitoramento e alertas automatizados para a pipeline.
- Otimização da coleta de dados para escalabilidade.
- Expansão das categorias de produtos rastreados.
- Enriquecimento do dashboard com mais métricas e filtros interativos.

## Como Usar
A instalação requer uma instância configurada do Apache Airflow e credenciais apropriadas do GCP para acesso ao GCS e ao BigQuery. Instruções detalhadas de instalação e configuração podem ser encontradas aqui (inserir link para instruções).

## Links
- [Repositório GitHub](#) (Inserir o link do repositório)
- [Post LinkedIn](https://www.linkedin.com/in/matheus-picotti/) (Inserir o link do post sobre o projeto)
- [Dashboard Looker Studio](#) (Inserir o link do dashboard se público)
