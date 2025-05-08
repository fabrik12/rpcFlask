import amqpstorm
from amqpstorm import Message

def worker():
    # Conexión a RabbitMQ
    connection = amqpstorm.Connection('127.0.0.1', 'guest', 'guest')
    channel = connection.channel()

    # Cola de RPC existe?
    channel.queue.declare('rpc_queue')

    def on_request(message):
        print(f"Worker: Recibido -> {message.body}")

        # Procesamiento de la solicitud.
        # Logica para procesar solicitud 
        #  Ej. Mensaje invertido.
        response_body = message.body[::-1]

        # Crear un mensaje de respuesta usando la misma conexión y canal.
        response_message = Message.create(
            channel, 
            response_body,
            properties={'correlation_id': message.correlation_id}
        )

        # Mandar respuesta
        response_message.publish(
            routing_key=message.reply_to
        )
        # Confirmar que el mensaje ha sido procesado.
        message.ack()

    # Comenzar a consumir mensajes de la cola 'rpc_queue'
    channel.basic.consume(queue='rpc_queue', callback=on_request, no_ack=False)
    print("Worker iniciado. Esperando mensajes...")
    channel.start_consuming()

if __name__ == '__main__':
    worker()
