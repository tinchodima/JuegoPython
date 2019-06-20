from pattern.web import Wiktionary, DOM

w = Wiktionary(language="es")

a = w.search('rojo')

# ~ clasificarPalabra = a.sections[3].title


definicion = a.sections[3].content.split('1')[1].split('.2')[0].split('*')[0]
clasificacion = a.sections[3].content.split()[0]
# ~ print(clasificacion)



titulos = a.sections[3].title.upper()

if clasificacion.lower() == "sustantivo":
	print('Sustantivo')
elif clasificacion.lower() == "adjetivo":
	print('Adjetivo')
else:
	print('Verbo')


# ~ if a.sections[3].title.upper()[0] == "S":
    # ~ print('Es un Sustantivo')
# ~ if a.sections[3].title.upper()[0] == "A":
    # ~ print('Es un Adjetivo')
# ~ if a.sections[3].title.upper()[0] == "V":
	# ~ print('Es un verbo')


