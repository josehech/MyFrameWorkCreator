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
    if option == 999:
        showTools(fname, ttypes, type)
    selectedcommand = commandsoptions[option]
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
    c.execute('SELECT * FROM '+args['bbdd']+' WHERE (tooltype=? AND toolname=? AND command=?)', (type, tool, selectedcommand))
    entry = c.fetchone()
    if entry is None:
        commandoutput = os.system(selectedcommand + ' 2>&1 | tee ./output.txt')
        with open("./output.txt", "r") as outputfile:
            terminaltext = outputfile.read()
        c.execute("INSERT INTO "+args['bbdd']+" VALUES (?, ?, ?, ?)", (type,tool,selectedcommand,str(terminaltext)))
        bbdd.commit()
    else:
        if args['recheck']:
            commandoutput = os.system(selectedcommand + ' 2>&1 | tee ./output.txt')
            with open("./output.txt", "r") as outputfile:
                terminaltext = outputfile.read()
            c.execute('DELETE FROM '+args['bbdd']+' WHERE (tooltype=? AND toolname=? AND command=?)', (type, tool, selectedcommand))
            bbdd.commit()
            c.execute("INSERT INTO "+args['bbdd']+" VALUES (?, ?, ?, ?)", (type, tool, selectedcommand, str(terminaltext)))
            bbdd.commit()
        else:
            commandoutput = 0
            sys.stdout.write(warningcolor)
            print('Se ha encontrado una ejecución previa en la BBDD')

    sys.stdout.write(messagecolor)
    print()
    if commandoutput == 0:
        input("La ejecución ha finalizado. Comprueba la salida y pulsa Enter para continuar : ")
    else:
        sys.stdout.write(warningcolor)
        input("La ejecución ha finalizado con una salida inesperada, compruebala y pulsa Enter para continuar : ")
    sys.stdout.write(primary)
    showCommands(fname, ttypes, type,tool)


def showTools(fname, ttypes, type):
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
    if option == 999:
        executeFramework(fname, ttypes)
    selectedtool = toolsoptions[option]
    showCommands(fname, ttypes,type, selectedtool)


def executeFramework(fname,ttypes):
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
    if option == 999:
        c.close()
        bbdd.close()        
        exit(0)
    selectedtype = typeoptions[option]
    showTools(fname,ttypes,selectedtype)

if __name__== "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--bbdd', default='testing')
    parser.add_argument('-r', '--recheck', action='store_true')
    args = vars(parser.parse_args())
    print(args['bbdd'])
    print(args['recheck'])
    print('HOLA')
    #BBDD
    bbdd = dbapi.connect("bbdd.dat")
    c = bbdd.cursor()
    c.execute("create table if not exists "+args['bbdd']+" (tooltype text, toolname text, command text, result text)")
    
    # use the parse() function to load and parse an XML file
    doc = ET.parse("tools.xml")
    root = doc.getroot()
    ToolTypes = dict()
    #name
    frameworkname = root.find("./frameworkproperties/frameworkname").text
    #style
    if root.find("./frameworkproperties/style") is None:
        style = 'standard'    
    else:
        style = root.find("./frameworkproperties/style").text

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
            ToolTypes[type.text][programname.text].append((commands.text,commands.attrib))
    #colors
    primary = "\033[1;34m"
    inputcolor = "\033[1;32m"
    messagecolor = "\033[1;33m"
    warningcolor = "\033[1;31m"
    execolor = "\033[1;35m"
    try:
        sys.stdout.write(primary)
        executeFramework(frameworkname, ToolTypes)
    except KeyboardInterrupt:
        print()
        sys.stdout.write(warningcolor)
        print("OK. Saliendo...")
        c.close()
        bbdd.close()
        sys.exit()
    except EOFError:
        print()
        sys.stdout.write(warningcolor)
        print("OK. Saliendo...")
        c.close()
        bbdd.close()
        sys.exit()
