#!/usr/bin/python3
# -*- coding: utf-8 -*-


import RPi.GPIO as GPIO
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT
import time
import registro_ambiental as ra


"""
A0  --> pin 7
VCC --> pin 2
GND --> pin 6
D0  --> pin 15 (BCM22)
"""

#Configuro todo lo relacionado al microfono
GPIO.setmode(GPIO.BCM)
canal = 22
GPIO.setup(canal, GPIO.IN)
# Desactivo las warnings por tener más de un circuito en la GPIO
GPIO.setwarnings(False)
GPIO.add_event_detect(canal, GPIO.RISING)

def sonido_detectado(canal):
    '''
        devuelve el estado del microfono, si detecto o no un sonido
    '''
    sonido = False
    if GPIO.event_detected(canal):
        sonido = True
    return sonido

#Se configura todo lo relacionado a la matriz LED

# Activamos los sensores que vamos a usar
# matriz = Matriz(numero_matrices=2, ancho=16)

numero_matrices=1
orientacion=0
rotacion=0
ancho=8
alto=8

#Fuentes disponibles
font = [CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT]
#inicializar la matriz
serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, width=ancho, height=alto, cascaded=numero_matrices, rotate=rotacion)

def mostrar_mensaje(msg, delay=0.5, font=1):
    '''
        Muestra el mensaje en la matriz
    '''
    show_message(device, msg, fill="white",
                     font=proportional(font[font]),
                     scroll_delay=delay)



while True:
    temperatura = ra.temperaturaYhumedad()
    if sonido_detectado(canal):
        mostrar_mensaje(temperatura)


    


        
        