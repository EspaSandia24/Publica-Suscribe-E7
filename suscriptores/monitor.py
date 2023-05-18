##!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------
# Archivo: monitor.py
# Capitulo: Estilo Publica-Suscribe
# Autor(es): Perla Velasco & Yonathan Mtz. & Jorge Solís
# Version: 3.0.0 Marzo 2022
# Descripción:
#
#   Esta clase define el suscriptor que recibirá mensajes desde el distribuidor de mensajes
#   y los mostrará al área interesada para su monitoreo continuo
#
#   Este archivo también define el punto de ejecución del Suscriptor
#
#   A continuación se describen los métodos que se implementaron en esta clase:
#
#                                             Métodos:
#           +------------------------+--------------------------+-----------------------+
#           |         Nombre         |        Parámetros        |        Función        |
#           +------------------------+--------------------------+-----------------------+
#           |       __init__()       |  - self: definición de   |  - constructor de la  |
#           |                        |    la instancia de la    |    clase              |
#           |                        |    clase                 |                       |
#           +------------------------+--------------------------+-----------------------+
#           |       suscribe()       |  - self: definición de   |  - inicializa el      |
#           |                        |    la instancia de la    |    proceso de         |
#           |                        |    clase                 |    monitoreo de       |
#           |                        |                          |    signos vitales     |
#           +------------------------+--------------------------+-----------------------+
#           |        consume()       |  - self: definición de   |  - realiza la         |
#           |                        |    la instancia de la    |    suscripción en el  |
#           |                        |    clase                 |    distribuidor de    |
#           |                        |  - queue: ruta a la que  |    mensajes para      |
#           |                        |    el suscriptor está    |    comenzar a recibir |
#           |                        |    interesado en recibir |    mensajes           |
#           |                        |    mensajes              |                       |
#           +------------------------+--------------------------+-----------------------+
#           |       callback()       |  - self: definición de   |  - muetra en pantalla |
#           |                        |    la instancia de la    |    los datos del      |
#           |                        |    clase                 |    adulto mayor       |
#           |                        |  - ch: canal de          |    recibidos desde el |
#           |                        |    comunicación entre el |    distribuidor de    |
#           |                        |    suscriptor y el       |    mensajes           |
#           |                        |    distribuidor de       |                       |
#           |                        |    mensajes [propio de   |                       |
#           |                        |    RabbitMQ]             |                       |
#           |                        |  - method: método de     |                       |
#           |                        |    conexión utilizado en |                       |
#           |                        |    la suscripción        |                       |
#           |                        |    [propio de RabbitMQ]  |                       |
#           |                        |  - properties:           |                       |
#           |                        |    propiedades de la     |                       |
#           |                        |    conexión [propio de   |                       |
#           |                        |    RabbitMQ]             |                       |
#           |                        |  - body: contenido del   |                       |
#           |                        |    mensaje recibido      |                       |
#           +------------------------+--------------------------+-----------------------+
# Actualizacion por el equipo 7.
# al cambiar la tecnologia tomamos como base los metodos implementados.
# cambiamos los canales de rabbit mq por conexiones de active mq en el
#metodo consume y cambiamos el metodo callback por  el metodo on_message
#           +------------------------+--------------------------+---------------------------+
#           |on_message()|  - self: definición de   | muestra en pantalla |
#           |                        |    la instancia de la       |  los datos del             |
#           |                        |    clase                           |  adulto mayor            |
#           |                        |  - frame: es un             |  recibidos desde el   |
#           |                        | objeto interno             |  distribuidor de         |
#           |                        | utilizado por la             | mensajes                  |
#           |                        |biblioteca STOMP         |
#           |                        |para representar           |   
#           |                        |los mensajes                  |
#           |                        |STOMP recibidos           |
#           +------------------------+--------------------------+---------------------------+
#-------------------------------------------------------------------------
import json, time, stomp ,sys
class Monitor(stomp.ConnectionListener):

    def __init__(self):
        self.topic = "monitor"

    def suscribe(self):
        print("Inicio de monitoreo de signos vitales...")
        print()
        self.consume(queue=self.topic)

    def consume(self, queue, ):
        try:
            conn = stomp.Connection([('localhost', 61613)])
            conn.set_listener('', self)
            conn.connect('guest', 'guest', wait=True)
            conn.subscribe(queue, id=1, ack='auto')

            while True:
                pass

        except (KeyboardInterrupt, SystemExit):
            conn.disconnect()
            sys.exit("Conexión finalizada...")

    def on_message(self,frame):
        message=frame.body
        data = json.loads(message)
        print("ADVERTENCIA!!!")
        print(f"[{data['wearable']['date']}]: asistir al paciente {data['name']} {data['last_name']}... con wearable {data['wearable']['id']}")
        print(f"ssn: {data['ssn']}, edad: {data['age']}, temperatura: {round(data['wearable']['temperature'], 1)}, ritmo cardiaco: {data['wearable']['heart_rate']}, presión arterial: {data['wearable']['blood_pressure']}, dispositivo: {data['wearable']['id']}")
        print()
if __name__ == '__main__':
    monitor = Monitor()
    monitor.suscribe()
