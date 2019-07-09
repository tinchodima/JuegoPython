#Gomez, Brian Agustin
#Di Maria, Juan Martin

import sys
import PySimpleGUI as sg
from pattern.web import Wiktionary
from pattern.es import parse,split
import SopaDeLetras as sdl

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

def comprobarWikPattern(palabra):
	if clasificarPalabraPattern(palabra) == clasificarPalabraWiktionary(palabra) and clasificarPalabraPattern(palabra) != 'No se pudo clasificar':
		clasificacionWiktionary(palabra)
		print('wik1')
	elif clasificarPalabraWiktionary(palabra) == 'No se pudo clasificar' and clasificarPalabraPattern(palabra) == 'No se pudo clasificar':
		#informar en un reporte que la clasificacion no existe ni en wik ni en pattern
		msg = 'Clasificacion no encontrada en Wiktionary y Pattern'
		reporteClasificaciones(msg)
		print('ninguno')
	elif clasificarPalabraWiktionary(palabra) != clasificarPalabraPattern(palabra) and clasificarPalabraWiktionary(palabra) != 'No se pudo clasificar':
		clasificacionPattern(palabra)
		print('pattern1')
		#pedir que ingrese una definicion
	elif clasificarPalabraWiktionary(palabra) != clasificarPalabraPattern(palabra) and clasificarPalabraWiktionary(palabra) != 'No se pudo clasificar' and clasificarPalabraPattern(palabra) != 'No se pudo clasificar':
		clasificacionPattern(palabra)
		print('pattern2')
		#pedir que ingrese una definicion
	elif clasificarPalabraPattern(palabra) != clasificarPalabraWiktionary(palabra) and clasificarPalabraPattern(palabra) != 'No se pudo clasificar':
		#informar en un reporte que la clasificacion no existe en pattern
		clasificacionWiktionary(palabra)
		msg = 'Clasificacion no encontrada en Pattern'
		reporteClasificaciones(msg)
		print('wik2')
	elif clasificarPalabraPattern(palabra) != clasificarPalabraWiktionary(palabra) and clasificarPalabraPattern(palabra) != 'No se pudo clasificar' and clasificarPalabraWiktionary(palabra) != 'No se pudo clasificar':
		#informar en un reporte que la clasificacion no existe en pattern
		clasificacionWiktionary(palabra)
		msg = 'Clasificacion no encontrada en Pattern'
		reporteClasificaciones(msg)
		print('wik3')

def clasificacionWiktionary(p):
    try:
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

def clasificacionPattern(p):
	try:
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

def reporteClasificaciones(error):
	f = open('reporte.txt', 'a')
	f.write(error + '\n')
	f.close

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
	



layout = [
    [sg.Text('Sopa de Letras con PySimpleGUI', size=(32, 1), font=('Time New Roman', 14), background_color='#CDCDCD')],
    [sg.Text('● Ingrese una palabra:', text_color='darkblue',font=('Time New Roman', 12), background_color='#CDCDCD'), sg.InputText(), sg.Submit('Agregar'), sg.Submit('Quitar')],
    [sg.Multiline(key='dato', size=(70,1), font='Arial')],
    [sg.Text('● Nivel de dificultad:     ', text_color='darkblue', font=('Time New Roman', 11), background_color='#CDCDCD'), sg.Radio('Sin ayuda ', "RADIO1", default=True, background_color='#CDCDCD'), sg.Radio('Mostrar definiciones', "RADIO1", background_color='#CDCDCD'), sg.Radio('Mostrar palabras a buscar', "RADIO1", background_color='#CDCDCD')],
    [sg.Text('● Orientación:     ', text_color='darkblue', font=('Time New Roman', 10), background_color='#CDCDCD'), sg.Radio('Horizontalmente', "RADIO2", default=True, background_color='#CDCDCD'), sg.Radio('Verticalmente', "RADIO2", background_color='#CDCDCD')],
    [sg.Submit('Generar sopa de letras'), sg.Cancel('Salir')]
]
window = sg.Window('Seminario de Lenguajes 2019: Python', font=('Arial', 10), background_color='#CDCDCD').Layout(layout)

listaSustantivos = []	
listaAdjetivos = []
listaVerbos = []
listaPalabrasAceptadas = []
listaPalabras = ()
listaAyuda= ()





#----------------------------------------------------------------------------------------------------------------------------------#

#BRIAN CAMBIA QUE CUANDO LA PALABRA SEA IGUAL (LA QUE INGRESA) QUE NO LA AGREGUE A LA LISTA

#----------------------------------------------------------------------------------------------------------------------------------#






while True:
    button, values = window.Read()
    
    if button == 'Salir':
        break
    else:    
        listaAyuda= (values[1],values[2],values[3])
        orientacion=values[4]
        if(values[1]):
            ayuda=False
        else:
            ayuda=True 

        if button == 'Agregar':
            comprobarWikPattern(values[0])
            mostrar = ', '.join(listaPalabrasAceptadas)
            window.FindElement('dato').Update(mostrar)

        if button == 'Generar sopa de letras':
            break
        
        print('Adjetivos: ', listaAdjetivos)
        print('Sustantivos: ', listaSustantivos)
        print('Verbos: ', listaVerbos)
        print(listaAyuda)

if button != 'Salir':
    listaPalabras = ([listaSustantivos, listaAdjetivos, listaVerbos], orientacion, ayuda)
    colores = dict(cSus= 'yellow', cAdj='red', cVer= 'green')
else:
    listaPalabras=()
    colores={}    
