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
  
 
     `43  #Introducir directorio de la carpeta`\
     `44  root = "C:/Users/jcmartinez/Desktop/Dashboard3"`
  
  
 
# 3.- Creación de ambiente virtual

 El primer paso es ingresar al directorio (carpeta que contiene los archivos)
  - En la barra inferior de inicio de windows teclear `cmd` en el ícono **buscar**.
  - Después teclearlos siguientes comandos:
    `cd Desktop`  y enter <break>
 
    `cd Dashboard` y enter <break>
 
     **Observación**
 
     Otra opción es introducir la ruta completa, p.e. `cd Desktop/Dashboard`. Note la dirección del ícono slash `/`, si copia la ruta desde la carpeta compruebe que sea la correcta en caso contrario realizar la sustitución manualmente.
Una vez que el directorio de la consola se encuentre dentro de la carpeta ejecutar los siguientes comandos, uno a la vez,  en consola (cmd para windown o bien en terminal de linux) 
 
1.- `conda update conda`, y enter
      
     Nota:
     Sólo si la consola devuelve 
     `ModuleNotFoundError: No module named 'conda'`
     Hay que hacer el siguiente paso extra, en caso contrario pasar al paso 2. El paso extra consiste en egragar conda a variables de entorno:
 
     # Agregar las siguientes líneas en la consola, una a la vez:
     # path de conda library
     SITE_PACKAGES=C:/Users/jcmartinez/Anaconda3/Library/bin/conda.bat
     # path del actual interprete de python
     PYTHON_BASE=C:/Users/jcmartinez/Anaconda3/python.exe
     
     Para hallar las ubicaciones de conda y python puede ayudarse de los siguientes comandos en consola: `where python`, `where conda`. 
 
2.- `conda create -n dashboard python=3.11.3`, y enter # crea el ambien virtual con nombre dashboard (se puede elegir cualquier otro nombre) 
 
3.- `conda activate dashboard` y enter (activa el ambiente virtual) <break> 
      `conda deactivate` # desactiva ambiente virtual 
      `conda env list`   # despliega lista de ambientes virtuales  

Cuando se va a ejecutar por primera vez, es necesario instalar las siguintes dependencias en línea de comandos con el ambiente virtual activado:

    conda install -c conda-forge pandas 
    conda install -c conda-forge numpy 
    conda install -c conda-forge dash 
    conda install -c conda-forge dash-table 
    conda install -c conda-forge plotly
    conda install -c conda-forge folium
    conda install -c conda-forge dash-mantine-components-0.12.1
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
    
    conda install -c conda-forge dash-iconify==0.1.2
    pip install dash-iconify==0.1.2
    conda install -c conda-forge millify==0.1.1
    pip install dash-millify==0.1.1
    conda install -c conda-forge dash-extensions==0.1.13rc1
    conda install -c conda-forge dash-lazy-load==1.3.1

**Observación:** Si alguna dependencia no se puede inatalar mediante 'conda install -c conda-forge' probar con 'pip install' seguido de la dependencia
    
  


Una vez instaladas todas las dependencias ejecutamos el paso siguiente para desplegar el proyecto.
 
4.- `python index.py` y enter (cuando aparezca (dashboard) al inicio de la línea de comandos se ejcuta el index), p.e.

     (dashboard) C:\Users\jcmartinez\Desktop\Dashboard_v2>python index.py 
     En el ejemplo anterior, la carpeta que contiene 

# Fuentes de consulta

[icons](https://icon-sets.iconify.design/ic/baseline-edit-location-alt/)



# Proceso para ingreso a servidor

1.- Generar llaves públicas y privadas

- Abrir `cdm` 
- Ingresar el siguiente comando `ssh-keygen`
- Ingresar un nombre de archivo después de 
`Enter file in which to save the key (C:\Users\jcmartinez/.ssh/id_rsa):` 
- Después ingresar cualquier palabra (o enter):
`Enter passphrase (empty for no passphrase):`
- Nuevamente escribir la palabra anterior(o enter) 
`Enter same passphrase again:` 
- Una vez que aparezcan las siguientes líneas de código, las llaves ya se habrán generado <break>
  
      The key's randomart image is:
      +---[RSA 3072]----+
      |     +.o .       |
      |    . + o        |
      | . .     . .     |
      |  o      .o.o    |
      |   ..   S..o.o   |
      |o E  o...+  ..o  |
      |.o  . =++.   =+. |
      |     o.++ +.= o=o|
      |      .o +.=oo+B=|
      +----[SHA256]-----+


- La llave pública comienza con:
 `ssh-rsa ... `

- Abrir el cmd en windows posicionarse en la carpeta de la llave pública (en mi caso tiene el nombre keys.ppk) e ingresar el siguiente comando (el local no se pone pormotivos de seguridad, habrá que sustituirlo):

  `ssh -i .\keys.ppk ubuntu@localhost`

# Descargar archivos del dashboard

- Primero hay que ingresar al servidor
- Crear una  carpeta, p.e. `Desktop` e ingresar a ella:
  - cd home
  - mkdir Desktop (mkdir crea carpeta)
  - cd Desktop
     
- sudo apt update
- sudo apt install git
- git --version

- git init
- git clone `https://github.com/SESNA-Inteligencia/Dashboard-1_1.git`

Si haz seguido los pasos correctamente hasta aquí, en la carpeta `Desktop` se deben haber descargado todos los archivos del repositorio remoto `GitHub` en la carpeta `/Dashboard-1_1`.

- Finalmente ingresar a la carpeta `/Dashboard-1_1`
- obtener la ruta de la carpeta con el siguiente comando en consola:
   `(dashboard2) ubuntu@sesna-mex-proyectosria01:~/Desktop/ProyectoDash/Dashboard-1_1$ pwd`
  `/home/ubuntu/Desktop/ProyectoDash/Dashboard-1_1`
  
- Copiar la ruta  `/home/ubuntu/Desktop/ProyectoDash/Dashboard-1_1` (ctr + c)
- Acceder a la carpeta apps : `cd/apps`
- abrir el archivo segalmex.py : `vim segalmex.py` (vim permite abrir cualquier archivo y modificarlo si no lo reconoce ingresar sudo apt install vim)
- cambiar el root
  - ctr + i : para editar el archivo
  - click derecho (mouse) + pegar (ruta del directorio)
  - ctr + c (para cambiar opciones de vim)
  - :wq! (guardar cambios y salir)  

# Instalar Python 3.11.3 en Ubuntu 18.04

Ingresar a la carpeta de archivos temporales (tmp) e ingresar los comandos siguientes:

- sudo apt update
- sudo apt install build-essential software-properties-common libssl-dev libffi-dev python3-dev libgdbm-dev libc6-dev libbz2-dev libsqlite3-dev tk-dev libffi-dev zlib1g-dev -y
- sudo add-apt-repository ppa:deadsnakes/ppa
- wget https://www.python.org/ftp/python/3.11.3/Python-3.11.3.tgz
- md5dsum Python-3.11.3.tgz 
- tar  -xvf Python-3.11.3.tgz (extrae el archivo .tar)
-  cd Python-3.11.3/ (ingresar a la carpeta)
-  sudo ./configure --enable-optimizations (se revisan todas las dependencias e instala python3)
-  sudo make altinstall (instala binarios)
- python3.11 --version (verifica la versión instalada)


Ligas útiles:

- [How to Install Python 3 on Ubuntu 18.04](https://phoenixnap.com/kb/how-to-install-python-3-ubuntu)
- [Install Python3 From Source](https://www.cherryservers.com/blog/install-python-on-ubuntu)


# Crear ambiente virtual en servidor

Una vez instalado python creamos en la ruta `Desktop/Dashboard-1_1` el ambiente virtual, siguiendo los siguientes pasos:

- sudo pip install --upgrade pip
- sudo apt install python3-virtualenv (instala ambiente virtual)
- sudo python3 -m venv dashboard2 (crea ambiente virtual)
- source dashboard2/bin/activate (se activa el ambiente virtual)

Si el ambien virtual se activo de manera correcta deberá aparecer al inicio de la linea de comando en consola el nombre del ambiente virtual entre paréntesis:

      `(dashboard2) ubuntu@sesna-mex-proyectosria01:~/Desktop/ProyectoDash/Dashboard-1_1$ git clone https://github.com/SESNA-Inteligencia/Dashboard-1_1.git`

Una vez creado instalamos todas las dependencias (con el ambiente virtual activado) mediante:

    sudo pip install --upgrade pip
    
    pip install pandas 
    pip install numpy 
    pip install dash 
    pip install dash-table 
    pip install plotly
    pip install folium
    pip install dash-mantine-components
    pip install matplotlib
    pip install seaborn
    pip install dash-bootstrap-components
    pip install dash-leaflet
    pip install sqlalchemy 
    pip install datetime 
    pip install pymysql
    pip install requests
    pip install openpyxl
    pip install dash-iconify
    pip install millify
    pip install dash-extensions
    pip install dash-lazy-load


Ligas útiles:

- [Change the Python3 default version in Ubuntu
](https://unix.stackexchange.com/questions/410579/change-the-python3-default-version-in-ubuntu)
- [Switch Python Version in Ubuntu](https://tecadmin.net/how-to-switch-python-version-in-ubuntu-debian/)


# Acceder al ambiente virtual

- Aceder a la carpeta

  `ubuntu@sesna-mex-proyectosria01:~/Desktop/ProyectoDash/Dashboard-1_1$`

- activar el ambiente virtual:

 `source dashboard2/bin/activate` (dashboard2 es el nombre del ambiente virtual)

 - ejecutar el archivo index.py :

 `python index.py`

Si no hay error alguno se debe mostrar:

      Dash is running on http://127.0.0.1:8050/
      
       * Serving Flask app 'app'
       * Debug mode: off
      WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
       * Running on http://127.0.0.1:8050
      Press CTRL+C to quit


Listo!!!
