# FrameworkCreator
### Descripción
MyFrameWorkCreator es un script que permite crear nuestro propio entorno de trabajo (Framework) a partir de un archivo XML con un formato determinado.

### Formato tools.xml
~~~xml
<framework>
    <frameworkproperties>
        <frameworkname>MyFramework</frameworkname>
        <style>standard</style>
    </frameworkproperties>
    <tool>
        <tooltype>Headers Info</tooltype>
        <programname>Curl</programname>
        <command comment="#Imprime las cabeceras de la peticion">curl -X [METHOD] -I [URL]</command>
        <command comment="#Petición GET sin verificar los certificados HTTPS">curl -k -X GET [URL] </command>
    </tool>
</framework>
~~~
Las etiquetas y atributos son los siguientes:
- framework (obligatorio) : Contiene la descripcion del framework.
- frameworkproperties (obligatorio) : Contiene la descripcion de las propiedades del framework (de momento nombre y estilo del texto).
- framworkname (obligatorio) : Contiene el nombre del Framework.
- style (recomendado) : Indica el estilo del texto del banner.
- tool (obligatorio) : Contiene la descripcion de una herramienta.
- tooltype (obligatorio) : Indica la finalidad de la herramienta y de los comandos.
- programname (obligatorio) : Indica el nombre de la herramienta (puede repetirse si el tooltype es distinto).
- command (obligatorio) : Indica el comando que se va a ejecutar.
- comment (recomendado) : Añade un comentario al comando.

Dentro de un comando se especificará un parámetro como un string entre corchetes. Por ejemplo, para el comando 'curl -X [METHOD] -I [URL]', METHOD y URL son parámetros que el framework preguntará por su valor.

### Archivo de configuración por defecto
El archivo config_example.txt es un ejemplo de archivo de configuración de variables por defecto que indica que el valor de los parámetros definidos en él no deben ser preguntados por el framework. Por ejemplo, si dentro de este archivo se encuentra la asignación 'METHOD = GET' (sin comillas), el comando 'curl -X [METHOD] -I [URL]' sólo preguntará por el valor del parámetro URL. Para activar el uso del archivo de configuración se debe utilizar el argumento '--config config_example.txt'.

### Instalación
~~~sh
git clone https://github.com/josehech/MyFrameWorkCreator.git
cd MyFrameWorkCreator/
sudo apt-get install python3-pyfiglet
pip install -r requirements.txt
~~~

### Uso
1. Se crea un fichero XML con el formato que tiene el archivo tools.xml
2. Se ejecuta el script MyFrameworkName.py con python3
    ~~~
    python3 MyFrameworkName.py
    ~~~
![Inicio](./screenshot.png)
![Types](./screenshot_1.png)
![Tools](./screenshot_2.png)
![variables](./screenshot_3.png)
![Ejecucion](./screenshot_4.png)
### Opciones
~~~sh
-r , --recheck  #Flag que fuerza ejecutar los comandos aunque se encuentren en la BBDD (CUIDADO, borra los datos anteriores)
-t table_name , --table table_name  #Tabla que guardará los datos de los comandos ejecutados (por defecto testing)
-c config_file, --config_file   #Fichero que asigna valores por defecto a los parámetros
~~~
### Características
- [X] Banner personalizado
- [X] Estilo de Banner personalizado con pyfiglet
- [X] Guarda salida previas en BBDD
- [X] Múltiples tablas en BBDD
- [X] Opción para ver datos de una tabla
- [X] Opción para ver las tablas que alamacena la BBDD
- [X] Archivo de configuración
- [X] Reconocimiento de parámetros
- [X] Comentarios en los comandos
- [X] Distinción de mensajes por colores
- [X] Automatización de un conjunto de comandos
- [X] Ejecución por índices
