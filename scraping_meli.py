from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator
from google.cloud import storage
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from google.cloud import bigquery
from airflow.utils.dates import days_ago

def extrair_dados(num_pages):
    """
    Extrair dados do Mercadolivre.

    Args:
    num_pages (int): Número de páginas que gostaria de extrair os dados.

    Returns:
    list: Lista de dicionários contendo nome, preço e link de cada produto.
    """
    # cria uma lista vazia para realizar o append das informações
    lista = []
    extraction_date = datetime.now().date()

    # loop dentro de cada pagina para extrair nome, preço e link de compra
    for page in range(1, num_pages + 1):
        url = f'https://www.mercadolivre.com.br/ofertas?container_id=MLB779362-1&page={page}'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # encontra a seção de produtos no HTML
        products_section = soup.find('main', {'role': 'main', 'id': 'root-app'}).find('div', {'class': 'section_promotions_web'}).find('div', {'class': 'promotions_boxed-width'})
        # obtém todos os itens de promoção
        promotion_items = products_section.find_all('li', class_=lambda x: x and 'promotion' in x)

        for item in promotion_items:
            # extrai informações de cada item
            product_name = item.find('p', {'class': 'promotion-item__title'}).text
            product_price = item.find('span', {'class': 'andes-money-amount__fraction'})
            product_price = product_price.text if product_price else None
            product_link = item.find('a', {'class': 'promotion-item__link-container'})['href']

            # adiciona os dados extraídos à lista
            lista.append({'nome_produto': product_name, 'preco': product_price, 'link': product_link, 'data_request': extraction_date})

    return lista

def transformar_e_salvar_dados(**kwargs):
    """
    Transforma os dados extraídos em um DataFrame pandas e salva em formato Parquet.
    """

    # carrega os dados do XCom retornado pela tarefa extrair_dados
    ti = kwargs['ti']
    lista = ti.xcom_pull(task_ids='extrair_dados')

    # transforma a lista de dicionários em um DataFrame
    df = pd.DataFrame(lista)

    if 'preco' not in df:
        # se a coluna 'preco' não existir, podemos optar por adicionar a coluna com valores NaN
        df['preco'] = pd.NA
    else:
        # se a coluna 'preco' existir, aplique a substituição e conversão
        df['preco'] = pd.to_numeric(df['preco'].replace({'\D': ''}, regex=True), errors='coerce')

    # defina o caminho para a pasta onde você deseja salvar os dados
    output_directory = "mercado_livre_produtos"

    # verifique se o diretório existe, senão crie
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # defina o caminho completo do arquivo Parquet
    parquet_file_path = os.path.join(output_directory, "mercado_livre_produtos.parquet")

    # salve o Dataframe em um arquivo Parquet
    df.to_parquet(parquet_file_path, index=False)

def enviar_para_gcs(bucket_name, arquivo_local, arquivo_remoto):
    """
    Envia um arquivo local para um bucket do Google Cloud Storage.

    Args:
    bucket_name (str): Nome do bucket do GCS.
    arquivo_local (str): Caminho do arquivo local a ser carregado.
    arquivo_remoto (str): Nome do arquivo no GCS.

    """
    # valida as credencias, é importante que o bucket tenha sido criado no GCS e o caminho para as credencias esteja correto
    client = storage.Client.from_service_account_json('/home/matheus-picotti/airflow_env/credentials/credenciais.json')
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(arquivo_remoto)
    blob.upload_from_filename(arquivo_local)

def carregar_para_bigquery(bucket_name, source_file_name, dataset_id, table_id):
    """
    Carrega dados do Google Cloud Storage para uma tabela do BigQuery.

    Args:
    bucket_name (str): Nome do bucket do GCS onde os dados estão armazenados.
    source_file_name (str): Nome do arquivo de origem no GCS.
    dataset_id (str): ID do dataset do BigQuery.
    table_id (str): ID da tabela do BigQuery para onde os dados serão carregados.
    """
    # valida as credenciais, o source_file_name tem que ser o mesmo arquiivo que foi enviado para o GCS na função anterior
    client = bigquery.Client.from_service_account_json('/home/matheus-picotti/airflow_env/credentials/credenciais.json')
    table_ref = client.dataset(dataset_id).table(table_id)
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.PARQUET,
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,  # da um append na tabela, se ja existir dados
    )
    uri = f"gs://{bucket_name}/{source_file_name}"
    load_job = client.load_table_from_uri(uri, table_ref, job_config=job_config)
    load_job.result()

# cria a dag para rodar todo dia ao 12:00
with DAG(
      "scraping_meli", start_date = days_ago(1),
    schedule_interval = "0 12 * * *", catchup = False
) as dag:
    
# tarefas a serem executadas

    t1 = PythonOperator(
        task_id = "extrair_dados",
        python_callable = extrair_dados,
        op_args=[5]
    )

    t2 = PythonOperator(
        task_id = "tranformar_dados",
        python_callable = transformar_e_salvar_dados
    )

    t3 = PythonOperator(
        task_id="carregar_dados_storage",
        python_callable=enviar_para_gcs,
        op_args=["teste-mercadolivre", "mercado_livre_produtos/mercado_livre_produtos.parquet", "scraping.parquet"]
    )

    t4 = PythonOperator(
        task_id="carregar_dados_bigquery",
        python_callable=carregar_para_bigquery,
        op_args=["teste-mercadolivre", "scraping.parquet", "teste", "mercadolivre_scraping_"]
    )

# orderm em que cada tarefa deve ser executada
t1 >> t2 >> t3 >> t4
