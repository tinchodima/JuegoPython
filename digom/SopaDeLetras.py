#Gomez, Brian Agustin
#Di Maria, Juan Martin
#!/usr/bin/python3
# -*- coding: utf-8 -*-

import random
import string
import sys
import PySimpleGUI as sg
import ventanaConfiguracion as vc
from pattern.web import Wiktionary

class Digom:
    def __init__(self):
        _listaPalabras= self.recibirPalabras()
        colores= self.recibirColores()
        ori= self.recibirOrientacion()
        #tipografia= self.recibirTipografia()
        n= self.sacarMax()
        matriz= self.crearMatriz()
        self.mayOmin=False #mayOmin en true es mayuscula y false en minuscula
        self.ayuda= self._listaPalabras[2]
        self.palabrasEncontradas= [] #lista de las palabras encontradas
        self.palabraSel= [] #lista con la palabra seleccionada

    #listaPalabras= [ [listaSustantivos[], listaAdjetivos[], listaVerbos[]], True(ori), True(ayuda) ]
    #listaPalabras[0]= [listaSustantivos, listaAdjetivos, listaVerbos]
    #listaPalabras[0][1]= ["casa", "auto"]
    #listaPalabras[0][1][0]= "casa"

    def recibirPalabras(self):  
        self._listaPalabras = vc.recibirDatos() #recibe una lista de listas desde la ventana configuracion

    def recibirColores(self):
        self.colores = vc.recibirColores() #diccionario con colores de los tipos de letra   

    def recibirOrientacion(self):
        self.ori = self._listaPalabras[1]

    '''def recibirTipografia(self):
        self.tipografia = vc.recibirTipografia() '''   
    
    def sacarMax(self):
        max=0
        if len(self._listaPalabras) != 0: #max es el numero de palabras con mas letras 
            for j in range(3):
                for i in range(len(self._listaPalabras[0][j])):
                    palabra=list(self._listaPalabras[0][j][i])
                    num=len(palabra)
                    if num >= max:
                        max=num
            self.n=max+2
        else:
            self.n=0     

    #Creo una matriz de n * n con todos sus elementos siendo "*"
    def crearMatriz(self):
        self.matriz=[]
        for i in range(self.n):
            self.matriz.append([])
            for j in range(self.n):           
                self.matriz[i].append("*")

    #Llena todos los elementos (que no tienen palabras) de la matriz con letras al azar
    def llenarMatriz(self):
        for i in range(self.n):
            for j in range(self.n):
                if self.matriz[i][j] == "*": 
                    if self.mayOmin:          
                        self.matriz[i][j]=random.choice(string.ascii_uppercase)
                    else:
                        self.matriz[i][j]=random.choice(string.ascii_lowercase)

    def meterPalabrasEnMatriz(self):
        for j in range(3):
            for i in range(len(self._listaPalabras[0][j])):
                palabra=list(self._listaPalabras[0][j][i])
                if self.ori:
                    self.meterPalabraHorizontalmente(palabra, self._listaPalabras[0][j]) #Si ori es true la palabra se mete horizontal
                else:
                    self.meterPalabraVerticalmente(palabra, self._listaPalabras[0][j]) #Si ori es false la palabra se mete vertical                            

    #La palabra se ingresara verticalmente
    def meterPalabraHorizontalmente(self, palabra, listaPalabras):
        ok=False #El ok determina si la palabra fue escrita en la sopa de letras
        x=random.randrange(self.n)
        y=random.randrange(self.n)
        cont=0
        while True: #Tratará de ingresar la palabra sin que se "choque" con otra
            while True: #si la longitud de la palabra + el random "y" superan la altura de la matriz se volverá a seleccionar otro numero random hasta que la palabra entre
                lon=len(palabra)
                if lon+x >= self.n or self.matriz[x][y] != "*":
                    x=random.randrange(self.n)
                    y=random.randrange(self.n)
                else: #La palabra entra en la matriz
                    break
            auxX=x
            auxY=y        
            i=0
            for p in palabra: #se fija que todos los espacios esten disponibles para escribir la palabra ("i" tiene que ser igual a la longitud de la palabra)
                letra= self.matriz[x][y]
                if letra == "*":                 
                    x=x+1
                    i=i+1
            if lon == i: #Si todos los espacios tienen "*" entonces se procederá a escribir la palabra
                for p in palabra:
                    if self.mayOmin:                       
                        self.matriz[auxX][auxY]= str(p.upper())
                    else:
                        self.matriz[auxX][auxY]= str(p.lower())   
                    auxX+=1
                ok=True   
            if ok == True: #Si ok = True significa que la palabra fue agregada, sino tendrá que buscar nuevas coordenadas
                break 
            elif cont==5: #Si en 5 oportunidades la palabra no se pudo agregar no se agregará y se informará
                pal=''
                for element in palabra: # pal se queda con la palabra en forma de string (palabra es una lista) para poder imprimirla
                    pal=pal+element
                sg.Popup('No se pudo agregar la palabra '+pal.upper())
                listaPalabras.remove(pal)
                break
            else:
                cont+=1

    #La palabra se ingresara verticalmente
    def meterPalabraVerticalmente(self, palabra, listaPalabras):
        ok=False #El ok determina si la palabra fue escrita en la sopa de letras
        x=random.randrange(self.n)
        y=random.randrange(self.n)
        cont=0 #indica las veces que se quiere agregar la palabra a la sopa de letras
        while True: #Tratará de ingresar la palabra sin que se "choque" con otra
            while True: #si la longitud de la palabra + el random "y" superan la altura de la matriz se volverá a seleccionar otro numero random hasta que la palabra entre
                lon=len(palabra)
                if lon+y >= self.n or self.matriz[x][y] != "*":
                    x=random.randrange(self.n)
                    y=random.randrange(self.n)
                else: #La palabra entra en la matriz
                    break
            auxX=x
            auxY=y        
            i=0
            for p in palabra: #se fija que todos los espacios esten disponibles para escribir la palabra ("i" tiene que ser igual a la longitud de la palabra)
                letra=self.matriz[x][y]
                if letra == "*": #Si el lugar está disponible escribe la letra en la posicion de la matriz                   
                    y=y+1
                    i=i+1       
            if lon == i: #Si todos los espacios tienen "*" entonces se procederá a escribir la palabra
                for p in palabra:
                    if self.mayOmin:                       
                        self.matriz[auxX][auxY]= str(p.upper())
                    else:
                        self.matriz[auxX][auxY]= str(p.lower())
                    auxY+=1
                ok=True   
            if ok == True: #Si ok = True significa que la palabra fue agregada, sino tendrá que buscar nuevas coordenadas
                break 
            elif cont==5: #Si en 5 oportunidades la palabra no se pudo agregar no se agregará y se informará
                pal=''
                for element in palabra: # pal se queda con la palabra en forma de string (palabra es una lista) para poder imprimirla
                    pal=pal+element
                sg.Popup('No se pudo agregar la palabra '+pal.upper())
                listaPalabras.remove(pal)
                break
            else:
                cont+=1
       
    #--------------------------------------------------Método que crea el gráfico--------------------------------------------------#
    def graficar(self):
        totalPalabras = []
        totalPalabras = self._listaPalabras[0][0] + self._listaPalabras[0][1] + self._listaPalabras[0][2]

        BOX_SIZE = 22 #tamaño de las cajas que contiene cada letra
        layout = [
        [sg.T('DIGOM: Sopa de letras', font=(15), text_color='blue', background_color='White')],
        [sg.T('Sustantivos: '+str(len(self._listaPalabras[0][0])), text_color='blue', background_color='White'),sg.T('Adjetivos: '+str(len(self._listaPalabras[0][1])), text_color='blue', background_color='White'), sg.T('Verbos: '+str(len(self._listaPalabras[0][2])), text_color='blue', background_color='White' )],
        [sg.Graph((self.n*30, self.n*30), (-2, self.n*22.5), (self.n*22.5, -2), key='Graph', change_submits=True, drag_submits=False)],
        [sg.T('Elegir un tipo de letra', text_color='blue', background_color='White'), sg.Button('Sustantivo', button_color=('black', self.colores['cSus'])), sg.Button('Adjetivo', button_color=('black', self.colores['cAdj'])), sg.Button('Verbo', button_color=('black', self.colores['cVer'] ))],
        [sg.Button('Comprobar Palabra'), sg.Button('Salir')]
        ]        

        if self.ayuda == 2: #lista de palabras
            mostrarPalabras = [
                [sg.Listbox(values=[], key='ayudaPal', size=(self.n+4, self.n+4))],
                [sg.Button('Ayuda')]
                ]
            layout[2].append(sg.Frame('Palabras a encontrar', mostrarPalabras, font='Any 10', title_color='blue', size=(self.n*2, self.n*10)))

        elif self.ayuda == 3: #definiciones de palabras
            definicionPalabra = [
                [sg.Multiline('', key='ayudaDef')],
                [sg.Button('Ayuda')]
                ]
            layout[2].append(sg.Frame('Definicion de palabra al azar', definicionPalabra, font='Any 10', title_color='blue', size=(self.n*2, self.n*10)))

        window = sg.Window('Game', font=('Arial', 10), background_color='White').Layout(layout).Finalize()
        g = window.FindElement('Graph')

        #Dibuja la matriz en el gráfico
        for i in range(self.n):
            for j in range(self.n):            
                g.DrawText('{}'.format(self.matriz[i][j]), (i * BOX_SIZE + 12, j * BOX_SIZE + 12))

        auxColor='white' #Si no se elije un tipo de palabra no se pinta nada 
        listPosiciones=[] #posicion de la letra seleccionada de la matriz
        block=True #Si se elige un tipo de palabra ya no se podra elegir otro hasta que confirme palabra
        totalPalabrasEncontradas=0
        textoDefinicion='soy una definicion de una palabra'

        while True:
            event, values = window.Read()

            if event == 'Salir':
                window.Close()
                break
            
            #Botones de ayuda
            if event == 'Ayuda':
                if self.ayuda == 3:
                    window.FindElement('ayudaDef').Update(textoDefinicion)
                elif self.ayuda == 2:
                    window.FindElement('ayudaPal').Update(totalPalabras)

            #si apreta un tipo de palabra y quiere cambiarlo cuando ya eligio aluna palabra
            if event == 'Sustantivo' or event == 'Adjetivo' or event == 'Verbo':
                if not block:
                    sg.Popup('Primero debes comprobar la palabra antes de cambiar el tipo')    
            
            #Apreta en los botones de tipo de palabra
            if event == 'Sustantivo' and block:
                auxColor= self.colores['cSus']
                block=False
            if event == 'Adjetivo' and block:
                auxColor= self.colores['cAdj']
                block=False
            if event == 'Verbo' and block:
                auxColor= self.colores['cVer']    
                block=False

            mouse = values['Graph']
            if event == 'Graph':
                if mouse == (None, None):
                    continue
                y = mouse[0]//BOX_SIZE
                x = mouse[1]//BOX_SIZE

                #agrega la posicion marcada en una lista y la busca si ay estaba en la lista devuelve true
                posLetra= self.posLetraMatriz(listPosiciones, x, y)

                try:  
                    if auxColor != 'white':
                        self.palabraSel.append(self.matriz[y][x])
                        g.DrawRectangle((y * BOX_SIZE, x * BOX_SIZE), (y * BOX_SIZE+BOX_SIZE-2, x * BOX_SIZE+BOX_SIZE-2), line_color=auxColor) 

                        if posLetra == True: #Si está ya agregada la posicion de la letra se deseleccionará
                            try:
                                self.palabraSel.remove(self.matriz[y][x])
                                self.palabraSel.remove(self.matriz[y][x]) #Para que elimine bien tiene que estar 2 veces
                                g.DrawRectangle((y * BOX_SIZE, x * BOX_SIZE), (y * BOX_SIZE+BOX_SIZE-2, x * BOX_SIZE+BOX_SIZE-2), line_color='white')
                            except(ValueError): #Reiniciar la lista de posiciones guardadas porque no se eligió ninguna letra todavía
                                self.palabraSel=[] 

                #click fuera de la sopa de letras
                except(IndexError): 
                    print('fuera de rango')

            #Si no se elije una palabra se puede seguir cambiando entre tipos de palabras
            if len(self.palabraSel)==0: 
                block=True

            if event == 'Comprobar Palabra' and len(self.palabraSel)!=0:
                block=True
                auxX=x
                auxY=y
                pal='' 

                for element in self.palabraSel: # pal se queda con la palabra seleccionada
                    pal=pal+element

                if auxColor == self.colores['cSus']:
                    if pal.lower() in self._listaPalabras[0][0]: #Si la palabra elegida está en la lista de sustantivos se acepta
                        sg.Popup("encontraste la palabra: "+pal)
                        totalPalabrasEncontradas+=1
                    else:
                        sg.Popup("la palabra: "+pal+" no es un sustantivo")
                        listPosiciones=[]
                        if self.ori == True:
                            for x in range(len(pal)):
                                g.DrawRectangle((auxY * BOX_SIZE, auxX * BOX_SIZE), (auxY * BOX_SIZE+BOX_SIZE-2, auxX * BOX_SIZE+BOX_SIZE-2), line_color='white') 
                                auxY-=1
                        else:
                            for x in range(len(pal)):
                                g.DrawRectangle((auxY * BOX_SIZE, auxX * BOX_SIZE), (auxY * BOX_SIZE+BOX_SIZE-2, auxX * BOX_SIZE+BOX_SIZE-2), line_color='white')
                                auxX-=1                        

                elif auxColor == self.colores['cAdj']:
                    if pal.lower() in self._listaPalabras[0][1]:
                        sg.Popup("encontraste la palabra: "+pal)
                        totalPalabrasEncontradas+=1
                    else:
                        sg.Popup("la palabra: "+pal+" no es un adjetivo")
                        listPosiciones=[]
                        if self.ori == True:
                            for x in range(len(pal)):
                                g.DrawRectangle((auxY * BOX_SIZE, auxX * BOX_SIZE), (auxY * BOX_SIZE+BOX_SIZE-2, auxX * BOX_SIZE+BOX_SIZE-2), line_color='white') 
                                auxY-=1
                        else:
                            for x in range(len(pal)):
                                g.DrawRectangle((auxY * BOX_SIZE, auxX * BOX_SIZE), (auxY * BOX_SIZE+BOX_SIZE-2, auxX * BOX_SIZE+BOX_SIZE-2), line_color='white')
                                auxX-=1                        

                elif auxColor == self.colores['cVer']:
                    if pal.lower() in self._listaPalabras[0][2]:
                        sg.Popup("encontraste la palabra: "+pal)
                        totalPalabrasEncontradas+=1
                    else:
                        sg.Popup("la palabra: "+pal+" no es un verbo")
                        listPosiciones=[]
                        if self.ori == True:
                            for x in range(len(pal)):
                                g.DrawRectangle((auxY * BOX_SIZE, auxX * BOX_SIZE), (auxY * BOX_SIZE+BOX_SIZE-2, auxX * BOX_SIZE+BOX_SIZE-2), line_color='white') 
                                auxY-=1
                        else:
                            for x in range(len(pal)):
                                g.DrawRectangle((auxY * BOX_SIZE, auxX * BOX_SIZE), (auxY * BOX_SIZE+BOX_SIZE-2, auxX * BOX_SIZE+BOX_SIZE-2), line_color='white')
                                auxX-=1
                self.palabraSel=[]            

            if len(totalPalabras) == totalPalabrasEncontradas:
                sg.Popup('    Ganaste! Felicitaciones        ', title='GANASTE', font=(16))    

    #se guarda la posicion de cada letra seleccionada en la matriz y si la posicion ya estaba devuelve true y no la agrega
    def posLetraMatriz(self, listPosiciones, x, y): 
        pos=[]
        pos.append(x)
        pos.append(y)
        if pos in listPosiciones:
            listPosiciones.remove(pos)
            return True
        else:
            listPosiciones.append(pos)
        return False
#------------------------------------------------------------Seccion de Brian Gomez, aqui voy a toquetear tu programa------------------------------------------------------------#     

'''
def mostrarDefinicionAlAzar(listaPalabras):

		Devuelve una definicion al azar en base a las palabras agregadas

	posL=random.randrage(3)
	posP=random.randrage(len(listaPalabras[posL]))
	definicion = listaPalabras[posL][posP]
	return definicion
    '''

#------------------------------------------------------------Solo el programa tocare no te ilusiones-----------------------------------------------------------------------------#
