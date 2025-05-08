# Flask con RabbitMQ para llamadas RPC en una ventana de chat

Esta es una práctica realizada para el curso de Sistemas Distribuidos. La aplicación integra Flask con RabbitMQ mediante la librería AMQPStorm para implementar llamadas RPC en tiempo real, mostrando el intercambio de mensajes en una ventana de chat.

## Tabla de Contenidos

- [Descripción](#descripción)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Tecnologías y Dependencias](#tecnologías-y-dependencias)
- [Instalación y Configuración](#instalación-y-configuración)
- [Instrucciones de Ejecución](#instrucciones-de-ejecución)
- [Uso y Funcionalidades](#uso-y-funcionalidades)
- [Notas y Consideraciones Adicionales](#notas-y-consideraciones-adicionales)
- [Licencia](#licencia)

## Descripción

Esta aplicación demuestra cómo integrar una aplicación web en Flask con RabbitMQ para realizar llamadas RPC. La idea central es que el usuario interactúe mediante una ventana de chat (implementada en `index.html`), la cual envía mensajes al servidor y recibe respuestas a través de un sistema RPC.

## Estructura del Proyecto

La estructura del repositorio es la siguiente:

```bash
project/
├── app.py # Punto de entrada principal
├── config.py # Configuración general (RabbitMQ, Flask, etc.)
├── requirements.txt # Dependencias del proyecto
├── routes/ # Capa de rutas y controladores (endpoints)
│ ├── **init**.py
│ └── api.py # Endpoints con Blueprints
├── templates/ # Archivos HTML (Jinja2 templates)
│ ├── base.html
│ └── index.html
├── amqp_client/ # Lógica y clases para manejar RabbitMQ con amqpstorm
│ ├── **init**.py
│ └── rpc_client.py # Clase RpcClient y funciones relacionadas
└── worker/ # Código del worker
└── consumer.py # Worker que consume mensajes de la cola
```

## Tecnologías y Dependencias

- **Python:** 3.12
- **Flask:** Versión 3.1.0
- **AMQPStorm:** Versión 2.11.1

Todas las dependencias se pueden instalar usando un archivo `requirements.txt` (si se crea) con el siguiente contenido:

Para instalar las dependencias, ejecuta:

```bash
pip install -r requirements.txt
```

## Instalacion y Configuracion

1. Clona el repositorio en tu máquina local:

```bash
git clone
cd
```

2. Instala las dependencias usando pip (o pipenv/poetry si lo prefieres):

```bash
pip install -r requirements.txt
```

3. No se requieren variables de entorno especiales; la configuración se maneja desde el archivo `config.py.`

## Instrucciones de Ejecución

### Para ejecutar la aplicación web:

Puedes iniciar el servidor de Flask de cualquiera de estas formas:

- Ejecutando el archivo app.py:
  ```bash
  python app.py
  ```
- O, usando el comando Flask (útil para pruebas en la LAN):
  ```
  flask run --host=0.0.0.0 --port=5000
  ```

### Para ejecutar el worker (consumidor) de RabbitMQ:

- En otra terminal, ejecuta:
  `bash
python worker/consumer.py
`
  _Asegúrate de que RabbitMQ tenga una instancia corriendo y que los puertos necesarios estén accesibles_

## Uso y Funcionalidades

- La aplicación muestra una ventana de chat en index.html.
- El usuario puede escribir un mensaje en la caja de texto y enviarlo.
- Al enviar el mensaje, se realiza una llamada RPC mediante RabbitMQ:

  - El mensaje se envía al servidor.
  - El worker (en worker/consumer.py) procesa la solicitud y devuelve una respuesta.

- La respuesta se muestra en la misma ventana de chat, permitiendo visualizar una comunicación en tiempo real.

## Notas y Consideraciones Adicionales

- **RabbitMQ**: Asegúrate de tener una instancia de RabbitMQ corriendo y accesible (verifica puertos y firewall).

- **Conexión en la LAN**: Para acceder desde otros dispositivos (por ejemplo, desde tu celular), utiliza la dirección IP local de tu máquina en lugar de localhost y ejecuta Flask con --host=0.0.0.0.

- **Reconexión y Robustez**: La práctica no implementa estrategias de reconexión. En un entorno real, se debe considerar la robustez de la conexión a RabbitMQ.

## Licencia
