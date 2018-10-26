#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#Contiene funciones para manipular el archivo CSV con los offsets de la
#calibracion, se cumple el siguiente formato:
###------------------------------------------------------------------
#   Encabezado:          grado, TerminoN, TerminoN-1, ..., Termino1
#   Contenido:    Eje_Actuador,   ValorN,   ValorN-1,   ..., Valor1
###------------------------------------------------------------------
#Con N = grado + 1
##
#El archivo CSV con los offsets se sobreescribe cada vez que se hace una
#calibracion. Se guarda en el directorio .../Calibration/Offsets, bajo el nombre
#no alterable "offsets.csv".
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#Imports
import csv
import os
import time
from itertools import islice
from os.path import dirname, abspath

##Custom
import Error_Func as error

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#Lee archivo con los offsets y devuelve lista con el conjunto de terminos para
#cada actuador y el grado polinomial utilizado en la calibracion
def getOffsets(offsetsFile):
    print "Reading offsets values from default .../Calibration/Offsets/offsets.csv"
    #Root
    archivo = dirname(dirname(abspath(__file__)))
    archivo += "/Ver_Release/Calibration/Offsets/"+offsetsFile
    ##Abriendo archivo
    f = open(archivo, 'rt')
    ##Obteniendo datos completos y cerrando archivo
    reader = csv.reader(f)
    filas = [r for r in reader]
    f.close()
    #---------------------------------------------------------------------------
    ##Obtiene grado del polinomio
    polDegree = int(filas[0].pop(0))
    isRot = filas[0].pop(0)
    ##Borrando encabezado
    del filas[0]
    #---------------------------------------------------------------------------
    ##Cada elemento de "filas" incluye todos los terminos segun el grado polinomial
    ##por eje_actuador, segun el orden preferente (XYZ para ejes, RArm, RLeg,
    #LLeg, LArm, Torso, Head para actuadores; la lista es de 18 elementos)
    print "Got offsets"
    return filas,polDegree,isRot

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#Recibe grado polinomial usado y lista con grupos de terminos por eje_actuador,
#segun el orden preferente (XYZ para ejes, RArm, RLeg,#LLeg, LArm, Torso, Head
#para actuadores; la lista debe contener 18 elementos)
def writeOffsets(degree, eje_actuador, rotacion, ID):
    archivo = dirname(dirname(abspath(__file__)))
    archivo += "/Ver_Release/Calibration/Offsets/offsets_"+ID+".csv"
    with open(archivo, 'w') as csvfile:
        writer = csv.writer(csvfile)
        #Encabezado (solo importa el grado ya que el orden de los terminos se
        #considera siempre estaran bien)
        writer.writerow([degree, rotacion])
        for item in eje_actuador:
            for element in item:
                writer.writerow(element)
    return 0
