# routes/api.py

from flask import Blueprint, jsonify, render_template, request
from time import sleep
from ampq_client.rpc_client import get_rpc_client

api = Blueprint('api', __name__)

# Asumiendo que instancias RPC_CLIENT en un módulo de configuración o en app.py
@api.route('/', methods=['GET', 'POST'])
def home():
    response = None
    if request.method == 'POST':
        mensaje = request.form.get('mensaje')
        if mensaje:
            # DEBUG
            rpc_client = get_rpc_client()

            # Se envía la solicitud RPC
            corr_id = rpc_client.send_request(mensaje)
            # Espera activa con un pequeño sleep (pendiente implementar un timeout)
            while rpc_client.queue.get(corr_id) is None:
                sleep(0.1)
            response = rpc_client.queue[corr_id]
    return render_template('index.html', respuesta=response)


'''
ANTERIOR
@api.route('/rpc_call/<payload>')
def rpc_call(payload):
    # Envía la solicitud RPC
    corr_id = RPCClient.send_request(payload)
    
    # Espera la respuesta 
    # Implementar posible timeout para evitar bucles infinitos)
    while RPCClient.queue.get(corr_id) is None:
        sleep(0.1)
    
    return jsonify(response=RPCClient.queue[corr_id])
'''
