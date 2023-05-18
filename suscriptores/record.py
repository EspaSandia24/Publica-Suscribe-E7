##!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------
# Archivo: record.py
# Capitulo: Estilo Publica-Suscribe
# Autor(es): Perla Velasco & Yonathan Mtz. & Jorge Solís
# Version: 3.0.0 Marzo 2022
# Descripción:
#
#   Esta clase define el suscriptor que recibirá mensajes desde el distribuidor de mensajes
#   y los almacena en un archivo de texto que simula el expediente de los pacientes
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
#           |       callback()       |  - self: definición de   |  - escribe los datos  |
#           |                        |    la instancia de la    |    del adulto mayor   |
#           |                        |    clase                 |    recibidos desde el |
#           |                        |  - ch: canal de          |    distribuidor de    |
#           |                        |    comunicación entre el |    mensajes en un     |
#           |                        |    suscriptor y el       |    archivo de texto   |
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
#           +------------------------+--------------------------+-----------------------+
#           |on_message()|  - self: definición de   |  - escribe los datos  |
#           |                        |    la instancia de la    |    del adulto mayor   |
#           |                        |    clase                     |    recibidos desde el |
#           |                        |  - frame: es un       |  distribuidor de
#           |                        | objeto interno       | mensajes en un 
#           |                        | utilizado por la       | archivo de texto
#           |                        |biblioteca STOMP   |
#           |                        |para representar    ||    
#           |                        |los mensajes           |
#           |                        |STOMP recibidos   |
#           +------------------------+--------------------------+-----------------------+
#----------------------------------------------------------------------------------------
import json, time, stomp, sys, os

class Record():

    def __init__(self):
        try:
            os.mkdir('records')
        except OSError as _:
            pass
        self.topic = "record"

    def suscribe(self):
        print("Esperando datos del paciente para actualizar expediente...")
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

    def  on_message(self,frame):
        body = frame.body
        print("datos recibidos, actualizando expediente del paciente...")
        data = json.loads(body.encode("utf-8"))
        record_file = open (f"./records/{data['ssn']}.txt",'a')
        record_file.write(f"\n[{data['wearable']['date']}]: {data['name']} {data['last_name']}... ssn: {data['ssn']}, edad: {data['age']}, temperatura: {round(data['wearable']['temperature'], 1)}, ritmo    cardiaco: {data['wearable']['heart_rate']}, presión arterial: {data['wearable']['blood_pressure']}, dispositivo: {data['wearable']['id']}")
        record_file.close()
        time.sleep(1)
       

if __name__ == '__main__':
    record = Record()
    record.suscribe()
