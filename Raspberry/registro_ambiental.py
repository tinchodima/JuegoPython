#! /usr/bin/python3
# -*- coding: utf-8 -*-


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
    if(os.path.exists("Rasberry/datos-oficina.json")):
        with open("Rasberry/datos-oficina.json", "r") as f:
            dic_de_temperaturas = json.load(f)
    else:
        dic_de_temperaturas = {}

    # guardamos la nueva temperatura en el diccionario
    try :
        dic_de_temperaturas[oficina].append(temp)
    except KeyError:
        # si la oficina no estaba en el diccionario se agrega
        dic_de_temperaturas[oficina] = [temp]

    # guardamos en el archivo la nueva temperatura
    with open ("arch/datos-oficina.json", "w") as f:
        json.dump(dic_de_temperaturas, f, indent=4)

while True:
    print('Guardando en json')
    temp = temperaturaYhumedad()
    guardarTemperaturas(temp)
    time.sleep(60)  # Espera 1 min
