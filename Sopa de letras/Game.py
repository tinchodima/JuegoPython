class Game:
    def __init__(self,cantPalabras=0,sus=[],adj=[],verbos=[],agregarPalabra=False):
        self.cantPalabras=cantPalabras
        self.sus=sus
        self.adj=adj
        self.verbos=verbos
        self.agregarPalabra=agregarPalabra

    def AgregarPalabra(self):
        self.cantPalabras+=1
    def QuitarPalabra(self):
        self.cantPalabras-=1

    def AgregarSus(self, sus):
        self.sus.append(sus)
    def AgregarAdj(self,adj):
        self.adj.append(adj) 
    def AgregarVerbo(self, verbo):
        self.verbos.append(verbo)
        
    def EmpezarJuego(self):
        