##!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------
# Archivo: publicador.py
# Capitulo: Estilo Publica-Suscribe
# Autor(es): Perla Velasco & Yonathan Mtz. & Jorge Solís
# Version: 3.0.0 Marzo 2022
# Descripción:
#
#   Este archivo define la conexión del publicador hacia el el distribuidor de mensajes
#
#   A continuación se describen los métodos que se implementaron en este archivo:
#
#                                             Métodos:
#           +------------------------+--------------------------+-----------------------+
#           |         Nombre         |        Parámetros        |        Función        |
#           +------------------------+--------------------------+-----------------------+
#           |        publish()       |  - queue: nombre de la   |  - publica el mensaje |
#           |                        |    ruta con la que se    |    en el distribuidor |
#           |                        |    vinculará el mensaje  |    de mensajes        |
#           |                        |    enviado               |                       |
#           |                        |  - data: mensaje que     |                       |
#           |                        |    será enviado          |                       |
#           +------------------------+--------------------------+-----------------------+
#Modificado por el equipo 7.
#Al cambiar la tecnología, conservamos el metodo proporcionado con canales
#pero usamos una conexion para usar active mq
#-------------------------------------------------------------------------
import stomp

def publish(queue, data):
    connection = stomp.Connection([("localhost", 61613)])
    connection.connect("guest", "guest", wait=True)
    connection.send(queue, data)
    connection.disconnect()

