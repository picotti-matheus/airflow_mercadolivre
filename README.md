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
- Extrair mais dados dos produtos.
- Enriquecimento do dashboard com mais métricas e filtros interativos.
- Criação de camadas de consultas: bronze, silver e gold.

## Como Usar
A instalação requer uma instância configurada do Apache Airflow e credenciais apropriadas do GCP para acesso ao GCS e ao BigQuery.

## Links
- [Post LinkedIn](https://www.linkedin.com/posts/matheus-picotti-528904158_dataengineering-etl-airflow-activity-7127399247129288704-WZ72?utm_source=share&utm_medium=member_desktop)
- [Dashboard Looker Studio]((https://lookerstudio.google.com/u/0/reporting/337e2116-5f23-4615-b503-3272ba994178/page/SkOhD)https://lookerstudio.google.com/u/0/reporting/337e2116-5f23-4615-b503-3272ba994178/page/SkOhD)
