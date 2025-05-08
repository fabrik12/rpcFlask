# config.py

class Config:
    # Configuración de Flask
    SECRET_KEY = 'clave_secreta'

    # Configuración de RabbitMQ para RPC
    RABBITMQ_HOST = '127.0.0.1'
    RABBITMQ_USERNAME = 'guest'
    RABBITMQ_PASSWORD = 'guest'
    RABBITMQ_QUEUE = 'rpc_queue'
