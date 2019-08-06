#!/usr/bin/python3
# -*- coding: utf-8 -*-

####################################################################################################
# Copyright 2019 Gomez Brian Agustin, Di Maria Juan Martin
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software
# and associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial
# portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
# LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO
# EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN
# AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
# OR OTHER DEALINGS IN THE SOFTWARE.
#
# License URL: https://opensource.org/licenses/mit-license.php
####################################################################################################

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


    


        
        