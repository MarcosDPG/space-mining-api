import requests
from bs4 import BeautifulSoup
import deepl
import os
import configparser

config = configparser.ConfigParser()
config.read("./config/SpaceMining.ini")

auth_key = os.getenv("AUTH_KEY")
translator = deepl.Translator(auth_key)

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
            tags_vacios = ["Complete Data Files","Current Catalog Files","Launch Site","Owner/Operator (O/O)"]
            if (tag.get_text() in tags_vacios):
                continue
            elif (tag.name=="dt"):
                definicion_dict[titulo]=definicion
                titulo = tag.get_text()
                #titulo = translator.translate_text(tag.get_text(),target_lang="ES").text
                definicion=[]
            elif (tag.name=="dd"):
                texto = tag.get_text().replace("\n","").replace("link","").replace("                    ","").replace("                ","").replace("See: ","")
                #definicion.append(texto)
                if (texto == ""):
                    continue
                definicion.append(translator.translate_text(texto, target_lang="ES").text)

        # Agregar la última definición después del bucle
        definicion_dict[titulo] = definicion
        return definicion_dict
    except:
        return {}