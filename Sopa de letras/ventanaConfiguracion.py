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
    sustantivo, adjetivo o verbo.
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

orientacion=True
listaSustantivos = []	
listaAdjetivos = []
listaVerbos = []
lista_palabras = ([listaSustantivos, listaAdjetivos,listaVerbos],orientacion)
listaPalabrasAceptadas = []
   
   

def recibirDatos():
	'''
		Retorna los datos y la configuracion para usar en la sopa de letras
	'''
	return lista_palabras



layout = [
    [sg.Text('Sopa de Letras con PySimpleGUI', size=(32, 1), font=('Time New Roman', 14), background_color='#CDCDCD')],
    [sg.Text('● Ingrese una palabra:', text_color='darkblue',font=('Time New Roman', 12), background_color='#CDCDCD'), sg.InputText(), sg.Submit('Agregar'), sg.Submit('Quitar')],
    [sg.Multiline(key='dato', size=(70,1), font='Courier 10')],
    [sg.Text('● Nivel de dificultad:     ', text_color='darkblue', font=('Time New Roman', 11), background_color='#CDCDCD'), sg.Radio('Sin ayuda ', "RADIO1", default=True, background_color='#CDCDCD'), sg.Radio('Mostrar definiciones', "RADIO1", background_color='#CDCDCD'), sg.Radio('Mostrar palabras a buscar', "RADIO1", background_color='#CDCDCD')],
    [sg.Submit('Generar sopa de letras'), sg.Cancel('Salir')]
 ]
window = sg.Window('Seminario de Lenguajes 2019: Python', font=('Arial', 10), background_color='#CDCDCD').Layout(layout)

#g = Game()
while True:
    button, values = window.Read() 
    if button == 'Salir':
        break
    '''if button == 'Agregar':
        if values[0]== 'sustantivo':
            g.agregarSus(values[0])
        elif values[0]== 'adjetivo':
            g.agregarAdj(values[0])
        else:
            g.agregarVerbo(values[0])
        sg.Popup('se agregó la palabra: '+values[0])'''
    if button == 'Agregar':
        '''try:
            if clasificarPalabraWiktionary(values[0]) == 'NN':
                listaSustantivos.append(values[0])
            elif clasificarPalabraWiktionary(values[0]) == 'JJ':
                listaAdjetivos.append(values[0])
            elif clasificarPalabraWiktionary(values[0]) == 'VB':
                listaVerbos.append(values[0])
        except(AttributeError):
            print('No se pudo clasificar')
        # ~ sg.Popup('se agregó la palabra: '+values[0])
        palabra = mostrar_palabras_agregadas(values[0])
        window.FindElement('dato').Update(palabra)'''
        comprobarWikPattern(values[0])
        mostrar = ', '.join(listaPalabrasAceptadas)
        window.FindElement('dato').Update(mostrar)
        
    print('A',listaAdjetivos)
    print('S',listaSustantivos)
    print('V',listaVerbos)
    print(lista_palabras)
