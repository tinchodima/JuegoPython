#!/usr/bin/python3
#-*- coding: utf-8 -*-

import random
import string
import sys
import PySimpleGUI as sg

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
    cont=0 #indica las veces que se quiere agregar la palabra a la sopa de letras
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
def comenzar(matriz, n, palabra, listaPalabras):
    BOX_SIZE = 20 #tamaño de cada caja que contiene cada letra

    layout = [
    [sg.Text('SOPA DE LETRAS by PySimpleGUI', font=(15))],
    [sg.Graph((n*30, n*30), (0, n*22.5), (n*22.5, 0), key='Graph', change_submits=True, drag_submits=False), sg.Listbox(values=listaPalabras, size=(n+3, n+6))],
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
                palabra.append(matriz[y][x])
                g.DrawRectangle((y * BOX_SIZE, x * BOX_SIZE), (y * BOX_SIZE+BOX_SIZE-2, x * BOX_SIZE+BOX_SIZE-2), line_color='blue') #La letra elegida obtiene un contorno azul
            except(IndexError): #se clickea fuera de la sopa de letras
                print('fuera de rango')              

        if event == 'Buscar Palabra':
            aux=""
            ok=False

            for element in palabra: # aux se queda con la palabra seleccionada
                aux=aux+element

            for p in listaPalabras: # recorre las listas de palabras a buscar para ver si se encuentra la palabra encontrada                   
                if aux == p.upper():    
                    sg.Popup("Felicitaciones! encontraste la palabra: "+aux, title="Palabra encontrada!", font="Arial", background_color="#CDCDCD")
                    ok=True
            if ok==False: #La palabra no estaba dentro de la lista de palabras
                sg.Popup('La palabra "'+aux+'" no se encuentra dentro de la lista de palabras ingresadas', title="Palabra inexistente!", font="Arial", background_color="#CDCDCD")
            
            for x in range(n):
                for y in range(n):
                    g.DrawRectangle((y * BOX_SIZE, x * BOX_SIZE), (y * BOX_SIZE+BOX_SIZE-2, x * BOX_SIZE+BOX_SIZE-2), line_color='white')  
            palabra=[] 

    window.Close() 
    
#------------------------------------------------------------PP------------------------------------------------------------#     

listaPalabras=[] #Contiene todas las palabras a ingresar a la sopa de letras 
max=0 #indicará la cantidad de letras maxima que contiene la lista de palabras y deterimnará el tamaño de la matriz
while True:
    pal=input("Agregar palabra: ")
    if pal == "z":
        break
    if len(pal)>max:
        max=len(pal)
    listaPalabras.append(pal)

n=max+2 #La cantidad de filas y columnas dependera de la palabra ingresada mas grande y se le suma 2 para que quepan mas palabras
matriz=crearMatriz(n)

#Recorre la lista de palabras y las ingresa a la matriz 
for i in range(len(listaPalabras)):
    palabra=list(listaPalabras[i]) 
    num=random.randrange(100)
    if num <= 50: #Habrá un 50% de posibilidades de que la palabra se ingrese horizontalmente o verticalmente 
        meterPalabraHorizontalmente(palabra, matriz, n, listaPalabras)
    else:
        meterPalabraVerticalmente(palabra, matriz, n, listaPalabras)

palabra=[]
llenarMatriz(matriz,n)
comenzar(matriz,n,palabra,listaPalabras)