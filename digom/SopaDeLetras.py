#Gomez, Brian Agustin
#Di Maria, Juan Martin
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
            pal=''
            for element in palabra: # pal se queda con la palabra en forma de string (palabra es una lista) para poder imprimirla
                pal=pal+element
            sg.Popup('No se pudo agregar la palabra '+pal.upper())
            listaPalabras.remove(pal)
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
            pal=''
            for element in palabra: # pal se queda con la palabra en forma de string (palabra es una lista) para poder imprimirla
                pal=pal+element
            sg.Popup('No se pudo agregar la palabra '+pal.upper())
            listaPalabras.remove(pal)
            break
        else:
            cont+=1    
    return matriz

def posLetraMatriz(x,y): #se guarda la posicion de cada letra seleccionada en la matriz y si la posicion ya estaba devuelve true y no la agrega
    pos=[]
    pos.append(x)
    pos.append(y)
    if pos in listPosiciones:
        listPosiciones.remove(pos)
        return True
    else:
        listPosiciones.append(pos)
    return False

#--------------------------------------------------------------Crea el gráfico--------------------------------------------------------------#

def graficar(matriz, n, palabraSel, listaPal, ori, colores, palabrasEncontradas, ayuda):
    BOX_SIZE = 22 #tamaño de las cajas que contiene cada letra

    layout = [
    [sg.Text('DIGOM: Sopa de letras', font=(15), text_color='blue')],
    [sg.Graph((n*30, n*30), (0, n*22.5), (n*22.5, 0), key='Graph', change_submits=True, drag_submits=False)],
    [sg.Button('Buscar Palabra'), sg.Button('Ayuda'), sg.Button('Exit')]
    ]

    if (ayuda):
        layout.append(
        [sg.Text('Sustantivos', font=(10), background_color=colores['cSus']), sg.Text('   Adjetivos', font=(10), background_color=colores['cAdj']), sg.Text('    Verbos', font=(10), background_color=colores['cVer'])]
        )
        layout.append(
            [sg.Listbox(values=listaPalabras[0][0], size=(n+1, n-1)), sg.Listbox(values=listaPalabras[0][1], size=(n+1, n-1)), sg.Listbox(values=listaPalabras[0][2], size=(n+1, n-1))]
        )

    window = sg.Window('Game', font=('Arial',10) ).Layout(layout).Finalize()
    g = window.FindElement('Graph')

    #Dibuja la matriz en el gráfico
    for i in range(n):
        for j in range(n):            
            g.DrawText('{}'.format(matriz[i][j]), (i * BOX_SIZE + 12, j * BOX_SIZE + 12))

    aux=''
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
            
            '''if(aux==matriz[y][x] and len(palabraSel)!=0): #si se repite la letra se elimina de la lista. PROBLEMA SI ELIJE LA MISMA LETRA EN CASO DE PERRO 
                palabraSel.pop()
            aux=matriz[y][x]'''

            posLetra=posLetraMatriz(x,y)
            try:                               
                palabraSel.append(matriz[y][x])  
                g.DrawRectangle((y * BOX_SIZE, x * BOX_SIZE), (y * BOX_SIZE+BOX_SIZE-2, x * BOX_SIZE+BOX_SIZE-2), line_color='black') #La letra elegida obtiene un contorno negro
                if posLetra == True: #Si está ya agregada la posicion de la letra se deseleccionará
                    try:
                        palabraSel.remove(matriz[y][x])
                        palabraSel.remove(matriz[y][x]) #Para que elimine bien tiene que estar 2 vceces
                        g.DrawRectangle((y * BOX_SIZE, x * BOX_SIZE), (y * BOX_SIZE+BOX_SIZE-2, x * BOX_SIZE+BOX_SIZE-2), line_color='white')
                    except(ValueError):
                        sg.Popup('no se puede deseleccionar una letra de una palabra ya encontrada')                        
                        
            except(IndexError): #click fuera de la sopa de letras
                g.DrawRectangle((y * BOX_SIZE, x * BOX_SIZE), (y * BOX_SIZE+BOX_SIZE-2, x * BOX_SIZE+BOX_SIZE-2), line_color='none')

        if event == 'Buscar Palabra':
            auxX=x
            auxY=y
            pal=''
            ok=False #si ok es falso, la palabra no existe

            for element in palabraSel: # pal se queda con la palabra seleccionada
                pal=pal+element

            if(not pal in palabrasEncontradas):
                for k in range(len(listaPal)): # recorre la lista de palabras (sus, adj, ver) para ver si se encuentra la palabra encontrada    
                    for p in listaPal[k]:              
                        if pal == p.upper():    
                            if k==0: # la palabra encontrada es sustantivo
                                if ori == True: # es horizontal
                                    for x in range(len(pal)):
                                        g.DrawRectangle((auxY * BOX_SIZE, auxX * BOX_SIZE), (auxY * BOX_SIZE+BOX_SIZE-2, auxX * BOX_SIZE+BOX_SIZE-2), line_color=colores['cSus']) 
                                        auxY-=1
                                else: # es vertical
                                    for x in range(len(pal)): 
                                        g.DrawRectangle((auxY * BOX_SIZE, auxX * BOX_SIZE), (auxY * BOX_SIZE+BOX_SIZE-2, auxX * BOX_SIZE+BOX_SIZE-2), line_color=colores['cSus'])
                                        auxX-=1
                            elif k==1: # la palabra encontrada es adjetivo
                                if ori == True: # es horizontal
                                    for x in range(len(pal)):
                                        g.DrawRectangle((auxY * BOX_SIZE, auxX * BOX_SIZE), (auxY * BOX_SIZE+BOX_SIZE-2, auxX * BOX_SIZE+BOX_SIZE-2), line_color=colores['cAdj']) 
                                        auxY-=1
                                else: # es vertical
                                    for x in range(len(pal)): 
                                        g.DrawRectangle((auxY * BOX_SIZE, auxX * BOX_SIZE), (auxY * BOX_SIZE+BOX_SIZE-2, auxX * BOX_SIZE+BOX_SIZE-2), line_color=colores['cAdj'])
                                        auxX-=1 
                            else: # la palabra encontrada es verbo
                                if ori == True: # es horizontal
                                    for x in range(len(pal)):
                                        g.DrawRectangle((auxY * BOX_SIZE, auxX * BOX_SIZE), (auxY * BOX_SIZE+BOX_SIZE-2, auxX * BOX_SIZE+BOX_SIZE-2), line_color=colores['cVer']) 
                                        auxY-=1
                                else: # es vertical
                                    for x in range(len(pal)): 
                                        g.DrawRectangle((auxY * BOX_SIZE, auxX * BOX_SIZE), (auxY * BOX_SIZE+BOX_SIZE-2, auxX * BOX_SIZE+BOX_SIZE-2), line_color=colores['cVer'])
                                        auxX-=1
                            sg.Popup("encontraste la palabra: "+pal)                                  
                            ok=True

                if ok==False: #La palabra no estaba dentro de la lista de palabras
                    sg.Popup('La palabra "'+pal+'" no se encuentra dentro de la lista de palabras ingresadas', title="Palabra inexistente!", font="Arial", background_color="#CDCDCD")
                    if ori == True:
                        for x in range(len(pal)):
                            g.DrawRectangle((auxY * BOX_SIZE, auxX * BOX_SIZE), (auxY * BOX_SIZE+BOX_SIZE-2, auxX * BOX_SIZE+BOX_SIZE-2), line_color='white') 
                            auxY-=1
                    else:
                        for x in range(len(pal)):
                            g.DrawRectangle((auxY * BOX_SIZE, auxX * BOX_SIZE), (auxY * BOX_SIZE+BOX_SIZE-2, auxX * BOX_SIZE+BOX_SIZE-2), line_color='white')
                            auxX-=1
            else:
                sg.Popup('Ya encontraste esa palabra!')     
                palabrasEncontradas.pop()

            palabrasEncontradas.append(pal)
            palabraSel=[] 

    window.Close() 

def recibirDatosConfiguracion():
    listaPalabras=[] #Contiene todas las palabras a ingresar a la sopa de letras    
    listaPalabras = vc.recibirDatos() #recibe una lista de listas desde la ventana configuracion
    colores = vc.recibirColores() #diccionario con colores de los tipos de letra
    return listaPalabras, colores

#------------------------------------------------------------PP------------------------------------------------------------#     
listaPalabras=recibirDatosConfiguracion()[0]
colores=recibirDatosConfiguracion()[1]
ayuda=listaPalabras[2]
max=0 #indicará la cantidad de letras maxima que contiene la lista de palabras y deterimnará el tamaño de la matriz

if len(listaPalabras) != 0:
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

    palabrasEncontradas=[] #lista de las palabras encontradas
    palabraSeleccionada=[] #una lista con la palabra seleccionada
    listPosiciones=[] #posicion de la letra seleccionada de la matriz
    llenarMatriz(matriz,n)
    graficar(matriz, n, palabraSeleccionada, listaPalabras[0], listaPalabras[1], colores, palabrasEncontradas, ayuda)