import sys
import xml.etree.ElementTree as ET
import re
import os
import sqlite3 as dbapi
import argparse
from pyfiglet import Figlet


def showBanner():
    custom_fig = Figlet(font=style)
    ascii_banner = custom_fig.renderText(frameworkname)
    print(ascii_banner)
    print()


def showCommands(fname, ttypes, type, tool):
    # Muestra los comandos disponibles
    os.system("clear")
    showBanner()
    ncommands = 1
    commandsoptions = dict()
    for command in ttypes[type][tool]:
        commandsoptions[ncommands] = command[0]
        if 'comment' in command[1]:
            print("[" + str(ncommands) + "]", command[0], '\t'+command[1]['comment'])
        else:
            print("[" + str(ncommands) + "]", command[0])
        ncommands += 1
    print()
    print("[999] Volver")
    print()

    # Escoger el comando (hasta que llegue una entrada válida)
    while True:
        try:
            sys.stdout.write(inputcolor)
            option = int(input("Escoge el comando : "))
            sys.stdout.write(primary)
            if 0 < option < ncommands or option == 999:
                break
            else:
                sys.stdout.write(warningcolor)
                print("Error : Opción no válida")
                sys.stdout.write(primary)
        except ValueError:
            sys.stdout.write(warningcolor)
            print("Error : Opción no válida")
            sys.stdout.write(primary)

    # Si es 999 volver a la pantalla anterior
    if option == 999:
        showTools(fname, ttypes, type)

    # Guardar la opción seleccionada
    selectedcommand = commandsoptions[option]

    # Sustituir todos los parámetros del comando
    allmatches = re.findall(r"\[[^\]]+\]", selectedcommand)
    for match in allmatches:
        start=selectedcommand.find(match)
        end=start+len(match)
        sys.stdout.write(inputcolor)
        variable=str(input("Indica el valor de la variable "+match[1:-1]+" : "))
        sys.stdout.write(primary)
        selectedcommand = selectedcommand[:start]+variable+selectedcommand[end:]
    print()
    sys.stdout.write(messagecolor)
    print("Ejecutando : ",selectedcommand)
    sys.stdout.write(execolor)
    print()

    # Comprobar si existe una ejecución previa en la BBDD
    c.execute('SELECT * FROM '+args['table']+' WHERE (tooltype=? AND toolname=? AND command=?)', (type, tool, selectedcommand))
    entry = c.fetchone()

    # Si no existe, ejecutar el comando, guardarlo en output.txt y guardar la ejecución en la BBDD
    if entry is None:
        commandoutput = os.system(selectedcommand + ' 2>&1 | tee ./output.txt')
        with open("./output.txt", "r") as outputfile:
            terminaltext = outputfile.read()
        c.execute("INSERT INTO "+args['table']+" VALUES (?, ?, ?, ?)", (type,tool,selectedcommand,str(terminaltext)))
        bbdd.commit()
    else:
        # Si existe y está activado el flag --recheck, ejecutar el comando y actualizar la salida en la BBDD.
        if args['recheck']:
            commandoutput = os.system(selectedcommand + ' 2>&1 | tee ./output.txt')
            with open("./output.txt", "r") as outputfile:
                terminaltext = outputfile.read()
            c.execute('DELETE FROM '+args['table']+' WHERE (tooltype=? AND toolname=? AND command=?)', (type, tool, selectedcommand))
            bbdd.commit()
            c.execute("INSERT INTO "+args['table']+" VALUES (?, ?, ?, ?)", (type, tool, selectedcommand, str(terminaltext)))
            bbdd.commit()
        # Si existe y no está activado el flag --recheck, escapar la ejecución e imprimir la salida guardada.
        else:
            commandoutput = 0
            sys.stdout.write(warningcolor)
            print('Se ha encontrado una ejecución previa en la BBDD. La salida ha sido la siguiente:')
            sys.stdout.write(execolor)
            print(entry[3])
            sys.stdout.write(messagecolor)
            print('Para volver a ejecutar el comando utiliza la opción -r o --recheck al ejecutar MyFrameworkName.py')

    # Comprobar si hubo un error al ejecutar el comando
    sys.stdout.write(messagecolor)
    print()
    if commandoutput == 0:
        input("La ejecución ha finalizado. Comprueba la salida y pulsa Enter para continuar : ")
    else:
        sys.stdout.write(warningcolor)
        input("[!] La ejecución ha finalizado con una salida inesperada, compruebala y pulsa Enter para continuar : ")

    # Mostrar los comandos al acabar la ejecución
    sys.stdout.write(primary)
    showCommands(fname, ttypes, type,tool)


def showTools(fname, ttypes, type):
    # Muestra las herramientas que pertenecen al tipo "type"
    os.system("clear")
    showBanner()
    ntools = 1
    toolsoptions = dict()
    for tool in ttypes[type].keys():
        toolsoptions[ntools] = tool
        print("[" + str(ntools) + "]", tool)
        ntools += 1
    print()
    print("[999] Volver")
    print()

    # Escoger la herramienta (hasta que llegue una entrada válida)
    while True:
        try:
            sys.stdout.write(inputcolor)
            option = int(input("Escoge la herramienta a utilizar : "))
            sys.stdout.write(primary)
            if 0 < option < ntools or option == 999:
                break
            else:
                sys.stdout.write(warningcolor)
                print("Error : Opción no válida")
                sys.stdout.write(primary)
        except ValueError:
            sys.stdout.write(warningcolor)
            print("Error : Opción no válida")
            sys.stdout.write(primary)

    # Si es 999 ir a la pantalla anterior
    if option == 999:
        executeFramework(fname, ttypes)

    # Guarda la opción seleccionada
    selectedtool = toolsoptions[option]
    showCommands(fname, ttypes,type, selectedtool)


def executeFramework(fname,ttypes):
    # Muestra los ToolTypes
    os.system("clear")
    showBanner()
    ntypes = 1
    typeoptions = dict()
    for type in ttypes.keys():
        typeoptions[ntypes] = type
        print("[" + str(ntypes) + "]", type)
        ntypes += 1
    print()
    print("[999] Salir")
    print()

    # Escoger el tipo de herramienta (hasta que llegue una entrada válida)
    while True:
        try:
            sys.stdout.write(inputcolor)
            option = int(input("Escoge el tipo de herramienta : "))
            sys.stdout.write(primary)
            if 0 < option < ntypes or option == 999:
                break
            else:
                sys.stdout.write(warningcolor)
                print("Error : Opción no válida")
                sys.stdout.write(primary)
        except ValueError:
            sys.stdout.write(warningcolor)
            print("Error : Opción no válida")
            sys.stdout.write(primary)

    # Si es 999 salir
    if option == 999:
        c.close()
        bbdd.close()        
        exit(0)

    # Guarda la opción seleccionada
    selectedtype = typeoptions[option]
    showTools(fname,ttypes,selectedtype)


if __name__== "__main__":
    # Argument Parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--table', default='testing')
    parser.add_argument('-r', '--recheck', action='store_true')
    args = vars(parser.parse_args())

    # Fichero conf.txt
    configuracion = dict()
    try:
        conf = open("config.txt")
        linea = conf.readline()
        while linea:
            if len(linea) != 0:
                splited = str(linea).split("=", 1)
                if len(splited) != 2:
                    print("Error en el archivo de configuración")
                    exit(1)
                param = splited[0].strip()
                val = splited[1].strip()
                configuracion[param] = val
            linea = conf.readline()
        conf.close()
    except IOError:
        print("Fichero de configuración (conf.txt) no encontrado")
        input("Pulsa Enter para continuar sin el archivo de configuración : ")

    # BBDD
    bbdd = dbapi.connect("bbdd.dat")
    c = bbdd.cursor()
    c.execute("create table if not exists "+args['table']+" (tooltype text, toolname text, command text, result text)")
    
    # XML Parser
    doc = ET.parse("tools.xml")
    root = doc.getroot()
    ToolTypes = dict()

    # Nombre
    frameworkname = root.find("./frameworkproperties/frameworkname").text

    # Estilo
    if root.find("./frameworkproperties/style") is None:
        style = 'standard'    
    else:
        style = root.find("./frameworkproperties/style").text

    # Almacenamiento en ToolTypes y gestión de errores en fichero XML
    for tool in root.findall("./tool"):
        type = tool.find("./tooltype")
        if type is None:
            print("Error : Todas las Tools deben tener la etiqueta 'tooltype'")
            exit(1)
        if type.text not in ToolTypes:
            ToolTypes[type.text] = dict()
        programname = tool.find("./programname")
        if programname is None:
            print("Error : Todas las Tools deben tener la etiqueta 'programname'")
            exit(1)
        if programname.text not in ToolTypes[type.text]:
            ToolTypes[type.text][programname.text] = []
        for commands in tool.findall("./command"):
            ToolTypes[type.text][programname.text].append((commands.text, commands.attrib))

    # Colores
    primary = "\033[1;34m"
    inputcolor = "\033[1;32m"
    messagecolor = "\033[1;33m"
    warningcolor = "\033[1;31m"
    execolor = "\033[1;35m"

    # Gestión de excepciones
    try:
        sys.stdout.write(primary)
        executeFramework(frameworkname, ToolTypes)
    except KeyboardInterrupt:
        # Ctrl + C
        print()
        sys.stdout.write(warningcolor)
        print("OK. Saliendo...")
        c.close()
        bbdd.close()
        sys.exit()
    except EOFError:
        # Ctrl + D
        print()
        sys.stdout.write(warningcolor)
        print("OK. Saliendo...")
        c.close()
        bbdd.close()
        sys.exit()
