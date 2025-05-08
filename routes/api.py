# routes/api.py

from flask import Blueprint, jsonify, render_template, request
from time import sleep
from ampq_client.rpc_client import get_rpc_client

api = Blueprint('api', __name__)

@api.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@api.route('/rpc_call', methods=['POST'])
def rpc_call():
    response = None
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
        return jsonify(response=response)
    return jsonify(response="No se recibio mensaje"), 400


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
