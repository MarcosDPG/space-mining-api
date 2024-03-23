import requests
from bs4 import BeautifulSoup
import json

def space_track_conceptos():
    try:
        pagina_web_respuesta = requests.get('https://www.space-track.org/documentation#/legend')
        pagina_web = pagina_web_respuesta.content
        soup = BeautifulSoup(pagina_web, "html.parser")
        definiciones = soup.dl
        titulo = "Space Mining"
        definicion = ["Super aplicacion para el estudio de objetos espaciales"]
        definicion_dict = {}

        for tag in definiciones:
            if (tag.name=="dt"):
                definicion_dict[titulo]=definicion
                titulo = tag.get_text()
                definicion=[]
            elif (tag.name=="dd"):
                definicion.append(tag.get_text())

        # Agregar la última definición después del bucle
        definicion_dict[titulo] = definicion
        return definicion_dict
    except:
        return {}
