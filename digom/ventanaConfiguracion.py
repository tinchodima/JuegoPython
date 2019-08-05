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
        elif clasificacion.lower() == "adjetivo" or "forma adjetiva":
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

def comprobarWikPattern(palabra,listaPalabras,values):
	if clasificarPalabraPattern(palabra) == clasificarPalabraWiktionary(palabra) and clasificarPalabraPattern(palabra) != 'No se pudo clasificar':
		clasificacionWiktionary(palabra,listaPalabras,values)
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
		clasificacionWiktionary(palabra,listaPalabras,values)
		definiciones[palabra] = obtenerDefinicion(palabra)
		msg = 'Clasificacion no encontrada en Pattern'
		reporteClasificaciones(msg)
		print('wik2')
	elif clasificarPalabraPattern(palabra) != clasificarPalabraWiktionary(palabra) and clasificarPalabraPattern(palabra) != 'No se pudo clasificar' and clasificarPalabraWiktionary(palabra) != 'No se pudo clasificar':
		#informar en un reporte que la clasificacion no existe en pattern
		clasificacionWiktionary(palabra,listaPalabras,values)
		definiciones[palabra] = obtenerDefinicion(palabra)
		msg = 'Clasificacion no encontrada en Pattern'
		reporteClasificaciones(msg)
		print('wik3')

def clasificacionWiktionary(p,listaPalabras,values):
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
                listaVerbos.append(p)
                listaPalabras.append(p)
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
	# ~ w = Wiktionary(language="es")
	# ~ a = w.search(palabra)
	# ~ definicion = a.sections[3].content.split('1')[1].split('.2')[0].split('*')[0]
	# ~ return definicion
	w = Wiktionary(language="es")
	a = w.search(palabra)
	#definicion = a.sections[3].content.split('1')[1].split('.2')[0].split('*')[0]
	try:
		definicion = a.sections[3].content.split('1')[1].split('.2')[0].split('*')[0]
	except(IndexError):
		# ~ a.sections[3].content.split('1')[0].split('\n')[2] == ' ' or
		try:
			definicion = a.sections[3].content.split('1')[0].split('*')[1]
			if ' ' in definicion[1]:
				try:
					definicion = a.sections[3].content.split('1')[0].split('*')[2]
				except(IndexError):
					definicion = a.sections[3].content.split('1')[0].split('*')[3]
		except(IndexError):
				definicion = a.sections[3].content.split('1')[0].split('*')[2]
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
		comprobarWikPattern(values['textoIngresado'], listaPalabras,values)
		mostrar = ', '.join(listaPalabras)
		window.FindElement('dato').Update(mostrar)
		window.FindElement('textoIngresado').Update('')
		
	if button == 'Quitar':
		listaPalabras.remove(values[0])
			
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
		colorS = 'orange'
		sg.Popup('Como no se agrego un color específico a los SUSTANTIVOS tendrá un color por defecto: NARANJA', text_color='orange')
	else:
		colorS = values['Sustantivos']  

	if values['Adjetivos'] == '':
		colorA = 'red'
		sg.Popup('Como no se agrego un color específico a los ADJETIVOS tendrá un color por defecto: ROJO', text_color='red')
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
