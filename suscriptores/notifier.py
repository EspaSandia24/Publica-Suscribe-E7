##!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------
# Archivo: notifier.py
# Capitulo: Estilo Publica-Suscribe
# Autor(es): Perla Velasco & Yonathan Mtz. & Jorge Solís
# Version: 3.0.0 Marzo 2022
# Descripción:
#
#   Esta clase define el suscriptor que recibirá mensajes desde el distribuidor de mensajes
#   y lo notificará a un(a) enfermero(a) én particular para la atención del adulto mayor en
#   cuestión
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
#           |                        |  - callback: accion a    |                       |
#           |                        |    ejecutar al recibir   |                       |
#           |                        |    el mensaje desde el   |                       |
#           |                        |    distribuidor de       |                       |
#           |                        |    mensajes              |                       |
#           +------------------------+--------------------------+-----------------------+
#           |       callback()       |  - self: definición de   |  - envía a través de  |
#           |                        |    la instancia de la    |    telegram los datos |
#           |                        |    clase                 |    del adulto mayor   |
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
#
# Actualizacion por el equipo 7.
# al cambiar la tecnologia tomamos como base los metodos implementados.
# cambiamos los canales de rabbit mq por conexiones de active mq en el
#metodo consume y cambiamos el metodo callback por  el metodo on_message
#           +------------------------+--------------------------+------------------------------+
#           |on_message()|  - self: definición de     |  - envía a través de     |
#           |                         |    la instancia de la        |   telegram los datos   |
#           |                         |    clase                            |    del adulto mayor     |
#           |                         |  - body: es el mensaje  |    recibidos desde el   |
#           |                         |  recibido para codificar |   distribuidor de         |
#           |                         |                                          |  mensajes                   |
#           +------------------------+--------------------------+------------------------------+
#----------------------------------------------------------------------------------------
import json, time, sys, stomp
import telepot

class Notifier:

    def __init__(self):
        self.topic = "notifier"
        self.token = ""
        self.chat_id = ""

    def suscribe(self):
        print("Inicio de gestión de notificaciones...")
        print()
        self.consume(queue=self.topic)

    def consume(self, queue):
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

    def on_message(self,body):
        print("enviando notificación de signos vitales...")
        if self.token and self.chat_id:
            data = json.loads(body.decode("utf-8"))
            message = f"ADVERTENCIA!!!\n[{data['wearable']['date']}]: asistir al paciente {data['name']} {data['last_name']}...\nssn: {data['ssn']}, edad: {data['age']}, temperatura: {round(data['wearable']['temperature'], 1)}, ritmo cardiaco: {data['wearable']['heart_rate']}, presión arterial: {data['wearable']['blood_pressure']}, dispositivo: {data['wearable']['id']}"
            bot = telepot.Bot(self.token)
            bot.sendMessage(self.chat_id, message)
        time.sleep(1)
    

if __name__ == '__main__':
    notifier = Notifier()
    notifier.suscribe()
