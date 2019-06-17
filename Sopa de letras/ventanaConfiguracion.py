#import Game
import sys
import PySimpleGUI as sg

   

layout = [
    [sg.Text('Sopa de Letras con PySimpleGUI', size=(32, 1), font=('Time New Roman', 14), background_color='#CDCDCD')],
    [sg.Text('● Ingrese una palabra:', text_color='blue',font=('Time New Roman', 12), background_color='#CDCDCD'), sg.InputText(), sg.Submit('Agregar'), sg.Submit('Quitar')],
    [sg.Text('● Nivel de dificultad:     ', text_color='blue', font=('Time New Roman', 11), background_color='#CDCDCD'), sg.Radio('Fácil ', "RADIO1", default=True, background_color='#CDCDCD'), sg.Radio('Mediano', "RADIO1", background_color='#CDCDCD'), sg.Radio('Difícil', "RADIO1", background_color='#CDCDCD')],
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


window.Close()