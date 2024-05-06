# API de SPACE MINIG
API en desarrollo para la aplicación de SPACE MINIG (proyecto alojado en el repositorio [SpaceMiningApp](https://github.com/codeuler/SpaceMiningApp.git))

![](https://github.com/MarcosDPG/space-mining-api/assets/127441963/6ae15b37-9986-41a5-9198-2e0bebb218ef)

## Descripción
Esta API proporciona funcionalidades para interactuar con la aplicación SPACE MINIG. Permite realizar consultas, obtener datos relacionados con el espacio y generar imágenes para su análisis.
#### Arquitectura y Flujo de Datos
La arquitectura de la API se basa en el framework Flask para Python, que actúa como el motor principal para gestionar las solicitudes HTTP y las respuestas correspondientes. Al recibir una solicitud, Flask dirige la ejecución hacia diferentes módulos especializados, cada uno dedicado a tareas específicas como web scraping, extracción de datos, generación de imágenes y más.

#### Web Scraping y Extracción de Datos
Para obtener información actualizada y precisa sobre conceptos espaciales y satélites, la API utiliza la biblioteca BeautifulSoup para realizar web scraping de páginas web específicas, como la plataforma Space-Track. Esta técnica permite extraer datos estructurados de manera automatizada, los cuales son luego procesados y almacenados para su posterior uso en la API.

#### Traducción Automática y Internacionalización de Datos
Con el fin de internacionalizar los datos y hacer que la API sea más accesible para usuarios de diferentes idiomas, se ha integrado la API de traducción automática DeepL Translator. Esto permite traducir de manera automática ciertos datos y mensajes generados por la API, ampliando así su alcance y utilidad para una audiencia global.

#### Actualización Automática y Hilos (Threads)
La API implementa un sistema de actualización automática para garantizar que los datos estén siempre actualizados y precisos. Para lograr esto sin afectar el rendimiento, se utilizan hilos (threads) para ejecutar tareas en segundo plano, como la actualización de imágenes y la obtención de datos frescos desde fuentes externas como Space-Track. Esta técnica asegura una experiencia fluida para los usuarios mientras se mantienen los datos actualizados de manera constante.

#### Generación de Imágenes y Análisis Visual
Uno de los puntos destacados de la API es su capacidad para generar imágenes gráficas a partir de los datos obtenidos. Estas imágenes son herramientas poderosas para el análisis visual y la representación de tendencias y patrones relacionados con el espacio.

#### Seguridad, Escalabilidad y Mantenimiento
La API se ha diseñado teniendo en cuenta consideraciones importantes de seguridad, asegurando la integridad y confidencialidad de los datos manejados. Además, se ha implementado con la escalabilidad en mente, permitiendo un crecimiento sostenible a medida que aumenta la demanda y la complejidad de las funcionalidades.

## Tecnologías Destacadas
- **Flask**: Framework de desarrollo web para Python.
- **BeautifulSoup**: Biblioteca para web scraping y extracción de datos de páginas web.
- **DeepL Translator API**: API de traducción automática para la internacionalización de datos.
- **API de Space-Track**: Utilizada para obtener datos precisos sobre conceptos espaciales y satélites, ademas de ser la fuente de datos para las graficas (imagenes).
- **Threads (hilos)**: Utilizados para ejecutar tareas en segundo plano como la actualización de imágenes.
- **Requests**: Biblioteca para realizar solicitudes HTTP a otras APIs y fuentes de datos.
- **JSON**: Formato utilizado para el intercambio de datos entre la API y los clientes.

## Instalación
1. Clona este repositorio en tu máquina local.
2. Instala las dependencias necesarias ejecutando pip install -r requirements.txt.
3. Configura las variables de entorno según sea necesario.
    - **AUTH_KEY**: llave de deepl para realizar traducciones
    - **USERNAME_SPACE_TRACK**: Correo usado para iniciar sesion en space-track
    - **PASSWORD_SPACE_TRACK**: Contraseña del correo anterior
4. Ejecuta el script main.py con python para verificar que todo funcione correctamente.

## Uso

### Endpoints

- **Principales**

    - **/**: Proporciona un mensaje anunciando la disponibilidad de la API.
    - **/data/conceptos/space_track**: Proporciona datos sobre conceptos espaciales desde Space Track.
        - **Parametros de consulta**:
            - **tipo** (opcional): al enviar "FORZAR" en este parametro, se obligara al servidor a actualizar los conceptos.

            Ejemplo:

                /data/conceptos/space_track?tipo=forzar
    - **/data/images/get**: Permite obtener imágenes específicas.
        - **Parametros de consulta**:
            - **orbita**: Especifica si la imagen que se desea obtener es de los satelites que se encuentran en orbita (t) o no (f).
            - **grafico**: Define el tipo de grafico que se desea visualizar, dentro de ellos se encuentra dispersion (0), distribución (1), circular(2) y histograma (3)
            - **ejes**: Indica que par de atributos se desean ubicar dentro de los ejes x e y, para ser graficados. En algunos casos como los son el circular y los histogramas, solo se puede elegir un atributo

            [T] Orbit
            
            [F] No in orbit: * (* indica que solo pertenecen a este tipo)

            [0]Dispersión:

                [A]Apogee Period
                [B]Apogee Perigee
                [C]Apogee Inclination
                [D]Period Perigee
                [E]Period Inclination
                [F]Perigee Inclination
                [G]Days_in_Orbit Apogee *
                [H]Days_in_Orbit Period *
                [I]Days_in_Orbit Perigee *
                [J]Days_in_Orbit Inclination *
            [1]Distribución:

                [A]RCS_SIZE - Apogee
                [B]RCS_SIZE - Period
                [C]RCS_SIZE - Perigee
                [D]RCS_SIZE - Inclination
                [E]RCS_SIZE - Days in Orbit *
            [2]Circular:

                [A]RCS_SIZE
            [3]Histograma:

                [A]Apogee
                [B]Period
                [C]Preigee
                [D]Inclination
                [E]Days in orbit *

            Ejemplo:

                    /data/images/get?orbita=t&grafico=0&ejes=a
    - **/data/files/apk/\<file>**: Permite obtener un archivo APK específico.
        - **Parametros de ruta**:
            - **file**: se debe poner el nombre del archivo alojado en el servidor, 
            
            Ejemplo:

                /data/files/apk/space-mining.apk
- **Actualizacion de datos**
    - **/data/images/update**: Actualiza las imágenes generadas.
    - **/data/update**: Forza la actualización de los archivos CSV y las imágenes.
    - **/data/csv/update_files**: Forza la actualización de los archivos CSV.
- **Gestion de archivos**
    - **/data/files/\<type>/\<file>**: Permite obtener archivos según el tipo y nombre de archivo especificados.
        - **Parametros de ruta**:
            - **type**: la extención del archivo que quieres obtener. (csv, json)
            - **file**: el nombre del archivo que quieres obtener.

                Ejemplo:
                
                    /data/files/csv/data-in-orbit.csv
    - **/data/files/rows/\<n_rows>/\<csv>**: Permite obtener un archivo JSON con un número específico de filas desde un archivo CSV, las filas seleccionadas son aleatorias.
        - **Parametros de ruta**:
            - **n_rows**: el numero de filas que quieres obtener.
            - **csv**: el nombre del archivo fuente.

                ejemplo:
                
                    /data/files/rows/2/data-in-orbit.csv

## Estructura del Proyecto
- **main.py**: Contiene la lógica principal de la API.
- **scraping.py**: Módulo para la obtención de datos de conceptos relacionados con el espacio desde **Space Track**
- **extractData.py**: Módulo para la extracción y limpieza de datos desde Space Track.
- **buildImages.py**: Módulo para la generación de imágenes.
- Otros archivos y directorios son utilizados para almacenar datos y configuraciones.

## Contacto
Puedes contactar al equipo de desarrollo en caso de dudas:

Correo electrónico: 
 - marcosd.parrag@utadeo.edu.co
 - eulerd.ostosc@utadeo.edu.co
