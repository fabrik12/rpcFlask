# amqp_client/rpc_client.py

import threading
from time import sleep
import amqpstorm
from amqpstorm import Message

class RPCClient:
    queue = {}  # Variable de clase para mantener las respuestas

    def __init__(self, host, username, password, rpc_queue):
        self.host = host
        self.username = username
        self.password = password
        self.rpc_queue = rpc_queue
        self.connection = None
        self.channel = None
        self.callback_queue = None
        self.open()

    def open(self):
        """Conecta con RabbitMQ y declara colas necesarias."""
        self.connection = amqpstorm.Connection(self.host, self.username, self.password)
        self.channel = self.connection.channel()
        self.channel.queue.declare(self.rpc_queue)
        result = self.channel.queue.declare(exclusive=True)
        self.callback_queue = result['queue']
        self.channel.basic.consume(self._on_response, no_ack=True, queue=self.callback_queue)
        self._create_process_thread()

    def _create_process_thread(self):
        """Hilo dedicado al consumo de mensajes de respuesta."""
        thread = threading.Thread(target=self._process_data_events, daemon=True)
        thread.start()

    def _process_data_events(self):
        """Procesa eventos de datos de RabbitMQ indefinidamente."""
        self.channel.start_consuming(to_tuple=False)

    def _on_response(self, message):
        """Maneja la respuesta del mensaje RPC."""
        RPCClient.queue[message.correlation_id] = message.body

    def send_request(self, payload):
        """Envía una solicitud RPC."""
        message = Message.create(self.channel, payload)
        message.reply_to = self.callback_queue

        RPCClient.queue[message.correlation_id] = None
        message.publish(routing_key=self.rpc_queue)
        return message.correlation_id

# Instancia global para que pueda ser importada en otros módulos
RPC_CLIENT = None

def setup_rpc_client(host, username, password, rpc_queue):
    global RPC_CLIENT
    RPC_CLIENT = RPCClient(host, username, password, rpc_queue)

def get_rpc_client():
    global RPC_CLIENT
    if RPC_CLIENT is None:
        raise Exception("RPC_CLIENT no se ha inicializado. Asegúrate de llamar a setup_rpc_client() en app.py")
    return RPC_CLIENT