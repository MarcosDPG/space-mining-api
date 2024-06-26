from flask import Flask, request, send_from_directory, send_file
from scraping import space_track_conceptos
from datetime import datetime
from io import BytesIO
import requests
import json
import os
import threading
import extractData
import buildImages

app = Flask(__name__)
@app.route("/")
def hello():
  return "API de SPACE MINIG en tu disposicion."
@app.route('/data/conceptos/space_track', methods=['GET'])
def conceptos_ST():
  response = {"time":"","data":{},"type":""}
  tipo = request.args.get('tipo', default="no_forzar")
  if not os.path.exists('rss'):
    os.makedirs('rss')
    os.makedirs('rss/filesjson')
  if not os.path.exists('rss/filesjson/space_track_conceptos.json') or tipo.upper() == "FORZAR":
    with open('rss/filesjson/space_track_conceptos.json', 'w') as doc:
      datos = space_track_conceptos()
      response['time'] = datetime.now().strftime("%Y%m%d")
      response['data'] = datos
      response['type'] = "NEW"
      if datos:
        json.dump(response, doc)
  else:
    with open('rss/filesjson/space_track_conceptos.json',"r") as doc:
      datos = json.load(doc)
      if not datos['data']:
        datos['data'] = space_track_conceptos()
        response['time'] = datetime.now().strftime("%Y%m%d")
        response['data'] = datos['data']
        response['type'] = "NEW"
      else:
        if (datetime.now() - datetime.strptime(datos['time'], "%Y%m%d")).days >=7 :
          response['time'] = datetime.now().strftime("%Y%m%d")
          response['data'] = datos['data']
          response['type'] = "NEW"
        else:
          response['time'] = datos['time']
          response['data'] = datos['data']
          response['type'] = "no_NEW"
    with open('rss/filesjson/space_track_conceptos.json', "w") as doc:
          json.dump(response, doc)
    if(response['type'] == "NEW"):
      hilo2 = threading.Thread(target=traducirSegundoPlano, args=(response,))
      hilo2.start()
  return response

def traducirSegundoPlano(response):
  response_copia = response
  try:
    response['data'] = space_track_conceptos()
  except:
     response['data'] = response_copia['data']
  finally:
    with open('rss/filesjson/space_track_conceptos.json', "w") as doc:
            json.dump(response, doc)

@app.route("/data/images/update")
def update_images():
    urli = "rss/filesjson/detalles-in-orbit.json"
    urln = "rss/filesjson/detalles-no-in-orbit.json"
    retorno = ""
    if(not os.path.exists(urli) or  
       not os.path.exists(urln)):
        #No exiten por ende los crea
        retorno += update_files(forzar=False)
    retorno += buildImages.generarImagenes(forzar=True)
    return retorno

@app.route('/data/images/get', methods=['GET'])
def get_images():
    exitenJson()
    # if key doesn't exist, returns None
    orbita = request.args.get('orbita',default="None")
    grafico = request.args.get('grafico',default="None")
    ejes = request.args.get('ejes',default="None")
    if(os.path.exists(f"rss/images/{orbita.upper()}/{grafico}/{ejes.upper()}.png")):
        return send_file(f"rss/images/{orbita.upper()}/{grafico}/{ejes.upper()}.png")
    else:
        return send_file('error.png')

def exitenJson():
    urli = "rss/filesjson/detalles-in-orbit.json"
    urln = "rss/filesjson/detalles-no-in-orbit.json"
    if(not os.path.exists(urli) or  
       not os.path.exists(urln)):
        #No exiten por ende los crea
        update_files(forzar=False)
        buildImages.generarImagenes()
    else:
        #Existen por ende pasa a revisar json
        revisar_json(urli,urln)

def revisar_json(urli,urln):
    datosi = {}
    datosn = {}
    with open(urli) as file:
        datosi = json.load(file)
    with open(urln) as file:
        datosn = json.load(file)
    if ((datetime.now() - datetime.strptime(datosi['date'], "%Y%m%d")).days >= 8 or
        (datetime.now() - datetime.strptime(datosn['date'], "%Y%m%d")).days >= 8):
        #El tiempo que llevan es mayor al limite, por ende se actualiza en segundo plano
        hilo1 = threading.Thread(target=updateParalelo)
        hilo1.start()
    else:
        #El tiempo que llevan es menor al limite
        datosi["type"] ,datosn["type"]  = "noNew","noNew"
        with open("rss/filesjson/detalles-in-orbit.json", 'w') as f:
            json.dump(datosi, f)
        with open("rss/filesjson/detalles-no-in-orbit.json", 'w') as f:
            json.dump(datosn, f)
        #Revisa si las imagenes está actualizadas, pero en segundo plano
        hilo1 = threading.Thread(target=buildImages.generarImagenes)
        hilo1.start()

def updateParalelo():
    update_files(forzar=False)
    buildImages.generarImagenes()

#Forzar a actualizar los csv y las imagenes    
@app.route("/data/update")
def updateImagesFiles():
    retorno = ""
    retorno += update_files(forzar=True)
    retorno += buildImages.generarImagenes(forzar=True)
    return retorno

#Forzar a actualizar los csv
@app.route("/data/csv/update_files")
def update_files(forzar = True):
    inActualizar = False
    noinActualizar = False
    if (forzar):
        inActualizar = True
        noinActualizar = True
    retorno = "Se revisaron los archivos - Todo en orden"
    
    if(os.path.exists("rss/filesjson/detalles-in-orbit.json") and not inActualizar):
        datos = {}
        with open("rss/filesjson/detalles-in-orbit.json") as file:
            datos = json.load(file)
        if (datetime.now() - datetime.strptime(datos['date'], "%Y%m%d")).days >= 8 :
            inActualizar = True
        else:
            datos["type"] = "noNew"
            with open("rss/filesjson/detalles-in-orbit.json", 'w') as f:
                json.dump(datos, f)
    else:
        inActualizar = True

    if(os.path.exists("rss/filesjson/detalles-no-in-orbit.json") and not noinActualizar):
        datos = {}
        with open('rss/filesjson/detalles-no-in-orbit.json') as file:
            datos = json.load(file)
        if (datetime.now() - datetime.strptime(datos['date'], "%Y%m%d")).days >= 8 :
            noinActualizar = True
        else:
            datos["type"] = "noNew"
            with open("rss/filesjson/detalles-no-in-orbit.json", 'w') as f:
                json.dump(datos, f)
    else:
        noinActualizar = True

    if(inActualizar or noinActualizar):
        configUsr = os.getenv("USERNAME_SPACE_TRACK")
        configPwd = os.getenv("PASSWORD_SPACE_TRACK")
        siteCred = {'identity': configUsr, 'password': configPwd}

        uriBase                = "https://www.space-track.org"
        requestLogin           = "/ajaxauth/login"

        try: 
            with requests.Session() as session:
                # Primer se debe loguear. Si se recibe una respuesta diferente a 200 implica que no se logró
                resp = session.post(uriBase + requestLogin, data = siteCred)
                if resp.status_code != 200:
                    raise Exception("No se pudo hacer login")
                if(noinActualizar):
                    extractData.noInOrbita(session)
                    extractData.limpiarNoInOrbit()
                if(inActualizar):
                    extractData.inOrbita(session)
                    extractData.limpiarInOrbit()
            retorno = "Se crearon/actualizaron y limpiaron los datos"
        except Exception as e:
            retorno = e.args[0]
    return retorno


@app.route('/data/files/<type>/<file>', methods=['GET'])
def get_file_rows(type,file):
    json_path = f'rss/files{type}/{file}'
    if os.path.exists(json_path):
        return send_from_directory(f'rss/files{type}', file)
    else:
        return f"El archivo {type} no existe en el servidor.", 404
    
@app.route('/data/files/rows/<n_rows>/<csv>', methods=['GET'])
def get_file(n_rows,csv):
    json_data = extractData.traerRows(int(n_rows),f'rss/filescsv/{csv}')
    # Convertir el JSON a un objeto BytesIO
    json_bytesio = BytesIO(json_data.encode())
    # Enviar el BytesIO como archivo adjunto
    return send_file(json_bytesio, as_attachment=True, download_name='resultado.json')

@app.route('/data/files/apk/<file>', methods=['GET'])
def get_file_apk(file):
    path = f"rss/filesapk/{file}"
    if os.path.exists(path):
        return send_file(path, as_attachment=True, download_name='space-mining.apk')
    else:
        return f"El archivo no existe en el servidor.", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=int(os.environ.get('PORT', 5000)),debug=False)
