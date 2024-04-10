from flask import Flask, request
from scraping import space_track_conceptos
from datetime import datetime
import requests
import json
import os
app = Flask(__name__)
@app.route("/")
def hello():
  return "API de SPACE MINIG en desarrollo."
@app.route('/data', methods=['GET'])
def proxy():
  url = request.args.get('url')
  response = requests.get(url)
  return response.content, response.status_code, response.headers.items()
@app.route('/data/conceptos/space_track', methods=['GET'])
def conceptos_ST():
  response = {"time":"","data":{},"type":""}
  tipo = request.args.get('tipo', default="no_forzar")
  if not os.path.exists('rss'):
    os.makedirs('rss')
  if not os.path.exists('rss/space_track_conceptos.json') or tipo.upper() == "FORZAR":
    with open('rss/space_track_conceptos.json', 'w') as doc:
      datos = space_track_conceptos()
      response['time'] = datetime.now().strftime("%Y%m%d")
      response['data'] = datos
      response['type'] = "NEW"
      if datos:
        json.dump(response, doc)
  else:
    with open('rss/space_track_conceptos.json',"r+") as doc:
      datos = json.load(doc)
      if not datos['data']:
        datos['data'] = space_track_conceptos()
        response['time'] = datetime.now().strftime("%Y%m%d")
        response['data'] = datos['data']
        response['type'] = "NEW"
        json.dump(response, doc)
      else:
        if (datetime.now() - datetime.strptime(datos['time'], "%Y%m%d")).days >=1 :
          datos['data'] = space_track_conceptos()
          response['time'] = datetime.now().strftime("%Y%m%d")
          response['data'] = datos['data']
          response['type'] = "NEW"
        else:
          response['time'] = datos['time']
          response['data'] = datos['data']
          response['type'] = "no_NEW"
      json.dump(response, doc)
  return response

@app.route('/data/conceptos/space_track/json', methods=['GET'])
def get_space_track_json():
    json_path = 'rss/space_track_conceptos.json'
    if os.path.exists(json_path):
        return send_from_directory('rss', 'space_track_conceptos.json')
    else:
        return "El archivo JSON no existe en el servidor.", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=int(os.environ.get('PORT', 5000)),debug=False)
