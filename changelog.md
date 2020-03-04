# v1.0
Añadido:
- fastmode
- Opción -3 para ejecutar por indices
- Opción para imprimir los datos de una tabla
- Fichero showbbdd.py
- Opcion para imprimir las tablas de la bbdd
- Fichero showtables.py
Modificado:
- Detección de Ctrl+C al insertar parámetros. Ahora vuelve a mostrar los comandos en lugar de salir del programa.
- Correciones de ortografía.
- Al existir una entrada en la BBDD y no tener recheck activado se pregunta si desea eliminar la entrada y volver a ejecutar.
- Bugs con opcion -1
Eliminado:

# v0.0.3a
Añadido:
- BBDD por defecto
- Argparse con los argumentos "-b" para bbdd y "-r" para recheck
- Salida de la ejecución guardada en la bbdd
- Argumento -c CONFIG, --config CONFIG
- Archivo de configuración personalizado
- Archivo requeriments.txt 
- Opcion -2 para ejecutar todos los comandos de una herramienta

Modificado:
- Al ejecutar un comando se vuelven a listar los comandos para la herramienta
- Si el comando ya existe en la bbdd y no esta activado el recheck, cancela la ejecución
- Mensajes al finalizar la ejecución (Se recomienda comprobar la salida siempre)
- Mensaje que indica la existencia de la opción recheck
- Opción -1 para volver

Eliminado:

# v0.0.2a
Añadido:

- Creación automática de Banners
- Tag "frameworkproperties"
- Tag "frameworkproperties/style"
- Posibilidad de poner comentarios a los comandos
- Mensajes de error más concretos
- Mensaje al comienzo y al finalizar la ejecución de un comando
- Reconoce Ctrl+C y Ctrl+D

Modificado:

- Mensajes con colores.
- Ahora la etiqueta frameworkname está dentro de frameworkproperties

Eliminado:
