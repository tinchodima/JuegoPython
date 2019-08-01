# Gomez, Brian Agustin
# Di Maria, Juan Martin
# !/usr/bin/python3
#  -*- coding: utf-8 -*-

import sys
import PySimpleGUI as sg
from pattern.web import Wiktionary
from pattern.es import parse,split
import SopaDeLetras as sdl

class Configuracion:
    layout = [
            [sg.Text('DIGOM: SOPA DE LETRAS', size=(32, 1), font=('Time New Roman', 14), background_color='#80cbc4')],
            [sg.Text('● Configurar cantidad de palabras a ingresar', text_color='black',font=('Time New Roman', 12), background_color='#80cbc4')],
            [sg.Text('Sustantivos', text_color='black',font=('Time New Roman', 11), background_color='#80cbc4'),sg.Spin([i for i in range(0,11)], initial_value=0, size=(2,2), key=('cantS')),sg.Text('Adjetivos', text_color='black',font=('Time New Roman', 11), background_color='#80cbc4'),sg.Spin([i for i in range(0,11)], initial_value=0, size=(2,2), key=('cantA')),sg.Text('Verbos', text_color='black',font=('Time New Roman', 11), background_color='#80cbc4'),sg.Spin([i for i in range(0,11)], initial_value=0, size=(2,2), key=('cantV'))],
            [sg.Text('● Ingrese una palabra:', text_color='black',font=('Time New Roman', 12), background_color='#80cbc4'), sg.InputText(key='textoIngresado'), sg.Submit('Agregar'), sg.Submit('Quitar')],
            [sg.Multiline(key='dato', size=(70,1), font='Arial', text_color='blue')],
            [sg.Text('● Nivel de dificultad:     ', text_color='black', font=('Time New Roman', 11),background_color='#80cbc4'), sg.Radio('Sin ayuda ', "RADIO1", default=True, background_color='#80cbc4', key='sinAyuda'), sg.Radio('Mostrar definiciones', "RADIO1", background_color='#80cbc4', key='mosDef'), sg.Radio('Mostrar palabras a buscar', "RADIO1", background_color='#80cbc4', key='mosPal')],
            [sg.Text('● Orientación de las palabras:     ', text_color='black', font=('Time New Roman', 10), background_color='#80cbc4'), sg.Radio('Horizontal', "RADIO2", default=True, background_color='#80cbc4', key='horizontal'), sg.Radio('Vertical', "RADIO2", background_color='#80cbc4', key='vertical')],
            [sg.Text('● Elegir colores',text_color='black', font=('Time New Roman', 10), background_color='#80cbc4'), sg.ColorChooserButton('Sustantivos',button_color=('#FFFFFF','#03A9F4')), sg.ColorChooserButton('Adjetivos',button_color=('#FFFFFF','#03A9F4')), sg.ColorChooserButton('Verbos',button_color=('#FFFFFF','#03A9F4'))],
            [sg.Submit('Generar sopa de letras'), sg.Cancel('Salir')]
        ]
    window = sg.Window('Seminario de Lenguajes 2019: Python', font=('Arial', 10), background_color='#80cbc4').Layout(layout)
    button = window.Read ()
    values = window.Read()

    def __init__(self):
        self.__listaSustantivos = []
        self.__listaAdjetivos = []
        self.__listaVerbos = []
        self.__listaPalabrasAceptadas = []
        self.__listaPalabras = ()
        self.__listaAyuda = ()
        self.__colores = ()
        self.__definiciones = {}
        self.__palabra = values['textoIngresado']

    def clasificarPalabraWiktionary(self):
        w = Wiktionary(language="es")
        a = w.search(self.__palabra)
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

    def clasificarPalabraPattern(self):
        '''
        clasifica el string recibido como paramentro en pattern, analizando la palabra, devuleve su clasificacion
        (sustantivo, adjetivo o verbo).
        '''
        s = parse(self.__palabra).split()
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

    def comprobarWikPattern(self):
        if self.clasificarPalabraPattern() == self.clasificarPalabraWiktionary() and self.clasificarPalabraPattern() != 'No se pudo clasificar':
            self.clasificacionWiktionary()
            self.__definiciones[self.__palabra] = self.obtenerDefinicion()
            print('wik1')
        elif self.clasificarPalabraWiktionary() == 'No se pudo clasificar' and self.clasificarPalabraPattern() == 'No se pudo clasificar':
            #informar en un reporte que la clasificacion no existe ni en wik ni en pattern
            msg = 'Clasificacion no encontrada en Wiktionary y Pattern'
            self.reporteClasificaciones(msg)
            print('ninguno')
        elif self.clasificarPalabraWiktionary() != self.clasificarPalabraPattern() and self.clasificarPalabraWiktionary() != 'No se pudo clasificar':
            self.clasificacionPattern()
            print('pattern1')
            sg.Popup('La clasificacion no se encuentra en Wiktionary, ingresar una definicion manualmente')
            text = sg.PopupGetText(self.__palabra, 'Ingrese una definicion')
            self.__definiciones[self.__palabra] = text
            #pedir que ingrese una definicion
        elif self.clasificarPalabraWiktionary() != self.clasificarPalabraPattern() and self.clasificarPalabraWiktionary() != 'No se pudo clasificar' and self.clasificarPalabraPattern() != 'No se pudo clasificar':
            self.clasificacionPattern()
            print('pattern2')
            sg.Popup('La clasificacion no se encuentra en Wiktionary, ingresar una definicion manualmente')
            text = sg.PopupGetText(self.__palabra, 'Ingrese una definicion')
            self.__definiciones[self.__palabra] = text
            #pedir que ingrese una definicion
        elif self.clasificarPalabraPattern() != self.clasificarPalabraWiktionary() and self.clasificarPalabraPattern() != 'No se pudo clasificar':
            #informar en un reporte que la clasificacion no existe en pattern
            self.clasificacionWiktionary()
            self.__definiciones[self.__palabra] = self.obtenerDefinicion()
            msg = 'Clasificacion no encontrada en Pattern'
            self.reporteClasificaciones(msg)
            print('wik2')
        elif self.clasificarPalabraPattern() != self.clasificarPalabraWiktionary() and self.clasificarPalabraPattern() != 'No se pudo clasificar' and self.clasificarPalabraWiktionary() != 'No se pudo clasificar':
            #informar en un reporte que la clasificacion no existe en pattern
            self.clasificacionWiktionary()
            self.__definiciones[self.__palabra] = self.obtenerDefinicion()
            msg = 'Clasificacion no encontrada en Pattern'
            self.reporteClasificaciones(msg)
            print('wik3')

    def clasificacionWiktionary(self):
        try:
            if self.comprobarQueLaPalabraNoEsteAgregada() == False:
                sg.Popup('La palabra ya esta agregada en la sopa de letras')
            else:
                if self.clasificarPalabraWiktionary() == 'NN':
                    if str(len(self.__listaSustantivos)) < values['cantS']:
                        self.__listaSustantivos.append(self.__palabra)
                        self.__listaPalabrasAceptadas.append(self.__palabra)
                    else:
                        sg.Popup('El limite de Sustantivos se alcanzo')
                elif self.clasificarPalabraWiktionary() == 'JJ':
                    if str(len(self.__listaSustantivos)) < values['cantA']:
                        self.__listaPalabrasAceptadas.append(self.__palabra)
                        self.__listaSustantivos.append(self.__palabra)
                    else:
                        sg.Popup('El limite de Adjetivos se alcanzo')
                elif self.clasificarPalabraWiktionary() == 'VB':
                    if str(len(self.listaSustantivos)) < values['cantV']:
                        self.__listaSustantivos.append(self.__palabra)
                        self.__listaPalabrasAceptadas.append(self.__palabra)
                    else:
                        sg.Popup('El limite de Verbos se alcanzo')
                else:
                    print('No se pudo agregar')
        except(AttributeError):
            print('No se pudo agregar')


    def clasificacionPattern(self):
        try:
            if self.comprobarQueLaPalabraNoEsteAgregada() == False:
                sg.Popup('La palabra ya esta agregada en la sopa de letras')
            else:
                if self.clasificarPalabraPattern() == 'NN':
                    self.__listaSustantivos.append(self.__palabra)
                    self.__listaPalabrasAceptadas.append()
                elif self.clasificarPalabraPattern() == 'JJ':
                    self.__listaAdjetivos.append(self.__palabra)
                    self.__listaPalabrasAceptadas.append(self.__palabra)
                elif self.clasificarPalabraPattern() == 'VB':
                    self.__listaVerbos.append(self.__palabra)
                    self.__listaPalabrasAceptadas.append(self.__palabra)
                else:
                    print('No se pudo agregar')
                
        except(AttributeError):
            print('No se pudo agregar')

    def comprobarQueLaPalabraNoEsteAgregada(self):
        if self.__palabra in self.__listaPalabras:
            return False
        else:
            return True

    def reporteClasificaciones(self, error):
        f = open('reporte.txt', 'a')
        f.write(error + '\n')
        f.close

    def obtenerDefinicion(self):
        # ~ w = Wiktionary(language="es")
        # ~ a = w.search(palabra)
        # ~ definicion = a.sections[3].content.split('1')[1].split('.2')[0].split('*')[0]
        # ~ return definicion
        w = Wiktionary(language="es")
        a = w.search(self.__palabra)
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

    def recibirDatos(self):
        '''
            Retorna los datos y la configuracion para usar en la sopa de letras
        '''
        return self.__listaPalabras

    def recibirColores(self):
        '''
            Retorna los colores de los tipos de palabras
        '''	
        return self.__colores

    def recibirTipoDeAyuda(self):
        '''
            1: Sin ayuda
            2: Mostrar definiciones
            3: Mostrar palabras a buscar
            Devuelve en una tupla el tipo de ayuda seleccionado
        '''
        
        return False

    def recibirDefiniciones(self):
        '''
            Devuelve un diccionario con la palabra como clave y la definicion como valor
        '''
        return definiciones

    def graficarConfiguracion(self):
        layout = [
            [sg.Text('DIGOM: SOPA DE LETRAS', size=(32, 1), font=('Time New Roman', 14), background_color='#80cbc4')],
            [sg.Text('● Configurar cantidad de palabras a ingresar', text_color='black',font=('Time New Roman', 12), background_color='#80cbc4')],
            [sg.Text('Cantidad de Sustantivos', text_color='black',font=('Time New Roman', 12), background_color='#80cbc4'),sg.Spin([i for i in range(0,11)], initial_value=0, size=(2,2), key=('cantS')),sg.Text('Cantidad de Adjetivos', text_color='black',font=('Time New Roman', 12), background_color='#80cbc4'),sg.Spin([i for i in range(0,11)], initial_value=0, size=(2,2), key=('cantA')),sg.Text('Cantidad de Verbos', text_color='black',font=('Time New Roman', 12), background_color='#80cbc4'),sg.Spin([i for i in range(0,11)], initial_value=0, size=(2,2), key=('cantV'))],
            [sg.Text('● Ingrese una palabra:', text_color='black',font=('Time New Roman', 12), background_color='#80cbc4'), sg.InputText(key='textoIngresado'), sg.Submit('Agregar'), sg.Submit('Quitar')],
            [sg.Multiline(key='dato', size=(70,1), font='Arial', text_color='blue')],
            [sg.Text('● Nivel de dificultad:     ', text_color='black', font=('Time New Roman', 11),background_color='#80cbc4'), sg.Radio('Sin ayuda ', "RADIO1", default=True, background_color='#80cbc4', key='sinAyuda'), sg.Radio('Mostrar definiciones', "RADIO1", background_color='#80cbc4', key='mosDef'), sg.Radio('Mostrar palabras a buscar', "RADIO1", background_color='#80cbc4', key='mosPal')],
            [sg.Text('● Orientación de las palabras:     ', text_color='black', font=('Time New Roman', 10), background_color='#80cbc4'), sg.Radio('Horizontal', "RADIO2", default=True, background_color='#80cbc4', key='horizontal'), sg.Radio('Vertical', "RADIO2", background_color='#80cbc4', key='vertical')],
            [sg.Text('● Elegir colores',text_color='black', font=('Time New Roman', 10), background_color='#80cbc4'), sg.ColorChooserButton('Sustantivos',button_color=('#FFFFFF','#03A9F4')), sg.ColorChooserButton('Adjetivos',button_color=('#FFFFFF','#03A9F4')), sg.ColorChooserButton('Verbos',button_color=('#FFFFFF','#03A9F4'))],
            [sg.Submit('Generar sopa de letras'), sg.Cancel('Salir')]
        ]
        window = sg.Window('Seminario de Lenguajes 2019: Python', font=('Arial', 10), background_color='#80cbc4').Layout(layout)

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
                    
                    self.comprobarWikPattern(values['textoIngresado'],self.__listaPalabrasAceptadas,values)
                    mostrar = ', '.join(self.__listaPalabrasAceptadas)
                    window.FindElement('dato').Update(mostrar)
                    window.FindElement('textoIngresado').Update('')
                
                if button == 'Quitar':
                    self.__listaPalabrasAceptadas.remove(values[0])
                    self.__listaSustantivos.remove(values[0])
                    
                if button == 'Generar sopa de letras':
                    if len(self.__listaPalabrasAceptadas) == 0:
                        sg.Popup('¡Antes de agregar debe ingresar palabras!')
                    break
                
                print('Adjetivos: ', self.__listaAdjetivos)
                print('Sustantivos: ', self.__listaSustantivos)
                print('Verbos: ', self.__listaVerbos)

            if button != 'Salir':
                self.__listaPalabras = ([self.__listaSustantivos, self.__listaAdjetivos, self.__listaVerbos], orientacion, ayuda)
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

                self.__colores = dict(cSus=colorS, cAdj=colorA, cVer=colorV)
                
            else:
                self.__listaPalabras=()
                self.__colores={}


pruebaConf = Configuracion()
pruebaConf.graficarConfiguracion()