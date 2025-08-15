from opensearchpy import OpenSearch, RequestsHttpConnection
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

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

timezone_br = ZoneInfo('America/Sao_Paulo')

class Logger(object):
    def __init__(self, index_name='python-logs', app_name='my-python-app'):
        # Nome do índice onde os logs serão armazenados
        self.index_name = index_name
        self.app_name = app_name
        # Checa se o índice já existe. Se não, ele é criado
        if not client.indices.exists(index=self.index_name):
            client.indices.create(index=self.index_name)

    def log(self, level, message):
        log_entry = {
            'timestamp': datetime.now(timezone_br).isoformat(),
            'level': level,
            'message': message,
            'app_name': self.app_name
        }
        # Enviando o log para o OpenSearch
        response = client.index(
            index=self.index_name,
            body=log_entry,
            refresh=True
        )
        return response


if __name__ == '__main__':
    logger = Logger(index_name='python-logs', app_name='my-python-app')
    logger.log(level='info', message='Hello World from OpenSearch!')