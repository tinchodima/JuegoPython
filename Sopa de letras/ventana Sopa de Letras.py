import random
import string
import sys
import PySimpleGUI as sg


#sys.version_info[0] saber version del pysimplegui

BOX_SIZE = 22

listaPalabras=['Palabra1', 'Palabra2', 'Palabra3','Palabra4', 'Palabra5', 'Palabra6']
layout = [
    [sg.Text('SOPA DE LETRAS by PySimpleGUI', font=(15)), sg.Text('                                                                                      Lista de Palabras:',font=(15))],
    [sg.Graph((600, 550), (0, 450), (450, 0), key='Graph', change_submits=True, drag_submits=False), sg.Listbox(values=listaPalabras, size=(16, 30))],
    [sg.Button('Buscar Palabra'), sg.Button('Ayuda'), sg.Button('Exit')]
]
window = sg.Window('Game', font=('Arial',10) ).Layout(layout).Finalize()
g = window.FindElement('Graph')

"""palabra='HOLA'
lis=list(palabra)
num=random.randrange(3)
        if num==0:
            for aux in lis:
                g.DrawText('{}'.format(aux), (row * BOX_SIZE + 12, col * BOX_SIZE + 12))"""


matriz = []
for i in range(20):
    matriz.append([])
    for j in range(20):  
        letra = random.choice(string.ascii_uppercase)
        g.DrawText('{}'.format(letra), (i * BOX_SIZE + 12, j * BOX_SIZE + 12)) 
        matriz[i].append(letra)

palabra=[]
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
        print('x:',x,'y:',y)
        g.DrawRectangle((y * BOX_SIZE, x * BOX_SIZE), (y * BOX_SIZE+BOX_SIZE-2, x * BOX_SIZE+BOX_SIZE-2), line_color='blue')
        palabra.append(matriz[x][y])

    if event == 'Buscar Palabra':
        for element in palabra:
            print(element)

window.Close() 
      
