from opensearchpy import OpenSearch, RequestsHttpConnection
import json
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()
password = os.getenv('OPENSEARCH_INITIAL_ADMIN_PASSWORD')

# Informações de conexão do OpenSearch
host = 'localhost'
port = 9200
auth = ('admin', password) # Usuário e senha definidos no docker-compose

# Configuração da conexão com o OpenSearch
client = OpenSearch(
    hosts=[{'host': host, 'port': port}],
    http_auth=auth,
    use_ssl=True,
    verify_certs=False,
    ssl_assert_hostname=False,
    ssl_show_warn=False,
    connection_class=RequestsHttpConnection
)

# Nome do índice onde os logs serão armazenados
index_name = 'python-logs'

# Checa se o índice já existe. Se não, ele é criado
if not client.indices.exists(index=index_name):
    client.indices.create(index=index_name)

# Exemplo de um log que será enviado
log_entry = {
    'timestamp': '2025-08-14T11:00:00Z',
    'level': 'INFO',
    'message': 'Aplicação iniciada com sucesso de novo.',
    'app_name': 'my-python-app'
}

# Enviando o log para o OpenSearch
response = client.index(
    index=index_name,
    body=log_entry,
    refresh=True
)

print("Log enviado com sucesso!")
print(json.dumps(response, indent=2))