#! /usr/bin/python3
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

import os
import json
import time
import Adafruit_DHT


#Conección One-Wire:
#Resistencia 10K entre VCC y DATA
#1er pin del sensor al VCC 3,3V
#2do pin del sensor DATA al BCM 17( pin numero 11 de la raspberry)
#4to pin del sensor al GND de la raspberry

sensor = Adafruit_DHT.DHT12
pin = 17

def temperaturaYhumedad():
    humedad, temperatura = Adafruit_DHT.read_retry(sensor,pin)
    return {'temperatura': temperatura, 'humedad': humedad, 'fecha': time.asctime(time.localtime(time.time()))}
 
def guardarTemperaturas(temp , oficina = 'oficina1'):
    """Funcion encargada de guardar lo leido por el sensor, en el archivo json """
    if(os.path.exists("arch/datos-oficina.json")):
        with open("arch/datos-oficina.json", "r") as f:
            dic_de_temperaturas = json.load(f)
    else:
        dic_de_temperaturas = {}

    #guardamos la nueva temperatura en el diccionario
    try :
        dic_de_temperaturas[oficina].append(temp)
    except KeyError:
        #si la oficina no estaba en el diccionario se agrega
        dic_de_temperaturas[oficina] = [temp]

    #guardamos en el archivo la nueva temperatura
    with open ("arch/datos-oficina.json", "w") as f:
        json.dump(dic_de_temperaturas, f, indent=4)

while True:
    print('Guardando en json...')
    temp = temperaturaYhumedad()
    guardarTemperaturas(temp)
    time.sleep(60)  # Espera 1 min
