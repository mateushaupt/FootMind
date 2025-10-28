import os
from app import create_app
from config import ProductionConfig, Config

# Determina o ambiente atual (pode ser 'production' ou 'development')
# A variável de ambiente FLASK_ENV deve ser configurada
env = os.environ.get('FLASK_ENV', 'development')

# Seleciona a configuração apropriada
if env == 'production':
    config_class = ProductionConfig
else:
    # Usa a configuração base (development) por padrão
    config_class = Config

# Cria a instância da aplicação Flask usando o Application Factory
app = create_app(config_class)

# Este bloco permite que você execute o servidor diretamente com 'python run.py'
# embora o comando 'flask run' ainda seja o mais recomendado para ambientes de desenvolvimento.
if __name__ == '__main__':
    # A função run() do Flask usará as configurações de DEBUG e HOST/PORT definidas em config.py
    app.run()