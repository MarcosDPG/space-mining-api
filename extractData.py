import pandas as pd
from io import StringIO
import os
from datetime import datetime
import json

uriBase                = "https://www.space-track.org"
requestCmdAction       = "/basicspacedata/query" 
requestInOrbit         = "/class/satcat/predicates/OBJECT_ID,COUNTRY,PERIOD,INCLINATION,APOGEE,PERIGEE,RCS_SIZE,LAUNCH/DECAY/null-val/CURRENT/Y/orderby/NORAD_CAT_ID%20desc/format/csv/emptyresult/show"
requestNoInOrbit       = "/class/satcat/predicates/OBJECT_ID,COUNTRY,PERIOD,INCLINATION,APOGEE,PERIGEE,RCS_SIZE,LAUNCH,DECAY/DECAY/%3C%3Enull-val/CURRENT/Y/orderby/NORAD_CAT_ID%20desc/format/csv/emptyresult/show"

def noInOrbita(session):
    # Realizamos la consulta
    resp = session.get(uriBase + requestCmdAction + requestNoInOrbit)
    if resp.status_code != 200:
        raise Exception("No se pudo hacer la consulta noInOrbita")
    df = pd.read_csv(StringIO(resp.text))
    crearCarpetas()
    df.to_csv("rss/filescsv/data-no-in-orbit.csv", sep=',', index=False, encoding='utf-8')
    
    with open("rss/filesjson/detalles-no-in-orbit.json", "w") as archivo:
        detalles = {"date":datetime.now().strftime("%Y%m%d"),"type":"NEW"}
        json.dump(detalles,archivo)
    
def inOrbita(session):
    # Realizamos la consulta
    resp = session.get(uriBase + requestCmdAction + requestInOrbit)
    if resp.status_code != 200:
        raise Exception("No se pudo hacer la consulta InOrbita")
    crearCarpetas()
    df = pd.read_csv(StringIO(resp.text))
    df.to_csv("rss/filescsv/data-in-orbit.csv", sep=',', index=False, encoding='utf-8')
    with open("rss/filesjson/detalles-in-orbit.json", "w") as archivo:
        detalles = {"date":datetime.now().strftime("%Y%m%d"),"type":"NEW"}
        json.dump(detalles,archivo)

def crearCarpetas():
    if not os.path.exists('rss/filescsv'):
        os.makedirs('rss/filescsv')
    if not os.path.exists('rss/filesjson'):
        os.makedirs('rss/filesjson')

def limpiarNoInOrbit():
    df_i = pd.read_csv("rss/filescsv/data-no-in-orbit.csv")
    df_i = limpiarDf(df_i)
    df_i.to_csv("rss/filescsv/data-no-in-orbit.csv", sep=',', index=False, encoding='utf-8')

def limpiarInOrbit():
    df_i = pd.read_csv("rss/filescsv/data-in-orbit.csv")
    df_i = limpiarDf(df_i)
    df_i.to_csv("rss/filescsv/data-in-orbit.csv", sep=',', index=False, encoding='utf-8')

def limpiarDf(df_i):
    #Borrar nulos
    df_i.dropna(subset=['APOGEE', 'PERIOD', 'PERIGEE', 'INCLINATION'], inplace=True)
    #Borrar valores en 0
    df_i = df_i[(df_i['APOGEE'] > 0) & (df_i['PERIOD'] > 0) & (df_i['PERIGEE'] > 0) & (df_i['INCLINATION'] > 0)]
    #Cambiar los rcs_size nulos por indefinidos
    #df_i['RCS_SIZE'].fillna('UNDEFINED', inplace=True)
    df_i = df_i.fillna({'RCS_SIZE':'UNDEFINED'})
    #pasar launch y decay a tipo fecha
    df_i['LAUNCH'] = pd.to_datetime(df_i['LAUNCH'])

    if(df_i.shape[1]==9):
        df_i['DECAY'] = pd.to_datetime(df_i['DECAY'])
        #crear dias en orbita
        df_i['DAYS_IN_ORBIT'] = (df_i['DECAY'] - df_i['LAUNCH']).dt.days
        #filtrar datos
        df_i = df_i[((df_i['PERIOD']<120) & (df_i['APOGEE']<800) & (df_i['PERIGEE']<800) & (df_i['DAYS_IN_ORBIT']<12000))]
    else:
        df_i = df_i[((df_i['PERIOD']<120) & (df_i['APOGEE']<800) & (df_i['PERIGEE']<800))]
    return df_i

def traerRows(n,data):
    try:
        df = pd.read_csv(data)
        df = df[['OBJECT_ID', 'APOGEE', 'PERIOD', 'PERIGEE', 'INCLINATION']]
        # Verificar si n es mayor que la longitud del DataFrame
        if n > len(df):
            raise ValueError('La cantidad de registros solicitados es mayor que la longitud del DataFrame')
        # elegir aleatoriamente n filas y guardarlas en un diccionario
        df_dict = df.sample(n).to_dict(orient='records')
        # Convertir el diccionario a JSON
        df_json = json.dumps(df_dict)
        return df_json
    except Exception as e:
        # Manejar la excepción y devolver un JSON con error
        error_dict = {
            "OBJECT_ID": "error",
            "APOGEE": "error",
            "PERIOD": "error",
            "PERIGEE": "error",
            "INCLINATION": "error"
        }
        error_json = json.dumps([error_dict] * n)
        return error_json