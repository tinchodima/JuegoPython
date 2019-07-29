from SopaDeLetras import Digom
import ventanaConfiguracion
from Configuracion import Configuracion

if __name__ == "__main__":
    conf = Configuracion()
    conf.graficarConfiguracion()
    d = Digom()
    d.crearMatriz()
    d.meterPalabrasEnMatriz()
    d.llenarMatriz()
    d.graficar()
