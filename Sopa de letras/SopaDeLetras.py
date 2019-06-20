#!/usr/bin/python3
#-*- coding: utf-8 -*-

import random
import string
import sys
import PySimpleGUI as sg
import ventanaConfiguracion as vc

#Creo una matriz de n * n con todos sus elementos siendo "*"
def crearMatriz(n):
    matriz = []
    for i in range(n):
        matriz.append([])
        for j in range(n):           
            matriz[i].append("*")
    return matriz

#Llena todos los elementos (que no tienen palabras) de la matriz con letras al azar
def llenarMatriz(matriz,n):
    for i in range(n):
        matriz.append([])
        for j in range(n):
            if matriz[i][j] == "*":           
                matriz[i][j]=random.choice(string.ascii_uppercase)
    return matriz

#La palabra se ingresara verticalmente
def meterPalabraHorizontalmente(palabra,matriz,n,listaPalabras):
    ok=False #El ok determina si la palabra fue escrita en la sopa de letras
    x=random.randrange(n)
    y=random.randrange(n)
    cont=0
    while True: #Tratará de ingresar la palabra sin que se "choque" con otra
        while True: #si la longitud de la palabra + el random "y" superan la altura de la matriz se volverá a seleccionar otro numero random hasta que la palabra entre
            lon=len(palabra)
            if lon+x >= n or matriz[x][y] != "*":
                x=random.randrange(n)
                y=random.randrange(n)
            else: #La palabra entra en la matriz
                break
        auxX=x
        auxY=y        
        i=0
        for p in palabra: #se fija que todos los espacios esten disponibles para escribir la palabra ("i" tiene que ser igual a la longitud de la palabra)
            letra=matriz[x][y]
            if letra == "*":                 
                x=x+1
                i=i+1
        if lon == i: #Si todos los espacios tienen "*" entonces se procederá a escribir la palabra
            for p in palabra:                       
                matriz[auxX][auxY]= str(p.upper())
                auxX+=1
            ok=True   
        if ok == True: #Si ok = True significa que la palabra fue agregada, sino tendrá que buscar nuevas coordenadas
            break 
        elif cont==5: #Si en 5 oportunidades la palabra no se pudo agregar no se agregará y se informará
            aux=""
            for element in palabra: # aux se queda con la palabra en forma de string (palabra es una lista) para poder imprimirla
                aux=aux+element
            sg.Popup('No se pudo agregar la palabra '+aux.upper())
            listaPalabras.remove(aux)
            break
        else:
            cont+=1                       
    return matriz

#La palabra se ingresara verticalmente
def meterPalabraVerticalmente(palabra,matriz,n,listaPalabras):
    ok=False #El ok determina si la palabra fue escrita en la sopa de letras
    x=random.randrange(n)
    y=random.randrange(n)
    cont=0 #indica las veces que se quiere agregar la palabra a la sopa de letras
    while True: #Tratará de ingresar la palabra sin que se "choque" con otra
        while True: #si la longitud de la palabra + el random "y" superan la altura de la matriz se volverá a seleccionar otro numero random hasta que la palabra entre
            lon=len(palabra)
            if lon+y >= n or matriz[x][y] != "*":
                x=random.randrange(n)
                y=random.randrange(n)
            else: #La palabra entra en la matriz
                break
        auxX=x
        auxY=y        
        i=0
        for p in palabra: #se fija que todos los espacios esten disponibles para escribir la palabra ("i" tiene que ser igual a la longitud de la palabra)
            letra=matriz[x][y]
            if letra == "*": #Si el lugar está disponible escribe la letra en la posicion de la matriz                   
                y=y+1
                i=i+1       
        if lon == i: #Si todos los espacios tienen "*" entonces se procederá a escribir la palabra
            for p in palabra:                       
                matriz[auxX][auxY]= str(p.upper())
                auxY+=1
            ok=True   
        if ok == True: #Si ok = True significa que la palabra fue agregada, sino tendrá que buscar nuevas coordenadas
            break 
        elif cont==5: #Si en 5 oportunidades la palabra no se pudo agregar no se agregará y se informará
            aux=""
            for element in palabra: # aux se queda con la palabra en forma de string (palabra es una lista) para poder imprimirla
                aux=aux+element
            sg.Popup('No se pudo agregar la palabra '+aux.upper())
            listaPalabras.remove(aux)
            break
        else:
            cont+=1    
    return matriz

#Crea el grafico
def comenzar(matriz, n, palabraSel, listaPal, ori):
    BOX_SIZE = 20 #tamaño de cada caja que contiene cada letra

    layout = [
    [sg.Text('SOPA DE LETRAS by PySimpleGUI', font=(15))],
    [sg.Graph((n*30, n*30), (0, n*22.5), (n*22.5, 0), key='Graph', change_submits=True, drag_submits=False)],
    [sg.Text('Sustantivos', font=(10)), sg.Text('  Adjetivos', font=(10)), sg.Text('   verbos', font=(10))],
    [sg.Listbox(values=listaPalabras[0][0], size=(n+1, n)), sg.Listbox(values=listaPalabras[0][1], size=(n+1, n)), sg.Listbox(values=listaPalabras[0][2], size=(n+1, n))],
    [sg.Button('Buscar Palabra'), sg.Button('Ayuda'), sg.Button('Exit')]
    ]

    window = sg.Window('Game', font=('Arial',10) ).Layout(layout).Finalize()
    g = window.FindElement('Graph')

    #Se dibuja la matriz en el grafico
    for i in range(n):
        for j in range(n):            
            g.DrawText('{}'.format(matriz[i][j]), (i * BOX_SIZE + 12, j * BOX_SIZE + 12))

    while True:
        event, values = window.Read()

        if event == 'Exit':
            break

        mouse = values['Graph']
        if event == 'Graph':
            if mouse == (None, None):
                continue
            y = mouse[0]//BOX_SIZE
            x = mouse[1]//BOX_SIZE           
            try:    
                palabraSel.append(matriz[y][x])
                g.DrawRectangle((y * BOX_SIZE, x * BOX_SIZE), (y * BOX_SIZE+BOX_SIZE-2, x * BOX_SIZE+BOX_SIZE-2), line_color='black') #La letra elegida obtiene un contorno azul
            except(IndexError): #se clickeo fuera de la sopa de letras
                g.DrawRectangle((y * BOX_SIZE, x * BOX_SIZE), (y * BOX_SIZE+BOX_SIZE-2, x * BOX_SIZE+BOX_SIZE-2), line_color='none')  
                print('fuera de rango')
               
        if event == 'Buscar Palabra':
            auxX=x
            auxY=y

            aux=""
            ok=False #si ok es falso, la palabra no existe

            for element in palabraSel: # aux se queda con la palabra seleccionada
                aux=aux+element
            
            for k in range(len(listaPal)): # recorre la lista de palabras (sus, adj, ver) para ver si se encuentra la palabra encontrada    
                for p in listaPal[k]:              
                    if aux == p.upper():    
                        sg.Popup("encontraste la palabra: "+aux)
                        if k==0: # la palabra encontrada es sustantivo
                            if ori == True: # es horizontal
                                for x in range(len(aux)):
                                    g.DrawRectangle((auxY * BOX_SIZE, auxX * BOX_SIZE), (auxY * BOX_SIZE+BOX_SIZE-2, auxX * BOX_SIZE+BOX_SIZE-2), line_color='yellow') 
                                    auxY-=1
                            else: # es vertical
                                for x in range(len(aux)): 
                                    g.DrawRectangle((auxY * BOX_SIZE, auxX * BOX_SIZE), (auxY * BOX_SIZE+BOX_SIZE-2, auxX * BOX_SIZE+BOX_SIZE-2), line_color='yellow')
                                    auxX-=1
                        elif k==1: # la palabra encontrada es adjetivo
                            if ori == True: # es horizontal
                                for x in range(len(aux)):
                                    g.DrawRectangle((auxY * BOX_SIZE, auxX * BOX_SIZE), (auxY * BOX_SIZE+BOX_SIZE-2, auxX * BOX_SIZE+BOX_SIZE-2), line_color='red') 
                                    auxY-=1
                            else: # es vertical
                                for x in range(len(aux)): 
                                    g.DrawRectangle((auxY * BOX_SIZE, auxX * BOX_SIZE), (auxY * BOX_SIZE+BOX_SIZE-2, auxX * BOX_SIZE+BOX_SIZE-2), line_color='red')
                                    auxX-=1 
                        else: # la palabra encontrada es verbo
                            if ori == True: # es horizontal
                                for x in range(len(aux)):
                                    g.DrawRectangle((auxY * BOX_SIZE, auxX * BOX_SIZE), (auxY * BOX_SIZE+BOX_SIZE-2, auxX * BOX_SIZE+BOX_SIZE-2), line_color='green') 
                                    auxY-=1
                            else: # es vertical
                                for x in range(len(aux)): 
                                    g.DrawRectangle((auxY * BOX_SIZE, auxX * BOX_SIZE), (auxY * BOX_SIZE+BOX_SIZE-2, auxX * BOX_SIZE+BOX_SIZE-2), line_color='green')
                                    auxX-=1                      
                        ok=True

            if ok==False: #La palabra no estaba dentro de la lista de palabras
                sg.Popup('La palabra "'+aux+'" no se encuentra dentro de la lista de palabras ingresadas', title="Palabra inexistente!", font="Arial", background_color="#CDCDCD")
                if ori == True:
                    for x in range(len(aux)):
                        g.DrawRectangle((auxY * BOX_SIZE, auxX * BOX_SIZE), (auxY * BOX_SIZE+BOX_SIZE-2, auxX * BOX_SIZE+BOX_SIZE-2), line_color='white') 
                        auxY-=1
                else:
                    for x in range(len(aux)):
                        g.DrawRectangle((auxY * BOX_SIZE, auxX * BOX_SIZE), (auxY * BOX_SIZE+BOX_SIZE-2, auxX * BOX_SIZE+BOX_SIZE-2), line_color='white')
                        auxX-=1                
            
            """for x in range(n):
                for y in range(n):
                    g.DrawRectangle((y * BOX_SIZE, x * BOX_SIZE), (y * BOX_SIZE+BOX_SIZE-2, x * BOX_SIZE+BOX_SIZE-2), line_color='white') """
            
            palabraSel=[] 

    window.Close() 
    
#------------------------------------------------------------PP------------------------------------------------------------#     

listaPalabras=[] #Contiene todas las palabras a ingresar a la sopa de letras 
max=0 #indicará la cantidad de letras maxima que contiene la lista de palabras y deterimnará el tamaño de la matriz

listaPalabras = vc.recibirDatos()
orientacion = listaPalabras[1]

#listaPalabras[0]= [listaSustantivos, listaAdjetivos, listaVerbos]
#listaPalabras[0][1]= ["casa", "auto"]
#listaPalabras[0][1][0]= "casa"

for j in range(3):
    for i in range(len(listaPalabras[0][j])):
        palabra=list(listaPalabras[0][j][i])
        num=len(palabra)
        if num >= max:
            max=num

n=max+1 #La cantidad de filas y columnas dependera de la palabra ingresada mas grande y se le suma 5 para que quepan las demas ingresadas
matriz=crearMatriz(n)

if orientacion == True: #la orientacion de las palabras es horizontal

    for j in range(3):
        for i in range(len(listaPalabras[0][j])):
            palabra=list(listaPalabras[0][j][i])
            meterPalabraHorizontalmente(palabra, matriz, n, listaPalabras[0][j])  
else: #la orientacion de las palabras es vertical

    for j in range(3): 
        for i in range(len(listaPalabras[0][j])):
            palabra=list(listaPalabras[0][j][i])
            meterPalabraVerticalmente(palabra, matriz, n, listaPalabras[0][j])

palabraSeleccionada=[]
llenarMatriz(matriz,n)
comenzar(matriz,n,palabraSeleccionada,listaPalabras[0], listaPalabras[1])