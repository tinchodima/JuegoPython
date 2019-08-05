# Gomez, Brian Agustin
# Di Maria, Juan Martin
# !/usr/bin/python3
#  -*- coding: utf-8 -*-

import sys
import random
import string
import PySimpleGUI as sg
import ventanaConfiguracion as vc

class Digom():
    def __init__(self):
        self._listaPalabras = vc.getDatos()
        self.colores = vc.getColores()
        #self.definiciones = vc.getDefiniciones()
        self.definiciones = [['def 1 sus','def 2 sus', 'def 3 sus'],['def 1 adj','def 2 adj', 'def 3 adj', 'def 4 adj'],['def 1 ver','def 2 ver']]
        self.ori = vc.getOri()
        self.ayuda = vc.getAyuda() 
        self.tipografia = vc.getFuente() 
        self.mayOmin = vc.getTipo()
        self.cantPalAgregar = vc.getCantPal()
        n = self.sacarMax()
        matriz = self.crearMatriz()       
        self.colorFondo = 'white' # LOOK AND FEEL
        self.listaPalabrasAceptadas = {'sus':[],'adj':[],'ver':[]}
        self.palabrasEncontradas = [] # Lista de las palabras encontradas
        self.palabraSel = [] # Lista con la palabra seleccionada

    #listaPalabras= [ [listaSustantivos[], listaAdjetivos[], listaVerbos[]], True(ori), True(ayuda) ]
    #listaPalabras[0]= [listaSustantivos, listaAdjetivos, listaVerbos]
    #listaPalabras[0][1]= ["casa", "auto"]
    #listaPalabras[0][1][0]= "casa"     
    
    # Saca el número maximo dependiendo de la palabra mas grande
    def sacarMax(self):
        max=0
        if len(self._listaPalabras) != 0:
            for j in range(3):
                for i in range(len(self._listaPalabras[j])):
                    palabra=list(self._listaPalabras[j][i])
                    num=len(palabra)
                    if num >= max:
                        max=num
            self.n=max+2
        else:
            self.n=0     

    # Creo una matriz de n * n con todos sus elementos siendo "*"
    def crearMatriz(self):
        self.matriz=[]
        for i in range(self.n):
            self.matriz.append([])
            for j in range(self.n):           
                self.matriz[i].append("*")

    # Llena todos los elementos (que no tienen palabras) de la matriz con letras al azar
    def llenarMatriz(self):
        for i in range(self.n):
            for j in range(self.n):
                if self.matriz[i][j] == "*": 
                    if self.mayOmin:          
                        self.matriz[i][j]=random.choice(string.ascii_uppercase)
                    else:
                        self.matriz[i][j]=random.choice(string.ascii_lowercase)

    # Agrega de las palabras ingresadas, la cantidad indicada, eligiendo al azar entre ellas
    def meterPalabrasEnMatriz(self):
        listaPalCopia=self._listaPalabras.copy()
        for i in range(3):
            while self.cantPalAgregar[i] != 0 and len(listaPalCopia[i]) != 0:
                numRandom = random.randrange(len(listaPalCopia[i]))
                palabra = listaPalCopia[i][numRandom]
                listaPalabra= list(listaPalCopia[i][numRandom])
                self.aceptarPalabra(i,palabra)
                # Si ori es true la palabra se mete horizontal
                if self.ori:
                    self.meterPalabraHorizontalmente(listaPalabra, self._listaPalabras[i]) 
                # Si ori es false la palabra se mete vertical    
                else:
                    self.meterPalabraVerticalmente(listaPalabra, self._listaPalabras[i])
            
                self.cantPalAgregar[i] = self.cantPalAgregar[i] -1
                listaPalCopia[i].pop(numRandom)

    # La palabra ingresada se agrega en un diccionario con su tipo
    def aceptarPalabra(self, i, palabra):            
        if i==0:
            self.listaPalabrasAceptadas['sus'].append(palabra)
        elif i==1:
            self.listaPalabrasAceptadas['adj'].append(palabra)  
        else:
            self.listaPalabrasAceptadas['ver'].append(palabra)        

    # La palabra se ingresara verticalmente
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

    # La palabra se ingresara verticalmente
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


    # Método que crea el gráfico
    def graficarSopaDeLetras(self):
        auxColor='white' #Si no se elije un tipo de palabra no se pinta nada 
        marcada=[] # Posicion de la letra seleccionada de la matriz (lista que se usa para deseleccionar cuando se vuelve a clickear)
        block=True # Si se elige un tipo de palabra ya no se podra elegir otro hasta que confirme palabra
        listaPosiciones=[] # Posiciones elegidas por el usuario en el gráfico
        listaPosicionesNoBorrar=[] # Posiciones que no se deben borrar debido a que el usuario encontró una palabra 
        win=False
        totalPalabras = []
        totalPalabras = set(self.listaPalabrasAceptadas['sus'] + self.listaPalabrasAceptadas['adj'] + self.listaPalabrasAceptadas['ver'])

        BOX_SIZE = 22 #tamaño de las cajas que contiene cada letra
        layout = [
        [sg.T('DIGOM: Sopa de letras', font=(self.tipografia, 15), text_color='blue', background_color=self.colorFondo)],
        [sg.T('Sustantivos: '+str(len(self.listaPalabrasAceptadas['sus']))+'  -', text_color='blue', background_color=self.colorFondo, font=(self.tipografia,10)),sg.T('Adjetivos: '+str(len(self.listaPalabrasAceptadas['adj']))+'  -', text_color='blue', background_color=self.colorFondo, font=(self.tipografia,10)), sg.T('Verbos: '+str(len(self.listaPalabrasAceptadas['ver'])), text_color='blue', background_color=self.colorFondo, font=(self.tipografia,10))],
        [sg.Graph((self.n*30, self.n*30), (-2, self.n*22.5), (self.n*22.5, -2), key='Graph', change_submits=True, drag_submits=False, background_color=self.colorFondo)],
        [sg.T('Elegir un tipo de letra', text_color='blue', background_color=self.colorFondo, font=(self.tipografia,10)), sg.Button('Sustantivo', button_color=('black', self.colores['cSus'])), sg.Button('Adjetivo', button_color=('black', self.colores['cAdj'])), sg.Button('Verbo', button_color=('black', self.colores['cVer']))],
        [sg.Button('Comprobar Palabra'), sg.Button('Salir')]
        ]
        
        self.comprobarAyuda(layout)
        window = sg.Window('Game', font=(self.tipografia, 10), background_color=self.colorFondo).Layout(layout).Finalize()
        g = window.FindElement('Graph')

        # Dibuja la matriz en el gráfico
        for i in range(self.n):
            for j in range(self.n):            
                g.DrawText('{}'.format(self.matriz[i][j], font=(self.tipografia, 15)), (i * BOX_SIZE + 12, j * BOX_SIZE + 12))
        
        while True:
            event, values = window.Read()
            if event == 'Salir':
                sys.exit()             
            
            # Botones de ayuda
            if event == 'Ayuda' and not win:
                if self.ayuda == 3:
                    window.FindElement('ayudaDef').Update('')
                    window.FindElement('ayudaDef').Update(self.mostrarDefinicionAlAzar())
                elif self.ayuda == 2:
                    window.FindElement('ayudaPal').Update(totalPalabras)

            # Si apreta un tipo de palabra y quiere cambiarlo cuando ya eligio alguna palabra
            if event == 'Sustantivo' or event == 'Adjetivo' or event == 'Verbo':
                if not block:
                    sg.Popup('Primero debes comprobar la palabra antes de cambiar el tipo')
                elif win:
                    sg.Popup('Ganaste, para salir presione "Salir"')        
            
            # Apreta en los botones de tipo de palabra
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
            if event == 'Graph' and not win:
                if mouse == (None, None):
                    continue
                y = mouse[0]//BOX_SIZE
                x = mouse[1]//BOX_SIZE

                # Agrega la posicion marcada en una lista y la busca si ya estaba en la lista devuelve "true"
                posLetra= self.posLetraMatrizMarcada(marcada, x, y)
                self.guardarPosicion(listaPosiciones, x, y)

                try:  
                    if auxColor != 'white':
                        self.palabraSel.append(self.matriz[y][x])
                        g.DrawRectangle((y * BOX_SIZE, x * BOX_SIZE), (y * BOX_SIZE+BOX_SIZE-2, x * BOX_SIZE+BOX_SIZE-2), line_color=auxColor) 

                        if posLetra == True: #Si está ya agregada la posicion de la letra se deseleccionará
                            try:
                                self.palabraSel.remove(self.matriz[y][x])
                                self.palabraSel.remove(self.matriz[y][x]) # Se tiene que remover 2 veces (sino remueve mal)
                                g.DrawRectangle((y * BOX_SIZE, x * BOX_SIZE), (y * BOX_SIZE+BOX_SIZE-2, x * BOX_SIZE+BOX_SIZE-2), line_color=self.colorFondo)
                            except(ValueError): #Reiniciar la lista de posiciones guardadas porque no se eligió ninguna letra todavía
                                self.palabraSel=[] 
                            self.eliminarPos(listaPosiciones, x, y)

                # Click fuera de la sopa de letras
                except(IndexError): 
                    print('fuera de rango')

            # Si no se elije una palabra se puede seguir cambiando entre tipos de palabras
            if len(self.palabraSel)==0: 
                block=True

            if event == 'Comprobar Palabra' and len(self.palabraSel)!=0:
                block=True
                self.comprobarPalabra(BOX_SIZE,marcada,listaPosiciones,auxColor,g,listaPosicionesNoBorrar)

            # El juegador gana cuando encontró el total de palabras a buscar con su tipo
            palabrasEncontradas=set(self.palabrasEncontradas)
            self.juegoTerminado(totalPalabras, palabrasEncontradas, win)


    # Comprueba si la palabra elegida es un sustantivo, adjetivo o verbo
    def comprobarPalabra(self,BOX_SIZE,marcada,listaPosiciones,auxColor,g,listaPosicionesNoBorrar):
        pal='' 
        # 'pal' se queda con la palabra seleccionada (por que es una lista)
        for element in self.palabraSel: 
             pal=pal+element

        # Con el color me doy cuenta del tipo de palabra que eligio
        if auxColor == self.colores['cSus']:          
            if pal.lower() in self.listaPalabrasAceptadas['sus']: # Si la palabra elegida está en la lista de sustantivos se acepta 
                sg.Popup("encontraste la palabra: "+pal)
                self.palabrasEncontradas.append(pal.lower()) # Se agrega la palabra a la lista de palabras encontradas
                for elem in listaPosiciones: # Se guardan las posiciones a no borrar
                    listaPosicionesNoBorrar.append(elem)
            else:
                sg.Popup("la palabra "+pal+" no es un sustantivo")
                self.borrarPosiciones(listaPosiciones, g, BOX_SIZE, marcada,listaPosicionesNoBorrar)
                listaPosiciones=[]                        

        elif auxColor == self.colores['cAdj']:
            if pal.lower() in self.listaPalabrasAceptadas['adj']:
                sg.Popup("encontraste la palabra: "+pal)
                self.palabrasEncontradas.append(pal.lower())
                for elem in listaPosiciones:
                    listaPosicionesNoBorrar.append(elem)
            else:
                sg.Popup("la palabra "+pal+" no es un adjetivo")
                self.borrarPosiciones(listaPosiciones, g, BOX_SIZE, marcada,listaPosicionesNoBorrar)
                listaPosiciones=[]  

        elif auxColor == self.colores['cVer']:
            if pal.lower() in self.listaPalabrasAceptadas['ver']:
                sg.Popup("encontraste la palabra: "+pal)
                self.palabrasEncontradas.append(pal.lower())
                for elem in listaPosiciones:
                    listaPosicionesNoBorrar.append(elem)
            else:
                sg.Popup("la palabra "+pal+" no es un verbo")
                self.borrarPosiciones(listaPosiciones, g, BOX_SIZE, marcada,listaPosicionesNoBorrar)
                listaPosiciones=[]  
        # La palabra seleccionada vuelve a 0
        self.palabraSel=[]       

    # Comprueba si se encontraron todas las palabras
    def juegoTerminado(self, totalPalabras, palabrasEncontradas, win):
        final= totalPalabras & palabrasEncontradas
        if len(totalPalabras) == len(final) and not win:
            sg.Popup('    Ganaste! Felicitaciones          ', title='GANASTE', font=(20))  
            win=True

    # Comprueba el tipo de ayuda seleccionado y lo agrega al gráfico
    def comprobarAyuda(self, layout):
        if self.ayuda == 2: #lista de palabras
            mostrarPalabras = [
                [sg.Listbox(values=[], key='ayudaPal', size=(self.n+4, self.n+4))],
                [sg.Button('Ayuda')]
                ]
            layout[2].append(sg.Frame('Palabras a encontrar', mostrarPalabras, font=(self.tipografia, 10), title_color='blue', size=(self.n*2, self.n*10), background_color=self.colorFondo))

        elif self.ayuda == 3: #definiciones de palabras
            definicionPalabra = [
                [sg.Multiline('', key='ayudaDef')],
                [sg.Button('Ayuda')]
                ]
            layout[2].append(sg.Frame('Definicion de palabra al azar', definicionPalabra, font=(self.tipografia, 10), title_color='blue', size=(self.n*2, self.n*10), background_color=self.colorFondo))

    # Se guarda la posicion de cada letra seleccionada en la matriz y si la posicion ya estaba devuelve true y no la agrega
    def posLetraMatrizMarcada(self, marcada, x, y): 
        pos=[]
        pos.append(x)
        pos.append(y)
        if pos in marcada:
            marcada.remove(pos)
            return True
        else:
            marcada.append(pos)
        return False

    # Guarda las posiciones que se marcan en la sopa de letras
    def guardarPosicion(self, listaPosiciones, x, y):  
        pos=[]
        pos.append(x)
        pos.append(y)
        listaPosiciones.append(pos)

    # Elimina una posicion de la lista de posiciones
    def eliminarPos(self, listaPosiciones, x, y):
        pos=[x,y]
        listaPosiciones.remove(pos)    

    # Borra todas las posiciones del gráfico cuando se selecciona una palabra y no es correcta
    def borrarPosiciones(self, listaPosiciones, g, BOX_SIZE, marcada, listaPosicionesNoBorrar):
        for i in range(len(listaPosicionesNoBorrar)):
            if listaPosicionesNoBorrar[i] in listaPosiciones:
                listaPosiciones.remove(listaPosicionesNoBorrar[i])

        for i in range(len(listaPosiciones)):
            posLetra=self.posLetraMatrizMarcada(marcada, listaPosiciones[i][0], listaPosiciones[i][1])
            if posLetra == True:
                try:
                    self.palabraSel.remove(self.matriz[listaPosiciones[i][1]][listaPosiciones[i][0]])
                except(ValueError):
                    self.palabraSel=[]    
                g.DrawRectangle((listaPosiciones[i][1] * BOX_SIZE, listaPosiciones[i][0] * BOX_SIZE), (listaPosiciones[i][1] * BOX_SIZE+BOX_SIZE-2, listaPosiciones[i][0] * BOX_SIZE+BOX_SIZE-2), line_color=self.colorFondo)

    # Devuelve una definicion al azar de las palabras ingresadas
    def mostrarDefinicionAlAzar(self):
        pos1=random.randrange(3)
        pos2=random.randrange(len(self.definiciones[pos1]))
        definicion = self.definiciones[pos1][pos2]
        return definicion
