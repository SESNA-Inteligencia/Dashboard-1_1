[![My Skills](https://skillicons.dev/icons?i=py,html,css,git,mysql,vscode)](https://skillicons.dev)

# 📁 **Proyecto : Dashboard - SESNA**



# Ejecución del proyecto

- Descargar el proyecto en local : **Desktop** <break> 
- Crear un ambiente virtual (PENDIENTE) <break>
- Intalar dependencias (PENDIENTE) <break> 
- Activar el ambiente virtual (PENDIENTE) <break> 
- Ejecutar index: 'python index.py' <break> 

 
# Estructura del Proyecto

El proyecto está estructurado de la siguiente manera:
 
     
    .
    ├── apps  
    |   ├── home.py  
    |   └── segalmex.py  
    ├── assets  
    |   ├── logo.svg  
    |   ├── Logotipo_blanco 
    |   └── Segalmex2.jpg  
    ├── datasets  
    |   ├── base_beneficiarios_dashboard_v2.csv 
    |   ├── base_prodAgricola_con_claves_inegi.xlsx 
    |   ├── base_centros_inegi.xlsx 
    |   └──  produccion_estados.csv 
    ├── scripts 
    |   ├── Base_beneficiarios_dashboard.ipynb 
    |   └──  Base_ProduccionAgricola_dashboard.ipynb 
    ├── app.py 
    ├── index.py  
    ├── costumFunctions.py 
    └──  Readme.md

 # 1.- Intalación de Python y otras dependencias
 
 - Descargar Python **versión 3.11.3** e instalarlo:  `https://www.python.org/downloads/` <break> 
 - Descargar e instalar Anaconda : `https://www.anaconda.com/download/` <break>
 - Descargar e instalar VSCode :  `https://code.visualstudio.com/ ` (Opcional)<break>
 - Descargar e instalar Git : `https://git-scm.com/downloads` <break>

# 2.- Clonar el proyecto a una carpeta en escritorio
 
- Crear una carpeta en escritorio p.e. "Dashboard" <break> 
- Click derecho en cualquier lugar dentro de la carpeta y seleccionar **"Git Bash Here"** <break> 
- En la consola de Git ingtroducir siguiente comandos: <break> 
  - `git init` <break> 
  - `git clone https://github.com/SESNA-Inteligencia/Dashboard-1_1.git` <break>
  - Esperar unos minutos a que descargue los archivos en la carpeta
  - Una vez descargados los archivos, entrar a la carpeta y abrir el archivo `segalmex.py` en la siguiente ruta `segalmex.py` en VSCode o bien o en anaconda.
  - Abierto el archivo `segalmex.py`  agregar la ruta de la carpeta del proyecto en la variable `root` guardar cambios y cerrar.
  
 
     
     - introducir directorio de la carpeta
     - root = "C:/Users/jcmartinez/Desktop/Dashboard3"
  
  
 

# 3.- Creación de ambiente virtual

 El primer paso es ingresar al directorio (carpeta que contiene los archivos)
  - En la barra inferior de inicio de windows teclear `cmd` en el ícono **buscar**.
  - Después teclearlos siguientes comandos:
    `cd Desktop`  y enter <break>
    `cd Dashboard` y enter <break>
    
 
Una vez que el directorio de la consola se encuentre dentro de la carpeta ejecutar los siguientes comandos, uno a la vez,  en consola (cmd para windown o bien en terminal de linux) 
 
1.- `conda update conda`, y enter
 
2.- `conda create -n segalmex python=3.11.3`, y enter# crea el ambien virtual con nombre segalmex (se puede elegir cualquier otro nombre) 
 
3.- `conda activate segalmex` y enter (activa el ambiente virtual) 

Cuando se va a ejecutar por primera vez, es necesario instalar las siguintes dependencias en línea de comandos con el ambiente virtual activado:
 
    conda install -c conda-forge pandas 
    conda install -c conda-forge numpy 
    conda install -c conda-forge dash 
    conda install -c conda-forge dash-table 
    conda install -c conda-forge plotly
    conda install -c conda-forge folium
    conda install -c conda-forge dash-mantine-components
    conda install -c conda-forge matplotlib
    conda install -c conda-forge seaborn
    conda install -c conda-forge dash-bootstrap-components
    conda install -c conda-forge dash-leaflet
    conda install -c conda-forge sqlalchemy 
    conda install -c conda-forge datetime 
    conda install -c conda-forge pymysql
    conda install -c conda-forge requests
    conda install -c conda-forge openpyxl
    conda config --add channels conda-forge
    conda config --set channel_priority strict
    conda install zstandard
    conda install -c conda-forge install zstandard
    pip install dash-mantine-components==0.12.1

Una vez instaladas todas las dependencias ejecutamos el paso siguiente para desplegar el proyecto.
 
4.- `python index.py` y enter (cuando aparezca (segalmex) al inicio de la línea de comandos se ejcuta el index), p.e.
 
     (segalmex) C:\Users\jcmartinez\Desktop\Dashboard_v2>python index.py 
 
     En el ejemplo anterior, la carpeta que contiene 
