#Gomez, Brian Agustin
#Di Maria, Juan Martin
#! /usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os
import PySimpleGUI as sg
from pattern.web import Wiktionary
from pattern.es import parse,split
import SopaDeLetras as sdl
import json
import statistics

def clasificarPalabraWiktionary(palabra):		
    w = Wiktionary(language="es")
    a = w.search(palabra)
    encontre = '9999'
    try:	
        clasificacion = a.sections[3].content.split()[0]

        if clasificacion.lower() == "sustantivo":
            encontre = 'NN'
            return encontre
        elif clasificacion.lower() == "adjetivo" or "forma adjetiva":
            encontre = 'JJ'
            return encontre
        elif clasificacion.lower() == "verbo" or "verbo intransitivo":
            encontre = 'VB'
            return encontre
    except(AttributeError):
        return 'No se pudo clasificar'

def clasificarPalabraPattern(palabra):
    '''
    clasifica el string recibido como paramentro en pattern, analizando la palabra, devuleve su clasificacion
    (sustantivo, adjetivo o verbo).
    '''
    s = parse(palabra).split()
    encontre = '9999'
    try:
        for cada in s:
            for i in cada:
                if i[1] == 'VB':
                    encontre = 'VB'
                    return encontre
                elif i[1] == 'NN':
                    encontre = 'NN'
                    return encontre
                elif i[1] == 'JJ':
                    encontre = 'JJ'
                    return encontre
    except(AttributeError):
        return 'No se pudo clasificar'


def comprobarWikPattern2(palabra,listaPalabras,values):
    if (clasificarPalabraWiktionary(palabra) != '9999' and clasificarPalabraPattern(palabra) != '9999') and (clasificarPalabraWiktionary(palabra) == clasificarPalabraPattern(palabra)):
        clasificacionWiktionary(palabra,listaPalabras,values)
        definiciones[palabra] = obtenerDefinicion(palabra)
    elif (clasificarPalabraWiktionary(palabra) != '9999' and clasificarPalabraPattern(palabra) != '9999') and (clasificarPalabraWiktionary(palabra) != clasificarPalabraPattern(palabra)):
        clasificacionWiktionary(palabra,listaPalabras,values) 
        definiciones[palabra] = obtenerDefinicion(palabra)
        msg = 'Clasificacion no encontrada en Pattern, se tomara la clasificacion de Wiktionary'
        reporteClasificaciones(msg)
    if clasificarPalabraWiktionary(palabra) == '9999' and clasificarPalabraPattern(palabra) != '9999':
    	clasificacionPattern(palabra,listaPalabras)
    	sg.Popup('La clasificacion no se encuentra en Wiktionary, ingresar una definicion manualmente')
    	text = sg.PopupGetText(palabra, 'Ingrese una definicion')
    	definiciones[palabra] = text

    if clasificarPalabraWiktionary(palabra) == '9999' and clasificarPalabraPattern(palabra) == '9999':
        msg = 'Clasificacion no encontrada en Wiktionary y Pattern'
        reporteClasificaciones(msg)


def clasificacionWiktionary(p, listaPalabras,values):
    try:
        if comprobarQueLaPalabraNoEsteAgregada(p,listaPalabras) == False:
            sg.Popup('La palabra ya esta agregada en la sopa de letras')
        else:
            if clasificarPalabraWiktionary(p) == 'NN':
                listaSustantivos.append(p)
                listaPalabras.append(p)
            elif clasificarPalabraWiktionary(p) == 'JJ':
                listaAdjetivos.append(p)
                listaPalabras.append(p)
            elif clasificarPalabraWiktionary(p) == 'VB':
                listaPalabras.append(p)
                listaVerbos.append(p)
            else:
                print('No se pudo agregar')
            
    except(AttributeError):
        print('No se pudo agregar')
    except(AttributeError):
    	print('Error de atributo')

def clasificacionPattern(p, listaPalabras):
	try:
		if comprobarQueLaPalabraNoEsteAgregada(p,listaPalabras) == False:
			sg.Popup('La palabra ya esta agregada en la sopa de letras')
		else:
		    if clasificarPalabraPattern(p) == 'NN':
			    listaSustantivos.append(p)
			    listaPalabras.append(p)
		    elif clasificarPalabraPattern(p) == 'JJ':
			    listaAdjetivos.append(p)
			    listaPalabras.append(p)
		    elif clasificarPalabraPattern(p) == 'VB':
			    listaVerbos.append(p)
			    listaPalabras.append(p)
		    else:
			    print('No se pudo agregar')
            
	except(AttributeError):
		print('No se pudo agregar')

def comprobarQueLaPalabraNoEsteAgregada(palabra,listaPalabras):		
	if palabra in listaPalabras:
		return False
	else:
		return True


def reporteClasificaciones(error):
	f = open('reporte.txt', 'a')
	f.write(error + '\n')
	f.close

def obtenerDefinicion(palabra):
	w = Wiktionary(language="es")
	a = w.search(palabra)
	try:
		definicion = a.sections[3].content.split('1')[1].split('.2')[0].split('*')[0]
	except(IndexError):
		try:
			definicion = a.sections[3].content.split('1')[0].split('*')[1]
			if ' ' in definicion[1]:
				try:
					definicion = a.sections[3].content.split('1')[0].split('*')[2]
				except(IndexError):
					definicion = a.sections[3].content.split('1')[0].split('*')[3]
		except(IndexError):
				definicion = a.sections[3].content.split('1')[0].split('*')[2]
	except(AttributeError):
		definicion = sg.Popup('Esta palabra no existe en wiki ni en pattern')
		msg = 'Clasificacion no encontrada en Wiktionary y Pattern'
		reporteClasificaciones(msg)
	return definicion
		

def getDatos():
	'''
		Retorna los datos y la configuracion para usar en la sopa de letras
	'''
	return listaPalabras

def getColores():
	'''
		Retorna los colores de los tipos de palabras
	'''	
	return colores

def getAyuda():
	'''
		1: Sin ayuda
		2: Mostrar definiciones
		3: Mostrar palabras a buscar
		Devuelve en una tupla el tipo de ayuda seleccionado
	'''	
	return ayuda

def getOri():
	return orientacion	

def getDefiniciones():
	'''
		Devuelve un diccionario con la palabra como clave y la definicion como valor
	'''
	return definiciones

def getFuente():
	return fuente

def getTipo():
	return mayOmin

def getCantPal():
	return cantPal

def getColorFondo():
	return fondo

def promedio():
	dire = os.path.abspath(os.path.join(os.path.join(os.pardir, 'Raspberry'), 'datos-oficinas.json'))
	#dire = r'C:\Users\Dima\Desktop\datos-oficina.json'
	try:    
		promedioTemperaturas = {}
		oficinas = {}
		oficinasJSON = open(dire)
		oficinas = json.load(oficinasJSON)
		listaTemperaturas = []
		for oficina in oficinas:
			for temperatura in oficinas[oficina]:
				listaTemperaturas.append(int(temperatura['temp']))
			promedioTemperaturas[oficina] = statistics.mean(listaTemperaturas)
		print(promedioTemperaturas)
	except(FileNotFoundError):
		promedioTemperaturas[''] = 0
		sg.PopupNoButtons('No se encontraron oficinas',title='', auto_close_duration=2, auto_close=True)

	return promedioTemperaturas


layout = [
	[sg.T('DIGOM: SOPA DE LETRAS', size=(32, 1), font=('Time New Roman', 20), background_color='#80cbc4')],
	[sg.T('● Cantidad de palabras que se van a ingresar a la sopa de letras', text_color='black',font=('Time New Roman', 12), background_color='#80cbc4')],
	[sg.T('Sustantivos', text_color='black',font=('Time New Roman', 10), background_color='#80cbc4'),sg.Spin([i for i in range(0,11)], initial_value=0, size=(2,2), key=('cantS')),sg.Text('Adjetivos', text_color='black',font=('Time New Roman', 10), background_color='#80cbc4'),sg.Spin([i for i in range(0,11)], initial_value=0, size=(2,2), key=('cantA')),sg.Text('Verbos', text_color='black',font=('Time New Roman', 10), background_color='#80cbc4'),sg.Spin([i for i in range(0,11)], initial_value=0, size=(2,2), key=('cantV'))],
	[sg.T('● Ingrese una palabra:', text_color='black',font=('Time New Roman', 12), background_color='#80cbc4'), sg.InputText(key='textoIngresado'), sg.Submit('Agregar'), sg.Submit('Quitar')],
	[sg.Multiline(key='dato', size=(70,1), font='Arial', text_color='blue')],
	[sg.T('● Nivel de dificultad:   ', text_color='black', font=('Time New Roman', 12),background_color='#80cbc4'), sg.Radio('Sin ayuda ', "RADIO1", default=True, background_color='#80cbc4', key='sinAyuda'), sg.Radio('Con definiciones', "RADIO1", background_color='#80cbc4', key='mosDef'), sg.Radio('Mostrando las palabras a buscar', "RADIO1", background_color='#80cbc4', key='mosPal')],
	[sg.T('● Orientación de las palabras:   ', text_color='black', font=('Time New Roman', 12), background_color='#80cbc4'), sg.Radio('Horizontal', "RADIO2", default=True, background_color='#80cbc4', key='horizontal'), sg.Radio('Vertical', "RADIO2", background_color='#80cbc4', key='vertical')],
	[sg.T('● Fuente: ', text_color='black', font=('Time New Roman', 12), background_color='#80cbc4'), sg.InputCombo(['Arial', 'Helvetica', 'Calibri', 'Consolas', 'Tahoma', 'Courier', 'Verdana', 'Times', 'Fixedsys'], size=(12, 20), key='font', readonly=True)],
	[sg.T('● Tipo: ', text_color='black', font=('Time New Roman', 12), background_color='#80cbc4'),sg.InputCombo(['Mayúscula', 'Minúscula'], size=(12, 20), key='mayOmin', readonly=True)],
	[sg.T('● Oficina', background_color='#80cbc4', font=('Time New Roman', 12)), sg.InputCombo(values=list(promedio().keys()), key='oficinas', readonly=True)],
	[sg.T('● Elegir colores: ',text_color='black', font=('Time New Roman', 12), background_color='#80cbc4'), sg.ColorChooserButton('Sustantivos',button_color=('#000000','#03A9F4')), sg.ColorChooserButton('Adjetivos',button_color=('#000000','#03A9F4')), sg.ColorChooserButton('Verbos',button_color=('#000000','#03A9F4'))],
	[sg.Submit('Generar sopa de letras'), sg.Cancel('Salir')]
]
window = sg.Window('Seminario de Lenguajes 2019: Python', font=('Arial', 10), background_color='#80cbc4').Layout(layout)

listaSustantivos = []	
listaAdjetivos = []
listaVerbos = []
listaPalabrasAceptadas = []
listaPalabras = []
definiciones= {}

while True:
	button, values = window.Read()

	if button == 'Salir':
		break		

	if button == 'Agregar':			
		comprobarWikPattern2(values['textoIngresado'], listaPalabras,values)
		mostrar = ', '.join(listaPalabras)
		window.FindElement('dato').Update(mostrar)
		window.FindElement('textoIngresado').Update('')
		
	if button == 'Quitar':
		listaPalabras.remove(values['textoIngresado'])
		if values['textoIngresado'] in listaSustantivos:
			listaSustantivos.remove(values['textoIngresado'])
		elif values['textoIngresado'] in listaAdjetivos:
			listaAdjetivos.remove(values['textoIngresado'])
		else:
			listaVerbos.remove(values['textoIngresado'])

		mostrar = ', '.join(listaPalabras)
		window.FindElement('dato').Update(mostrar)
		window.FindElement('textoIngresado').Update('')
			
	if button == 'Generar sopa de letras':
		if len(listaPalabras) == 0:
			sg.Popup('¡Antes de generar la sopa de letras debe ingresar palabras!')
		elif int(values['cantS']) + int(values['cantA']) + int(values['cantV']) == 0:
			sg.Popup('¡Debes darle un valor a la cantidad de palabras que vas a elegir, sino la sopa de letras va a salir vacia!')	
		else:
			break	
    
if button == 'Salir':
	sys.exit()
else:
	# Manda el color del fondo que obtendrá la sopa de letras dependiendo del promedio de temperaturas sacado	
	promedioTemperaturas=promedio()
	if promedioTemperaturas[values['oficinas']] == 0:
		fondo = 'white'	
	elif promedioTemperaturas[values['oficinas']] < 10:
		fondo = 'blue'
	elif promedioTemperaturas[values['oficinas']] >= 10 and promedioTemperaturas[values['oficinas']] <= 20:
		fondo = 'violet'
	elif promedioTemperaturas[values['oficinas']] >= 20 and promedioTemperaturas[values['oficinas']] <= 28:	
		fondo = 'orange'
	else:
		fondo = 'red'

	listaPalabras = [listaSustantivos, listaAdjetivos, listaVerbos]

	if values['horizontal']:
		orientacion=True
	else:
		orientacion=False
			
	if values['mosPal']:
		ayuda=2
	elif values['mosDef']:
		ayuda=3
	else:
		ayuda=1	

	fuente = values['font']

	if values['mayOmin'] == 'Mayúscula':
		mayOmin = True
	else:
		mayOmin = False

	# Elección de colores, si no se elije alguno se aplica el color por defecto
	if values['Sustantivos'] == '':
		colorS = 'pink'
		sg.Popup('Como no se agrego un color específico a los SUSTANTIVOS tendrá un color por defecto: ROSA', text_color='pink')
	else:
		colorS = values['Sustantivos']  

	if values['Adjetivos'] == '':
		colorA = 'purple'
		sg.Popup('Como no se agrego un color específico a los ADJETIVOS tendrá un color por defecto: VIOLETA', text_color='purple')
	else:
		colorA = values['Adjetivos']

	if values['Verbos'] == '':
		colorV = 'green'
		sg.Popup('Como no se agrego un color específico a los VERBOS tendrá un color por defecto: VERDE', text_color='green') 
	else:
		colorV = values['Verbos']  

	colores = dict(cSus=colorS, cAdj=colorA, cVer=colorV)
	cantPal = [int(values['cantS']), int(values['cantA']), int(values['cantV'])]

	window.Close()
