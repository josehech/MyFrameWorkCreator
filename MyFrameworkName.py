import sys
import xml.etree.ElementTree as ET
import re
import os
import sqlite3 as dbapi
import argparse
import readline
from pyfiglet import Figlet

def showBanner():
    custom_fig = Figlet(font=style)
    ascii_banner = custom_fig.renderText(frameworkname)
    print(ascii_banner)
    print()

def executeCommand(ttypes, type, tool, selectedcommand):
    sys.stdout.write(inputcolor)
    print('Comando seleccionado :',selectedcommand)
    # Sustituir todos los parámetros del comando
    allmatches = re.findall(r"\[[^\]]+\]", selectedcommand)
    for match in allmatches:
        start=selectedcommand.find(match)
        end=start+len(match)
        sys.stdout.write(inputcolor)
        if match[1:-1] not in configuracion.keys():
            variable=str(input("Indica el valor del parámetro "+match[1:-1]+" : "))
        else:
            print('Asignando el valor',str(configuracion[match[1:-1]]),'al parámetro',match[1:-1])
            variable = configuracion[match[1:-1]]
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
            print('[!] Se ha encontrado una ejecución previa en la BBDD. La salida ha sido la siguiente:')
            sys.stdout.write(execolor)
            print(entry[3])
            rerun = str()
            if args['fastmode']:
                rerun = 'n'
            sys.stdout.write(inputcolor)
            while rerun == "":
                rerun = str(input('¿Quieres eliminar esta salida de la BBDD y volver a ejecutar el comando? (s/n) : '))
            sys.stdout.write(execolor)
            print()
            if rerun in ['s','S']:
                commandoutput = os.system(selectedcommand + ' 2>&1 | tee ./output.txt')
                with open("./output.txt", "r") as outputfile:
                    terminaltext = outputfile.read()
                c.execute('DELETE FROM '+args['table']+' WHERE (tooltype=? AND toolname=? AND command=?)', (type, tool, selectedcommand))
                bbdd.commit()
                c.execute("INSERT INTO "+args['table']+" VALUES (?, ?, ?, ?)", (type, tool, selectedcommand, str(terminaltext)))
                bbdd.commit()
            sys.stdout.write(messagecolor)
            print('Puedes utilizar la opción -r o --recheck para omitir la salida de la BBDD')
    os.system('rm ./output.txt 2>/dev/null')
    # Comprobar si hubo un error al ejecutar el comando
    print()
    if commandoutput != 0:
        sys.stdout.write(warningcolor)
        input("[!] La ejecución ha finalizado de forma inesperada, pulsa ENTER para continuar : ")

def showCommands(ttypes, type, tool):
    # Muestra los comandos disponibles
    os.system("clear")
    showBanner()
    ncommands = 1
    commandsoptions = dict()
    for command in ttypes[type][tool]:
        commandsoptions[ncommands] = command[0]
        if 'comment' in command[1]:
            print("[" + str(ncommands) + "]", command[0],end='')
            sys.stdout.write(messagecolor)
            print('\t'+command[1]['comment'])
            sys.stdout.write(primary)
        else:
            print("[" + str(ncommands) + "]", command[0])
        ncommands += 1
    print()
    print("[-1] Volver")
    print("[-2] Ejecutar todos")
    print("[-3] Ejecutar por índices")
    print()

    # Escoger el comando (hasta que llegue una entrada válida)
    while True:
        try:
            sys.stdout.write(inputcolor)
            option = int(input("Escoge el comando : "))
            sys.stdout.write(primary)
            if 0 < option < ncommands or option == -1 or option == -2 or option == -3:
                break
            else:
                sys.stdout.write(warningcolor)
                print("[!] Error : Opción no válida")
                sys.stdout.write(primary)
        except ValueError:
            sys.stdout.write(warningcolor)
            print("[!] Error : Opción no válida")
            sys.stdout.write(primary)
    try:
        # Si es -1 volver a la pantalla anterior
        if option == -1:
            return

        # Guardar la opción seleccionada
        elif option == -2:
            for number in range(1,ncommands):
                selectedcommand = commandsoptions[number]
                wantcontinue = str()
                if args['fastmode']:
                    wantcontinue = 's'
                while wantcontinue == "":
                    sys.stdout.write(inputcolor)
                    wantcontinue = input('¿Quieres ejecutar "'+selectedcommand+'" ?: ')
                if wantcontinue in ['s','S']:
                    executeCommand(ttypes, type, tool, selectedcommand)
        elif option == -3:
            lista_raw=input('Introduce los indices separados por un espacio (p.e:2 4 5 7): ')
            lista_numeros = [int(x) for x in lista_raw.split()]
            for number in lista_numeros:
                if 0 < number < ncommands:
                    selectedcommand = commandsoptions[number]
                    executeCommand(ttypes, type, tool, selectedcommand)
        else:
            selectedcommand = commandsoptions[option]
            executeCommand(ttypes, type, tool, selectedcommand)
        sys.stdout.write(warningcolor)
        input("[!] La ejecución ha finalizado. Comprueba la salida y pulsa ENTER para continuar : ")
    except KeyboardInterrupt:
        # Ctrl + C
        print()
        sys.stdout.write(warningcolor)
        input("[!] Cancelando ejecución. Pulsa ENTER para continuar...")
    except ValueError:
        sys.stdout.write(warningcolor)
        input("[!] Entrada no válida. Pulsa ENTER para continuar...")
    # Mostrar los comandos al acabar la ejecución
    sys.stdout.write(primary)
    showCommands(ttypes, type,tool)


def showTools(ttypes, type):
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
    print("[-1] Volver")
    print()

    # Escoger la herramienta (hasta que llegue una entrada válida)
    while True:
        try:
            sys.stdout.write(inputcolor)
            option = int(input("Escoge la herramienta a utilizar : "))
            sys.stdout.write(primary)
            if 0 < option < ntools or option == -1:
                break
            else:
                sys.stdout.write(warningcolor)
                print("[!] Error : Opción no válida")
                sys.stdout.write(primary)
        except ValueError:
            sys.stdout.write(warningcolor)
            print("[!] Error : Opción no válida")
            sys.stdout.write(primary)

    # Si es -1 ir a la pantalla anterior
    if option == -1:
        return

    # Guarda la opción seleccionada
    selectedtool = toolsoptions[option]
    showCommands(ttypes,type, selectedtool)
    showTools(ttypes,type)

def executeFramework(ttypes):
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
    print("[-1] Salir")
    print()

    # Escoger el tipo de herramienta (hasta que llegue una entrada válida)
    while True:
        try:
            sys.stdout.write(inputcolor)
            option = int(input("Escoge el tipo de herramienta : "))
            sys.stdout.write(primary)
            if 0 < option < ntypes or option == -1:
                break
            else:
                sys.stdout.write(warningcolor)
                print("[!] Error : Opción no válida")
                sys.stdout.write(primary)
        except ValueError:
            sys.stdout.write(warningcolor)
            print("[!] Error : Opción no válida")
            sys.stdout.write(primary)

    # Si es -1 salir
    if option == -1:
        return

    # Guarda la opción seleccionada
    selectedtype = typeoptions[option]
    showTools(ttypes,selectedtype)
    executeFramework(ttypes)

def printdata(tablename):
    # Colores
    red = "\033[1;31m"
    purple = "\033[1;35m"

    # BBDD
    bbdd = dbapi.connect("bbdd.dat")
    c = bbdd.cursor()
    c.execute('SELECT * FROM '+ tablename)
    entry = c.fetchall()
    for table in entry:
        sys.stdout.write(red)
        print(table[0:3])
        sys.stdout.write(purple)
        print(table[3])
    c.close()
    bbdd.close()
def printtables():
    # Colores
    green = "\033[1;32m"
    purple = "\033[1;35m"

    # BBDD
    bbdd = dbapi.connect("bbdd.dat")
    c = bbdd.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    sys.stdout.write(purple)
    for table in c.fetchall():
        print(table[0])
    c.close()
    bbdd.close()
if __name__== "__main__":
    # Argument Parser
    parser = argparse.ArgumentParser(description='ejemplo : python3 MyFrameworkName.py -t secondtable -c config_example.txt -r')
    parser.add_argument('-t', '--table', default='testing', help='Especifica el nombre de la tabla en la BBDD (por defecto = testing)')
    parser.add_argument('-r', '--recheck', action='store_true', help='Ejecuta el comando aunque haya una salida previa en la BBDD')
    parser.add_argument('-c', '--config', help='Especifica el archivo de configuración')
    parser.add_argument('-f', '--fastmode',action='store_true', help='Evita preguntas')
    parser.add_argument('-st', '--showtables', action='store_true', help='Muestra todas las tablas creadas en la BBDD.')
    parser.add_argument('-sb', '--showdata', help='Muestra los datos de la tabla especificada o testing si no se indica (ej. python3 <frameworkwname>.py --showdata <tablename>)')
    args = vars(parser.parse_args())
    
    if args['showdata'] != None:
        printdata(args['showdata'])
        sys.exit()
    if args['showtables']:
        printtables()
        sys.exit()
    # Fichero conf.txt
    configuracion = dict()
    if args['config'] != None:
        try:
            conf = open(args['config'])
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
            print("Fichero de configuración",args['config'],"no encontrado")
            input("Pulsa ENTER para continuar sin el archivo de configuración : ")
    
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
        executeFramework(ToolTypes)
    except KeyboardInterrupt:
        # Ctrl + C
        print()
        sys.stdout.write(warningcolor)
        print("[!] OK. Saliendo...")
    except EOFError:
        # Ctrl + D
        print()
        sys.stdout.write(warningcolor)
        print("[!] OK. Saliendo...")
    finally:
        c.close()
        bbdd.close()
        sys.exit()

