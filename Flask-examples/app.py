# app.py
from flask import Flask
from ampq_client.rpc_client import setup_rpc_client, RPC_CLIENT
from config import Config
from routes.api import api

app = Flask(__name__)
app.config.from_object(Config)

# Registrar Blueprints
app.register_blueprint(api, url_prefix='/api')

# Configuración e inicialización del cliente RabbitMQ
setup_rpc_client(
    host=app.config['RABBITMQ_HOST'],
    username=app.config['RABBITMQ_USERNAME'],
    password=app.config['RABBITMQ_PASSWORD'],
    rpc_queue=app.config['RABBITMQ_QUEUE']
)

if __name__ == '__main__':
    app.run()
