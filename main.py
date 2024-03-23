from flask import Flask, request
from scraping import space_track_conceptos
import requests
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
  response = {"time":"","data":{}}
  tipo = request.args.get('tipo', default="no_forzar")
  if not os.path.exists('rss/space_track_conceptos.json') or tipo.upper() == "FORZAR":
    with open('rss/space_track_conceptos.json', 'w') as doc:
      datos = space_track_conceptos()
      if datos:
        json.dump(datos, f)
      response.time = "NEW"
      response.data = datos
  else:
    with open('rss/space_track_conceptos.json',"r+") as doc:
      datos = json.load(doc)
      if not datos:
        datos = space_track_conceptos()
        json.dump(datos, doc)
        response.time = "NEW"
        response.data = datos
      else:
        response.time = "NO_NEW"
        response.data = datos
  return response
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=int(os.environ.get('PORT', 5000)),debug=False)
