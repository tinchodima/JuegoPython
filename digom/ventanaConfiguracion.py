#Gomez, Brian Agustin
#Di Maria, Juan Martin

import sys
import PySimpleGUI as sg
from pattern.web import Wiktionary
from pattern.es import parse,split
import SopaDeLetras as sdl

#sg.ChangeLookAndFeel('BluePurple')

def clasificarPalabraWiktionary(palabra):		
    w = Wiktionary(language="es")
    a = w.search(palabra)
	
    try:	
        clasificacion = a.sections[3].content.split()[0]

        if clasificacion.lower() == "sustantivo":
            return 'NN'
        elif clasificacion.lower() == "adjetivo":
            return 'JJ'
        elif clasificacion.lower() == "verbo":
            return 'VB'
        else:
            return 'No se pudo clasificar'
    except(AttributeError):
        return 'No se pudo clasificar'

def clasificarPalabraPattern(palabra):
    '''
    clasifica el string recibido como paramentro en pattern, analizando la palabra, devuleve su clasificacion
    (sustantivo, adjetivo o verbo).
    '''
    s = parse(palabra).split()
    try:
        for cada in s:
            for i in cada:
                if i[1] == 'VB':
                    return 'VB'
                elif i[1] == 'NN':
                    return 'NN'
                elif i[1] == 'JJ':
                    return 'JJ'
                else:
                    return 'No se pudo clasificar'
    except(AttributeError):
        return 'No se pudo clasificar'

def comprobarWikPattern(palabra,listaPalabras):
	if clasificarPalabraPattern(palabra) == clasificarPalabraWiktionary(palabra) and clasificarPalabraPattern(palabra) != 'No se pudo clasificar':
		clasificacionWiktionary(palabra,listaPalabras)
		definiciones[palabra] = obtenerDefinicion(palabra)
		print('wik1')
	elif clasificarPalabraWiktionary(palabra) == 'No se pudo clasificar' and clasificarPalabraPattern(palabra) == 'No se pudo clasificar':
		#informar en un reporte que la clasificacion no existe ni en wik ni en pattern
		msg = 'Clasificacion no encontrada en Wiktionary y Pattern'
		reporteClasificaciones(msg)
		print('ninguno')
	elif clasificarPalabraWiktionary(palabra) != clasificarPalabraPattern(palabra) and clasificarPalabraWiktionary(palabra) != 'No se pudo clasificar':
		clasificacionPattern(palabra,listaPalabras)
		print('pattern1')
		sg.Popup('La clasificacion no se encuentra en Wiktionary, ingresar una definicion manualmente')
		text = sg.PopupGetText(palabra, 'Ingrese una definicion')
		definiciones[palabra] = text
		#pedir que ingrese una definicion
	elif clasificarPalabraWiktionary(palabra) != clasificarPalabraPattern(palabra) and clasificarPalabraWiktionary(palabra) != 'No se pudo clasificar' and clasificarPalabraPattern(palabra) != 'No se pudo clasificar':
		clasificacionPattern(palabra,listaPalabras)
		print('pattern2')
		sg.Popup('La clasificacion no se encuentra en Wiktionary, ingresar una definicion manualmente')
		text = sg.PopupGetText(palabra, 'Ingrese una definicion')
		definiciones[palabra] = text
		#pedir que ingrese una definicion
	elif clasificarPalabraPattern(palabra) != clasificarPalabraWiktionary(palabra) and clasificarPalabraPattern(palabra) != 'No se pudo clasificar':
		#informar en un reporte que la clasificacion no existe en pattern
		clasificacionWiktionary(palabra,listaPalabras)
		definiciones[palabra] = obtenerDefinicion(palabra)
		msg = 'Clasificacion no encontrada en Pattern'
		reporteClasificaciones(msg)
		print('wik2')
	elif clasificarPalabraPattern(palabra) != clasificarPalabraWiktionary(palabra) and clasificarPalabraPattern(palabra) != 'No se pudo clasificar' and clasificarPalabraWiktionary(palabra) != 'No se pudo clasificar':
		#informar en un reporte que la clasificacion no existe en pattern
		clasificacionWiktionary(palabra,listaPalabras)
		definiciones[palabra] = obtenerDefinicion(palabra)
		msg = 'Clasificacion no encontrada en Pattern'
		reporteClasificaciones(msg)
		print('wik3')

def clasificacionWiktionary(p,listaPalabras):
    try:
        if comprobarQueLaPalabraNoEsteAgregada(p,listaPalabras) == False:
            sg.Popup('La palabra ya esta agregada en la sopa de letras')
        else:
            if clasificarPalabraWiktionary(p) == 'NN':
                listaSustantivos.append(p)
                listaPalabrasAceptadas.append(p)
            elif clasificarPalabraWiktionary(p) == 'JJ':
                listaAdjetivos.append(p)
                listaPalabrasAceptadas.append(p)
            elif clasificarPalabraWiktionary(p) == 'VB':
                listaVerbos.append(p)
                listaPalabrasAceptadas.append(p)
            else:
                print('No se pudo agregar')
            
    except(AttributeError):
        print('No se pudo agregar')

def clasificacionPattern(p,listaPalabras):
	try:
		if comprobarQueLaPalabraNoEsteAgregada(p,listaPalabras) == False:
			sg.Popup('La palabra ya esta agregada en la sopa de letras')
		else:
		    if clasificarPalabraPattern(p) == 'NN':
			    listaSustantivos.append(p)
			    listaPalabrasAceptadas.append(p)
		    elif clasificarPalabraPattern(p) == 'JJ':
			    listaAdjetivos.append(p)
			    listaPalabrasAceptadas.append(p)
		    elif clasificarPalabraPattern(p) == 'VB':
			    listaVerbos.append(p)
			    listaPalabrasAceptadas.append(p)
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
	definicion = a.sections[3].content.split('1')[1].split('.2')[0].split('*')[0]
	return definicion

def recibirDatos():
	'''
		Retorna los datos y la configuracion para usar en la sopa de letras
	'''
	return listaPalabras

def recibirColores():
	'''
		Retorna los colores de los tipos de palabras
	'''	
	return colores

def recibirTipoDeAyuda():
	'''
		1: Sin ayuda
		2: Mostrar definiciones
		3: Mostrar palabras a buscar
		Devuelve en una tupla el tipo de ayuda seleccionado
	'''
	
	return False
	

def recibirDefiniciones():
	'''
		Devuelve un diccionario con la palabra como clave y la definicion como valor
	'''
	return definiciones


	
layout = [
	[sg.Text('DIGOM: SOPA DE LETRAS', size=(32, 1), font=('Time New Roman', 14), background_color='#80cbc4')],
	[sg.Text('● Ingrese una palabra:', text_color='black',font=('Time New Roman', 12), background_color='#80cbc4'), sg.InputText(), sg.Submit('Agregar'), sg.Submit('Quitar')],
	[sg.Multiline(key='dato', size=(70,1), font='Arial')],
	[sg.Text('● Nivel de dificultad:     ', text_color='black', font=('Time New Roman', 11),background_color='#80cbc4'), sg.Radio('Sin ayuda ', "RADIO1", default=True, background_color='#80cbc4', key='sinAyuda'), sg.Radio('Mostrar definiciones', "RADIO1", background_color='#80cbc4', key='mosDef'), sg.Radio('Mostrar palabras a buscar', "RADIO1", background_color='#80cbc4', key='mosPal')],
	[sg.Text('● Orientación de las palabras:     ', text_color='black', font=('Time New Roman', 10), background_color='#80cbc4'), sg.Radio('Horizontal', "RADIO2", default=True, background_color='#80cbc4', key='horizontal'), sg.Radio('Vertical', "RADIO2", background_color='#80cbc4', key='vertical')],
	[sg.Text('● Elegir colores',text_color='black', font=('Time New Roman', 10), background_color='#80cbc4'), sg.ColorChooserButton('Sustantivos',button_color=('#FFFFFF','#03A9F4')), sg.ColorChooserButton('Adjetivos',button_color=('#FFFFFF','#03A9F4')), sg.ColorChooserButton('Verbos',button_color=('#FFFFFF','#03A9F4'))],
	[sg.Submit('Generar sopa de letras'), sg.Cancel('Salir')]
]
window = sg.Window('Seminario de Lenguajes 2019: Python', font=('Arial', 10), background_color='#80cbc4').Layout(layout)

listaSustantivos = []	
listaAdjetivos = []
listaVerbos = []
listaPalabrasAceptadas = []
listaPalabras = ()
listaAyuda= ()
colores = ()
definiciones= {}

ayuda=1
while True:
	button, values = window.Read()

	if button == 'Salir':
		break
	else:
		if values['horizontal']:
			orientacion=True
		else:
			orientacion=False
			
		if values['mosPal']:
			ayuda=2
		elif values['mosDef']:
			ayuda=3

		if button == 'Agregar':
			comprobarWikPattern(values[0],listaPalabrasAceptadas)
			mostrar = ', '.join(listaPalabrasAceptadas)
			window.FindElement('dato').Update(mostrar)
		
		if button == 'Quitar':
			listaPalabrasAceptadas.remove(values[0])
			listaSustantivos.remove(values[0])
			
		if button == 'Generar sopa de letras':
			break
        
		print('Adjetivos: ', listaAdjetivos)
		print('Sustantivos: ', listaSustantivos)
		print('Verbos: ', listaVerbos)

if button != 'Salir':
	listaPalabras = ([listaSustantivos, listaAdjetivos, listaVerbos], orientacion, ayuda)

	#   Elección de colores, si no se elije alguno se aplica el color por defecto
	if (values['Sustantivos']==''):
		colorS='yellow'
		#sg.Popup('Como no se agrego un color especifico a los SUSTANTIVOS tendrán su color por defecto: amarillo')
	else:
		colorS= values['Sustantivos']  

	if (values['Adjetivos']==''):
		colorA= 'red'
		#sg.Popup('Como no se agrego un color especifico a los ADJETIVOS tendrán su color por defecto: rojo')
	else:
		colorA= values['Adjetivos']

	if (values['Verbos']==''):
		colorV='green'
		#sg.Popup('Como no se agrego un color especifico a los VERBOS tendrán su color por defecto: verde') 
	else:
		colorV= values['Verbos']  

	colores = dict(cSus=colorS, cAdj=colorA, cVer=colorV)
    
else:
	listaPalabras=()
	colores={}
