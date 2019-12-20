import xml.etree.ElementTree as ET
import re
import os

# use the parse() function to load and parse an XML file
doc = ET.parse("luxpr3.xml")
root = doc.getroot()
ToolTypes = dict()
frameworkname = root.find("./frameworkname")
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
        ToolTypes[type.text][programname.text].append(commands.text)


def showCommands(fname, ttypes, type, tool):
    os.system("clear")
    print("%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%")
    print("|                                                 |")
    print("|                                                 |")
    print("|                   MY FRAMEWORK                  |")
    print("|                                                 |")
    print("|                                                 |")
    print("%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%")
    print()
    ncommands = 1
    commandsoptions = dict()
    for command in ttypes[type][tool]:
        commandsoptions[ncommands] = command
        print("[" + str(ncommands) + "]", command)
        ncommands+=1
    print()
    print("[999] Volver")
    print()
    while True:
        option = int(input("Escoge el comando : "))
        if 0 < option < ncommands or option == 999:
            break
        else:
            print("Error : Opción no válida")
    if option == 999:
        showTools(fname, ttypes, type)
    selectedcommand = commandsoptions[option]
    print(selectedcommand)
    allmatches = re.findall(r"\[[^\]]+\]", selectedcommand)
    for match in allmatches:
        start=selectedcommand.find(match)
        end=start+len(match)
        variable=str(input("Indica el valor de la variable "+match[1:-1]+" : "))
        selectedcommand = selectedcommand[:start]+variable+selectedcommand[end:]
    print(selectedcommand)
    os.system(selectedcommand)
    input("Press Enter to continue : ")
    showTools(fname, ttypes, type)

def showTools(fname, ttypes, type):
    os.system("clear")
    print("%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%")
    print("|                                                 |")
    print("|                                                 |")
    print("|                   MY FRAMEWORK                  |")
    print("|                                                 |")
    print("|                                                 |")
    print("%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%")
    print()
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
        option = int(input("Escoge la herramienta a utilizar : "))
        if 0 < option < ntools or option == 999:
            break
        else:
            print("Error : Opción no válida")
    if option == 999:
        executeFramework(fname, ttypes)
    selectedtool = toolsoptions[option]
    showCommands(fname, ttypes,type, selectedtool)


def executeFramework(fname,ttypes):
    os.system("clear")
    print("%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%")
    print("|                                                 |")
    print("|                                                 |")
    print("|                   MY FRAMEWORK                  |")
    print("|                                                 |")
    print("|                                                 |")
    print("%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%")
    print()
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
        option = int(input("Escoge el tipo de herramienta : "))
        if 0 < option < ntypes or option == 999:
            break
        else:
            print("Error : Opción no válida")
    if option == 999:
        exit(0)
    selectedtype = typeoptions[option]
    showTools(fname,ttypes,selectedtype)

executeFramework(frameworkname, ToolTypes)
