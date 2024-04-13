from datetime import datetime
import os
import pandas as pd
import matplotlib
import json
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def generarImagenes(forzar = False):
    urli = "rss/filesjson/detalles-imagenes.json"
    if(os.path.exists(urli)):
        datos = {}
        with open(urli) as archivo:
            datos = json.load(archivo)
        if ((datetime.now() - datetime.strptime(datos['date'], "%Y%m%d")).days < 1) and not forzar :
            with open(urli,"w") as archivo:
                datos["type"] = "noNew"
                json.dump(datos,archivo)
            return "No se tiene que graficar aún"

    patht = "rss/images/T"
    pathf = "rss/images/F"
    if(not os.path.exists("rss/images/")):
       os.mkdir("rss/images/")
       os.mkdir(patht)
       os.mkdir(pathf)
    
    df_t = pd.read_csv("rss/filescsv/data-in-orbit.csv")
    df_f = pd.read_csv("rss/filescsv/data-no-in-orbit.csv")

    try:
        crearImagenes(df_t,patht)
        crearImagenes(df_f,pathf)
        return "Creación/Actualización de imagenes exitosa"
    except Exception as e:
        return e.args[0]

def crearImagenes(df,pathe):
    #crear la imagenes de dispersion
    colums_graficar = ["APOGEE","PERIOD","PERIGEE","INCLINATION"]
    letra = 0
    if(not os.path.exists("rss/images/T/0")):
       os.mkdir("rss/images/T/0")
       os.mkdir("rss/images/T/1")
       os.mkdir("rss/images/T/2")
       os.mkdir("rss/images/T/3")

    if(not os.path.exists("rss/images/F/0")):
       os.mkdir("rss/images/F/0")
       os.mkdir("rss/images/F/1")
       os.mkdir("rss/images/F/2")
       os.mkdir("rss/images/F/3")

    #Se realizan las graficas de disperson
    for columna in range(0,len(colums_graficar)-1):
        #print(f"El rango va a ser : {columna+1} : {len(colums_graficar)-1}")
        
        for grafica in range(columna+1,len(colums_graficar)):
            plt.scatter(df[colums_graficar[columna]],df[colums_graficar[grafica]],alpha = 0.4)
            plt.xlabel(colums_graficar[columna])
            plt.ylabel(colums_graficar[grafica])
            if(os.path.exists(f"{pathe}/0/{chr(ord('A') + letra)}.svg")):
                os.remove(f"{pathe}/0/{chr(ord('A') + letra)}.svg")
            plt.savefig(f"{pathe}/0/{chr(ord('A') + letra)}.svg", bbox_inches='tight',format="svg")
            plt.clf()
            #plt.savefig(f"{pathe}/0/{chr(ord('a') + letra).upper}.svg", bbox_inches='tight')
            letra += 1
    if pathe.endswith("F"):
        for colunma in colums_graficar:
            plt.scatter(df["DAYS_IN_ORBIT"],df[colunma],alpha = 0.4)
            plt.xlabel("DAYS_IN_ORBIT")
            plt.ylabel(colunma)
            if(os.path.exists(f"{pathe}/0/{chr(ord('A') + letra)}.svg")):
                os.remove(f"{pathe}/0/{chr(ord('A') + letra)}.svg")
            plt.savefig(f"{pathe}/0/{chr(ord('A') + letra)}.svg", bbox_inches='tight',format="svg")
            plt.clf()
            letra += 1
        colums_graficar.append("DAYS_IN_ORBIT")
    letra = 0

    #se realizan las graficas de Distribución
    for columna in colums_graficar:
        df_n = df.groupby('RCS_SIZE')[columna].median().reset_index()
        plt.bar(df_n['RCS_SIZE'] ,height = df_n[columna] ,edgecolor='black') 
        plt.xlabel('RCS_SIZE')
        plt.ylabel(columna)  
        if(os.path.exists(f"{pathe}/1/{chr(ord('A') + letra)}.svg")):
            os.remove(f"{pathe}/1/{chr(ord('A') + letra)}.svg")
        plt.savefig(f"{pathe}/1/{chr(ord('A') + letra)}.svg", bbox_inches='tight',format="svg")
        plt.clf() 
        letra += 1
    
    letra = 0
    
    #Se realiza el grafico circular
    rcs_size_counts = df['RCS_SIZE'].value_counts()
    plt.pie(rcs_size_counts, labels=rcs_size_counts.index, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    if(os.path.exists(f"{pathe}/2/{chr(ord('A') + letra)}.svg")):
        os.remove(f"{pathe}/2/{chr(ord('A') + letra)}.svg")
    plt.savefig(f"{pathe}/2/{chr(ord('A') + letra)}.svg", bbox_inches='tight',format="svg")
    plt.clf() 

    #Se realiza el histograma 
    for columna in colums_graficar:
        plt.hist(df[columna],edgecolor='black')
        plt.xlabel(columna)
        plt.ylabel("Frecuencia")  
        if(os.path.exists(f"{pathe}/3/{chr(ord('A') + letra)}.svg")):
            os.remove(f"{pathe}/3/{chr(ord('A') + letra)}.svg")
        plt.savefig(f"{pathe}/3/{chr(ord('A') + letra)}.svg", bbox_inches='tight',format="svg")
        plt.clf() 
        letra += 1

    with open("rss/filesjson/detalles-imagenes.json","w") as archivo:
         datos = {"date":datetime.now().strftime("%Y%m%d"),"type":"NEW"}
         json.dump(datos,archivo)