#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#Incluye funciones para la lectura del archivo CSV y ajuste a los datos de la
#grabacion del movimiento capturado en MoCap que se quiere ejecutar.
##
#Recibe los terminos del ajuste de calibracion del archivo CSV
#.../Cal/Offsets/offsets.csv. Devuelve listas con los actuadores y vectores de
#coordenadas y tiempos, Las coordenadas pueden ser obtenidas en los marcos de
#referencia ROBOT y TORSO, segun se solicite.
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#Imports
import csv
import os
from itertools import islice
from os.path import dirname, abspath
from copy import deepcopy

##Custom
import OffsetFile_Func as offset
import Error_Func as error

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#Globales
coordenadasArriba     = list()
coordenadasROBOT      = list()
coordenadasTORSO      = list()
coordenadasCompletas  = list()
listaTiemposROBOT     = list()
listaTiemposTORSO     = list()
listaTiemposArriba    = list()
listaTiemposCompletos = list()

#Inicia el procesamiento de los archivos CSV necesarios para el ajuste de datos
#Recibe como parametro el nombre del archivo CSV con las coordenadas a leer
def startAdjustData(nombreArchivo, offFile):
    print "++++++++++++++++++++++++++++++++++++++++++++++++++++"
    print "Starting coordinates adjustment for", nombreArchivo
    #Coeficientes de Ajuste para valores del MoCap, considerando relacion lineal
    #entre datos del MoCap y datos del Nao
    ##Lectura del archivo con los parametros
    try:
        listaOffsets,degree,rotacion = offset.getOffsets(offFile)
    except Exception,e:
        error.abort("Failed to get offsets from file offset.csv, check file", None, "CSVMOCAPFunc")

    #Sin rotaciones, solo X,Y,Z
    if rotacion.lower() == "no":
        offRArm  = [[] for x in range(3)]
        offRLeg  = [[] for x in range(3)]
        offLLeg  = [[] for x in range(3)]
        offLArm  = [[] for x in range(3)]
        offTorso = [[] for x in range(3)]
        offHead  = [[] for x in range(3)]


        #RArm
        for j in range(degree+1):
            offRArm[0].append(round(float(listaOffsets[0][j]),4))
            offRArm[1].append(round(float(listaOffsets[1][j]),4))
            offRArm[2].append(round(float(listaOffsets[2][j]),4))
        #RLeg
        for j in range(degree+1):
            offRLeg[0].append(round(float(listaOffsets[3][j]),4))
            offRLeg[1].append(round(float(listaOffsets[4][j]),4))
            offRLeg[2].append(round(float(listaOffsets[5][j]),4))
        #LLeg
        for j in range(degree+1):
            offLLeg[0].append(round(float(listaOffsets[6][j]),4))
            offLLeg[1].append(round(float(listaOffsets[7][j]),4))
            offLLeg[2].append(round(float(listaOffsets[8][j]),4))

        #LArm
        for j in range(degree+1):
            offLArm[0].append(round(float(listaOffsets[9][j]),4))
            offLArm[1].append(round(float(listaOffsets[10][j]),4))
            offLArm[2].append(round(float(listaOffsets[11][j]),4))

        #Torso
        for j in range(degree+1):
            offTorso[0].append(round(float(listaOffsets[12][j]),4))
            offTorso[1].append(round(float(listaOffsets[13][j]),4))
            offTorso[2].append(round(float(listaOffsets[14][j]),4))

        #Head
        for j in range(degree+1):
            offHead[0].append(round(float(listaOffsets[15][j]),4))
            offHead[1].append(round(float(listaOffsets[16][j]),4))
            offHead[2].append(round(float(listaOffsets[17][j]),4))

    #Con rotaciones, X,Y,Z,wX,wY,wZ
    elif rotacion.lower() == "yes":
        offRArm  = [[] for x in range(6)]
        offRLeg  = [[] for x in range(6)]
        offLLeg  = [[] for x in range(6)]
        offLArm  = [[] for x in range(6)]
        offTorso = [[] for x in range(6)]
        offHead  = [[] for x in range(6)]

        #RArm
        for j in range(degree+1):
            offRArm[0].append(round(float(listaOffsets[0][j]),4))
            offRArm[1].append(round(float(listaOffsets[1][j]),4))
            offRArm[2].append(round(float(listaOffsets[2][j]),4))
            offRArm[3].append(round(float(listaOffsets[3][j]),4))
            offRArm[4].append(round(float(listaOffsets[4][j]),4))
            offRArm[5].append(round(float(listaOffsets[5][j]),4))
        #RLeg
        for j in range(degree+1):
            offRLeg[0].append(round(float(listaOffsets[6][j]),4))
            offRLeg[1].append(round(float(listaOffsets[7][j]),4))
            offRLeg[2].append(round(float(listaOffsets[8][j]),4))
            offRLeg[3].append(round(float(listaOffsets[9][j]),4))
            offRLeg[4].append(round(float(listaOffsets[10][j]),4))
            offRLeg[5].append(round(float(listaOffsets[11][j]),4))
        #LLeg
        for j in range(degree+1):
            offLLeg[0].append(round(float(listaOffsets[12][j]),4))
            offLLeg[1].append(round(float(listaOffsets[13][j]),4))
            offLLeg[2].append(round(float(listaOffsets[14][j]),4))
            offLLeg[3].append(round(float(listaOffsets[15][j]),4))
            offLLeg[4].append(round(float(listaOffsets[16][j]),4))
            offLLeg[5].append(round(float(listaOffsets[17][j]),4))

        #LArm
        for j in range(degree+1):
            offLArm[0].append(round(float(listaOffsets[18][j]),4))
            offLArm[1].append(round(float(listaOffsets[19][j]),4))
            offLArm[2].append(round(float(listaOffsets[20][j]),4))
            offLArm[3].append(round(float(listaOffsets[21][j]),4))
            offLArm[4].append(round(float(listaOffsets[22][j]),4))
            offLArm[5].append(round(float(listaOffsets[23][j]),4))

        #Torso
        for j in range(degree+1):
            offTorso[0].append(round(float(listaOffsets[24][j]),4))
            offTorso[1].append(round(float(listaOffsets[25][j]),4))
            offTorso[2].append(round(float(listaOffsets[26][j]),4))
            offTorso[3].append(round(float(listaOffsets[27][j]),4))
            offTorso[4].append(round(float(listaOffsets[28][j]),4))
            offTorso[5].append(round(float(listaOffsets[29][j]),4))

        #Head
        for j in range(degree+1):
            offHead[0].append(round(float(listaOffsets[30][j]),4))
            offHead[1].append(round(float(listaOffsets[31][j]),4))
            offHead[2].append(round(float(listaOffsets[32][j]),4))
            offHead[3].append(round(float(listaOffsets[33][j]),4))
            offHead[4].append(round(float(listaOffsets[34][j]),4))
            offHead[5].append(round(float(listaOffsets[35][j]),4))
    else:
        error.abort("Expected \"yes\" or \"no\" on rotation statement.", rotacion, "CSVMOCAPFunc.py")

    #-------------------------------------------------------------------------------
    #-------------------------------------------------------------------------------
    print "    Reading choreography file"
    #Obtencion de directorio base
    rootDir = dirname(dirname(abspath(__file__)))
    #Declarando directorio para abrir archivo CSV
    ##Nombre del archivo CSV a leer
    archivo = os.path.join(rootDir, "Ver_Release/Choreography/")
    archivo = os.path.join(archivo, nombreArchivo)

    #Creando objeto con contenido del archivo CSV
    ##Abriendo archivo
    try:
        f = open(archivo, 'rt')
    except IOError:
        error.abort("Archivo no encontrado, revise nombre de la rutina a ejecutar.", None, "CSVMOCAPFunc")
    ##Obteniendo datos completos y cerrando archivo
    reader = csv.reader(f)
    filasIniciales = [r for r in reader]
    f.close()

    #-------------------------------------------------------------------------------
    #-------------------------------------------------------------------------------
    #Extrayendo informacion importante del archivo
    ##Obtencion del orden de aparicion de los marcadores(actuadores)
    filasActuadores = filasIniciales[3]
    ###Remueve primeros dos espacios siempre en blanco
    filasActuadores.remove('')
    filasActuadores.remove('')
    j = 0
    listaActuadores = [None]*6 #Se trabaja con 6 marcadores
    if rotacion.lower() == "no":
        for i, item in enumerate(filasActuadores):
            #Se repite el nombre del marcador 3 veces(XYZ)
            if i==0 or i==3 or i==6 or i==9 or i==12 or i==15:
                listaActuadores[j] = str(item)
                j+=1
    elif rotacion.lower() == "yes":
        for i, item in enumerate(filasActuadores):
            #Se repite el nombre del marcador 8 veces(wX,wY,wZ,W,X,Y,Z,Error)
            if i==0 or i==8 or i==16 or i==24 or i==32 or i==40:
                listaActuadores[j] = str(item)
                j+=1

    #-------------------------------------------------------------------------------
    ##Obtencion datos de posiciones, estas se muestran hasta la fila #8 del archivo
    ##incluyen numero de cuadro, tiempo en segundos y coordenadas XYZ en orden segun los
    ##actuadores obtenidos
    filasCoordenadas = filasIniciales[7::]

    ###Eliminado numero de cuadro, no se utiliza
    for i,item in enumerate(filasCoordenadas):
        del filasCoordenadas[i][0]

    ###Elimina columna de tiempos, y a su vez extrae los tiempos en caso de usarse
    ###estos en vez de la lista generada mas adelante por defecto
    tiempos = [None]*len(filasCoordenadas)
    for i,item in enumerate(filasCoordenadas):
        tiempos[i] = round(float(filasCoordenadas[i].pop(0)), 2)

    print "    Generating new coordinates"
    ###Ordenando coordenadas para generar lista de posiciones XYZ segun el orden de los actuadores
    contXYZ = 0
    contActuador = 0
    ####Manejando cada actuador con su propia lista de posiciones
    actuador = [None]*6
    for i in range(len(listaActuadores)):
        actuador[i] = list()

    #Ajuste sin rotacion
    if rotacion.lower() == "no":
        coordenadas = [0.0,0.0,0.0,0.0,0.0,0.0] #XYZ+rotacion
        try:
            for i, item in enumerate(filasCoordenadas):
                #contActuador = 1 #Reinicia contador de actuador cada vez que carga fila nueva
                for contTrio in range(0,18) : #3 DoF * 6 actuadores
                    if contXYZ < 2 :
                        try:
                            coordenadas[contXYZ] = float(filasCoordenadas[i].pop(0))
                        except ValueError:
                            print "Cell is not a valid value"
                        contXYZ+=1
                    elif contXYZ == 2 :
                        try:
                            coordenadas[contXYZ] = float(filasCoordenadas[i].pop(0))
                        except ValueError:
                            print "Cell is not a valid value"
                        contXYZ=0
                            #trioTemp[contXYZ] = coordenadas[contXYZ]
                        #Se tienen XYZ+rot para un actuador en un cuadro especifico
                        ### Z e Y estan invertidos en el marco de referencia del MoCap
                        ### Rotaciones en 0.0, X*-1
                        ####Sin importar el orden de los actuadores en el archivo aqui
                        ####se acomodan en el orden preferente y se aplica la correccion
                        ####con los offsets

                        #Polinomio grado 1
                        if deegree == 1:
                            if listaActuadores[contActuador] == "RArm":
                                actuador[0].append([round(coordenadas[0]*offRArm[0][0] + offRArm[0][1], 2),
                                                    round(coordenadas[2]*offRArm[1][0] + offRArm[1][1], 2),
                                                    round(coordenadas[1]*offRArm[2][0] + offRArm[2][1], 2),
                                                    0.0, 0.0, 0.0]) #Se pone rotaciones en 0 ya que no se van a utilizar
                            elif listaActuadores[contActuador] == "RLeg":
                                actuador[1].append([round(coordenadas[0]*offRArm[0][0] + offRArm[0][1], 2),
                                                    round(coordenadas[2]*offRArm[1][0] + offRArm[1][1], 2),
                                                    round(coordenadas[1]*offRArm[2][0] + offRArm[2][1], 2),
                                                    0.0, 0.0, 0.0])
                            elif listaActuadores[contActuador] == "LLeg":
                                actuador[2].append([round(coordenadas[0]*offRArm[0][0] + offRArm[0][1], 2),
                                                    round(coordenadas[2]*offRArm[1][0] + offRArm[1][1], 2),
                                                    round(coordenadas[1]*offRArm[2][0] + offRArm[2][1], 2),
                                                    0.0, 0.0, 0.0])
                            elif listaActuadores[contActuador] == "LArm":
                                actuador[3].append([round(coordenadas[0]*offRArm[0][0] + offRArm[0][1], 2),
                                                    round(coordenadas[2]*offRArm[1][0] + offRArm[1][1], 2),
                                                    round(coordenadas[1]*offRArm[2][0] + offRArm[2][1], 2),
                                                    0.0, 0.0, 0.0])
                            elif listaActuadores[contActuador] == "Torso":
                                actuador[4].append([round(coordenadas[0]*offRArm[0][0] + offRArm[0][1], 2),
                                                    round(coordenadas[2]*offRArm[1][0] + offRArm[1][1], 2),
                                                    round(coordenadas[1]*offRArm[2][0] + offRArm[2][1], 2),
                                                    0.0, 0.0, 0.0])
                            elif listaActuadores[contActuador] == "Head":
                                actuador[5].append([round(coordenadas[0]*offRArm[0][0] + offRArm[0][1], 2),
                                                    round(coordenadas[2]*offRArm[1][0] + offRArm[1][1], 2),
                                                    round(coordenadas[1]*offRArm[2][0] + offRArm[2][1], 2),
                                                    0.0, 0.0, 0.0])
                        #Polinomio grado 2
                        elif deegree == 2:
                            if listaActuadores[contActuador] == "RArm":
                                actuador[0].append([round((coordenadas[0]**2)*offRArm[0][0] + coordenadas[0]*offRArm[0][1]+offRArm[0][2], 2),
                                                    round((coordenadas[2]**2)*offRArm[1][0] + coordenadas[2]*offRArm[1][1]+offRArm[1][2], 2),
                                                    round((coordenadas[1]**2)*offRArm[2][0] + coordenadas[1]*offRArm[2][1]+offRArm[2][2], 2),
                                                    0.0, 0.0, 0.0]) #Se pone rotaciones en 0 ya que no se van a utilizar
                            elif listaActuadores[contActuador] == "RLeg":
                                actuador[1].append([round((coordenadas[0]**2)*offRArm[0][0] + coordenadas[0]*offRArm[0][1]+offRArm[0][2], 2),
                                                    round((coordenadas[2]**2)*offRArm[1][0] + coordenadas[2]*offRArm[1][1]+offRArm[1][2], 2),
                                                    round((coordenadas[1]**2)*offRArm[2][0] + coordenadas[1]*offRArm[2][1]+offRArm[2][2], 2),
                                                    0.0, 0.0, 0.0])
                            elif listaActuadores[contActuador] == "LLeg":
                                actuador[2].append([round((coordenadas[0]**2)*offRArm[0][0] + coordenadas[0]*offRArm[0][1]+offRArm[0][2], 2),
                                                    round((coordenadas[2]**2)*offRArm[1][0] + coordenadas[2]*offRArm[1][1]+offRArm[1][2], 2),
                                                    round((coordenadas[1]**2)*offRArm[2][0] + coordenadas[1]*offRArm[2][1]+offRArm[2][2], 2),
                                                    0.0, 0.0, 0.0])
                            elif listaActuadores[contActuador] == "LArm":
                                actuador[3].append([round((coordenadas[0]**2)*offRArm[0][0] + coordenadas[0]*offRArm[0][1]+offRArm[0][2], 2),
                                                    round((coordenadas[2]**2)*offRArm[1][0] + coordenadas[2]*offRArm[1][1]+offRArm[1][2], 2),
                                                    round((coordenadas[1]**2)*offRArm[2][0] + coordenadas[1]*offRArm[2][1]+offRArm[2][2], 2),
                                                    0.0, 0.0, 0.0])
                            elif listaActuadores[contActuador] == "Torso":
                                actuador[4].append([round((coordenadas[0]**2)*offRArm[0][0] + coordenadas[0]*offRArm[0][1]+offRArm[0][2], 2),
                                                    round((coordenadas[2]**2)*offRArm[1][0] + coordenadas[2]*offRArm[1][1]+offRArm[1][2], 2),
                                                    round((coordenadas[1]**2)*offRArm[2][0] + coordenadas[1]*offRArm[2][1]+offRArm[2][2], 2),
                                                    0.0, 0.0, 0.0])
                            elif listaActuadores[contActuador] == "Head":
                                actuador[5].append([round((coordenadas[0]**2)*offRArm[0][0] + coordenadas[0]*offRArm[0][1]+offRArm[0][2], 2),
                                                    round((coordenadas[2]**2)*offRArm[1][0] + coordenadas[2]*offRArm[1][1]+offRArm[1][2], 2),
                                                    round((coordenadas[1]**2)*offRArm[2][0] + coordenadas[1]*offRArm[2][1]+offRArm[2][2], 2),
                                                    0.0, 0.0, 0.0])
                        contActuador+=1
                        if contActuador == 6:
                            contActuador = 0
        except Exception,e:
            error.abort("Check file data, not able to read all of it", None, "CSVMOCAPFunc", "Move")

    #Ajuste con rotaciones
    if rotacion.lower() == "yes":
        coordenadas = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ,0.0, 0.0] #Incluye wX,wY,wZ,W,X,Y,Z,Error
        #try:
        for i, item in enumerate(filasCoordenadas):
            #contActuador = 1 #Reinicia contador de actuador cada vez que carga fila nueva
            for contTrio in range(0,48) :#(6 DoF+2 extra data) * 6 actuadores
                if contXYZ < 7 :
                    coordenadas[contXYZ] = float(filasCoordenadas[i].pop(0))
                    contXYZ+=1
                elif contXYZ == 7 :
                    coordenadas[contXYZ] = float(filasCoordenadas[i].pop(0))
                    contXYZ=0
                    #Orden datos en CSV (wX,wY,wZ,W,X,Y',Z',Error), con Y' y Z' cambiados
                    #Orden necesario de los datos (X,Z',Y',wX,wY,wZ), con Y'=Z y Z'=Y

                    #Polinomio grado 1
                    if degree == 1:
                        if listaActuadores[contActuador] == "RArm":
                            actuador[0].append([round(coordenadas[4]* offRArm[0][0] +  offRArm[0][1], 2),
                                                round(coordenadas[6]* offRArm[1][0] +  offRArm[1][1], 2),
                                                round(coordenadas[5]* offRArm[2][0] +  offRArm[2][1], 2),
                                                round(coordenadas[0]* offRArm[3][0] +  offRArm[3][1], 2),
                                                round(coordenadas[1]* offRArm[4][0] +  offRArm[4][1], 2),
                                                round(coordenadas[2]* offRArm[5][0] +  offRArm[5][1], 2),
                                               ])
                        elif listaActuadores[contActuador] == "RLeg":
                            actuador[1].append([round(coordenadas[4]* offRArm[0][0] +  offRArm[0][1], 2),
                                                round(coordenadas[6]* offRArm[1][0] +  offRArm[1][1], 2),
                                                round(coordenadas[5]* offRArm[2][0] +  offRArm[2][1], 2),
                                                round(coordenadas[0]* offRArm[3][0] +  offRArm[3][1], 2),
                                                round(coordenadas[1]* offRArm[4][0] +  offRArm[4][1], 2),
                                                round(coordenadas[2]* offRArm[5][0] +  offRArm[5][1], 2),
                                               ])
                        elif listaActuadores[contActuador] == "LLeg":
                            actuador[2].append([round(coordenadas[4]* offRArm[0][0] +  offRArm[0][1], 2),
                                                round(coordenadas[6]* offRArm[1][0] +  offRArm[1][1], 2),
                                                round(coordenadas[5]* offRArm[2][0] +  offRArm[2][1], 2),
                                                round(coordenadas[0]* offRArm[3][0] +  offRArm[3][1], 2),
                                                round(coordenadas[1]* offRArm[4][0] +  offRArm[4][1], 2),
                                                round(coordenadas[2]* offRArm[5][0] +  offRArm[5][1], 2),
                                               ])
                        elif listaActuadores[contActuador] == "LArm":
                            actuador[3].append([round(coordenadas[4]* offRArm[0][0] +  offRArm[0][1], 2),
                                                round(coordenadas[6]* offRArm[1][0] +  offRArm[1][1], 2),
                                                round(coordenadas[5]* offRArm[2][0] +  offRArm[2][1], 2),
                                                round(coordenadas[0]* offRArm[3][0] +  offRArm[3][1], 2),
                                                round(coordenadas[1]* offRArm[4][0] +  offRArm[4][1], 2),
                                                round(coordenadas[2]* offRArm[5][0] +  offRArm[5][1], 2),
                                               ])
                        elif listaActuadores[contActuador] == "Torso":
                            #Torso desbalance mucho, se debe restringir valores en X
                            torsoX = round(coordenadas[4]* offRArm[0][0] +  offRArm[0][1], 2)
                            if torsoX > 0.01:
                                torsoX = 0.01
                            elif torsoX < -0.01:
                                torsoX = -0.01

                            actuador[4].append([torsoX,
                                                round(coordenadas[6]* offRArm[1][0] +  offRArm[1][1], 2),
                                                round(coordenadas[5]* offRArm[2][0] +  offRArm[2][1], 2),
                                                round(coordenadas[0]* offRArm[3][0] +  offRArm[3][1], 2),
                                                round(coordenadas[1]* offRArm[4][0] +  offRArm[4][1], 2),
                                                round(coordenadas[2]* offRArm[5][0] +  offRArm[5][1], 2),
                                               ])
                        elif listaActuadores[contActuador] == "Head":
                            actuador[5].append([round(coordenadas[4]* offRArm[0][0] +  offRArm[0][1], 2),
                                                round(coordenadas[6]* offRArm[1][0] +  offRArm[1][1], 2),
                                                round(coordenadas[5]* offRArm[2][0] +  offRArm[2][1], 2),
                                                round(coordenadas[0]* offRArm[3][0] +  offRArm[3][1], 2),
                                                round(coordenadas[1]* offRArm[4][0] +  offRArm[4][1], 2),
                                                round(coordenadas[2]* offRArm[5][0] +  offRArm[5][1], 2),
                                               ])
                    #Polinomio grado 2
                    elif degree == 2:
                        if listaActuadores[contActuador] == "RArm":
                            actuador[0].append([round((coordenadas[4]**2)*offRArm[0][0] +  coordenadas[4]* offRArm[0][1] +  offRArm[0][2], 2),
                                                round((coordenadas[6]**2)*offRArm[1][0] +  coordenadas[6]* offRArm[1][1] +  offRArm[1][2], 2),
                                                round((coordenadas[5]**2)*offRArm[2][0] +  coordenadas[5]* offRArm[2][1] +  offRArm[2][2], 2),
                                                round((coordenadas[0]**2)*offRArm[3][0] +  coordenadas[0]* offRArm[3][1] +  offRArm[3][2], 2),
                                                round((coordenadas[1]**2)*offRArm[4][0] +  coordenadas[1]* offRArm[4][1] +  offRArm[4][2], 2),
                                                round((coordenadas[2]**2)*offRArm[5][0] +  coordenadas[2]* offRArm[5][1] +  offRArm[5][2], 2),
                                               ])
                        elif listaActuadores[contActuador] == "RLeg":
                            actuador[1].append([round((coordenadas[4]**2)*offRLeg[0][0] +  coordenadas[4]* offRLeg[0][1] +  offRLeg[0][2], 2),
                                                round((coordenadas[6]**2)*offRLeg[1][0] +  coordenadas[6]* offRLeg[1][1] +  offRLeg[1][2], 2),
                                                round((coordenadas[5]**2)*offRLeg[2][0] +  coordenadas[5]* offRLeg[2][1] +  offRLeg[2][2], 2),
                                                round((coordenadas[0]**2)*offRLeg[3][0] +  coordenadas[0]* offRLeg[3][1] +  offRLeg[3][2], 2),
                                                round((coordenadas[1]**2)*offRLeg[4][0] +  coordenadas[1]* offRLeg[4][1] +  offRLeg[4][2], 2),
                                                round((coordenadas[2]**2)*offRLeg[5][0] +  coordenadas[2]* offRLeg[5][1] +  offRLeg[5][2], 2),
                                               ])
                        elif listaActuadores[contActuador] == "LLeg":
                            actuador[2].append([round((coordenadas[4]**2)*offLLeg[0][0] +  coordenadas[4]* offLLeg[0][1] +  offLLeg[0][2], 2),
                                                round((coordenadas[6]**2)*offLLeg[1][0] +  coordenadas[6]* offLLeg[1][1] +  offLLeg[1][2], 2),
                                                round((coordenadas[5]**2)*offLLeg[2][0] +  coordenadas[5]* offLLeg[2][1] +  offLLeg[2][2], 2),
                                                round((coordenadas[0]**2)*offLLeg[3][0] +  coordenadas[0]* offLLeg[3][1] +  offLLeg[3][2], 2),
                                                round((coordenadas[1]**2)*offLLeg[4][0] +  coordenadas[1]* offLLeg[4][1] +  offLLeg[4][2], 2),
                                                round((coordenadas[2]**2)*offLLeg[5][0] +  coordenadas[2]* offLLeg[5][1] +  offLLeg[5][2], 2),
                                               ])
                        elif listaActuadores[contActuador] == "LArm":
                            actuador[3].append([round((coordenadas[4]**2)*offLArm[0][0] +  coordenadas[4]* offLArm[0][1] +  offLArm[0][2], 2),
                                                round((coordenadas[6]**2)*offLArm[1][0] +  coordenadas[6]* offLArm[1][1] +  offLArm[1][2], 2),
                                                round((coordenadas[5]**2)*offLArm[2][0] +  coordenadas[5]* offLArm[2][1] +  offLArm[2][2], 2),
                                                round((coordenadas[0]**2)*offLArm[3][0] +  coordenadas[0]* offLArm[3][1] +  offLArm[3][2], 2),
                                                round((coordenadas[1]**2)*offLArm[4][0] +  coordenadas[1]* offLArm[4][1] +  offLArm[4][2], 2),
                                                round((coordenadas[2]**2)*offLArm[5][0] +  coordenadas[2]* offLArm[5][1] +  offLArm[5][2], 2),
                                               ])
                        elif listaActuadores[contActuador] == "Torso":
                            actuador[4].append([round((coordenadas[4]**2)*offTorso[0][0] + coordenadas[4]*offTorso[0][1] + offTorso[0][2], 2),
                                                round((coordenadas[6]**2)*offTorso[1][0] + coordenadas[6]*offTorso[1][1] + offTorso[1][2], 2),
                                                round((coordenadas[5]**2)*offTorso[2][0] + coordenadas[5]*offTorso[2][1] + offTorso[2][2], 2),
                                                round((coordenadas[0]**2)*offTorso[3][0] + coordenadas[0]*offTorso[3][1] + offTorso[3][2], 2),
                                                round((coordenadas[1]**2)*offTorso[4][0] + coordenadas[1]*offTorso[4][1] + offTorso[4][2], 2),
                                                round((coordenadas[2]**2)*offTorso[5][0] + coordenadas[2]*offTorso[5][1] + offTorso[5][2], 2),
                                               ])
                        elif listaActuadores[contActuador] == "Head":
                            actuador[5].append([round((coordenadas[4]**2)*offHead[0][0] +  coordenadas[4]* offHead[0][1] +  offHead[0][2], 2),
                                                round((coordenadas[6]**2)*offHead[1][0] +  coordenadas[6]* offHead[1][1] +  offHead[1][2], 2),
                                                round((coordenadas[5]**2)*offHead[2][0] +  coordenadas[5]* offHead[2][1] +  offHead[2][2], 2),
                                                round((coordenadas[0]**2)*offHead[3][0] +  coordenadas[0]* offHead[3][1] +  offHead[3][2], 2),
                                                round((coordenadas[1]**2)*offHead[4][0] +  coordenadas[1]* offHead[4][1] +  offHead[4][2], 2),
                                                round((coordenadas[2]**2)*offHead[5][0] +  coordenadas[2]* offHead[5][1] +  offHead[5][2], 2),
                                               ])
                    contActuador+=1
                    if contActuador == 6:
                        contActuador = 0
    #    except Exception,e:
    #        error.abort("Check file data, not able to read all of it", None, "CSVMOCAPFunc", "Move")

    #En este punto ya se tienen los vectores de posiciones XYZ+rotacion(0.0) para cada
    #actuador independiente, en el orden segun el archivo CSV

    ##Generando Vector completo como lista de vectores para cada actuador
    global coordenadasCompletas
    coordenadasCompletas = [actuador[0], actuador[1], actuador[2], actuador[3], actuador[4], actuador[5]]
    global coordenadasArriba
    coordenadasArriba = [actuador[0], actuador[3], actuador[4]]
    global coordenadasROBOT
    coordenadasROBOT = [actuador[0], actuador[3], actuador[5]]

    ##Si los datos obtenidos vienen con referencia al TORSO no es necesario este
    ##proceso de cambio de referencia
    listaDeActuadores = deepcopy(coordenadasCompletas)
    ## RArm
    for i, item in enumerate(listaDeActuadores[0]):
        for j, item2 in enumerate(listaDeActuadores[0][j]):
            listaDeActuadores[0][i][j] = round((listaDeActuadores[0][i][j] - listaDeActuadores[4][i][j]), 2)
    ## RLeg
    for i, item in enumerate(listaDeActuadores[1]):
        for j, item2 in enumerate(listaDeActuadores[1][j]):
            listaDeActuadores[1][i][j] = round((listaDeActuadores[1][i][j] - listaDeActuadores[4][i][j]), 2)
    ## LLeg
    for i, item in enumerate(listaDeActuadores[2]):
        for j, item2 in enumerate(listaDeActuadores[2][j]):
            listaDeActuadores[2][i][j] = round((listaDeActuadores[2][i][j] - listaDeActuadores[4][i][j]), 2)
    ## LArm
    for i, item in enumerate(listaDeActuadores[3]):
        for j, item2 in enumerate(listaDeActuadores[3][j]):
            listaDeActuadores[3][i][j] = round((listaDeActuadores[3][i][j] - listaDeActuadores[4][i][j]), 2)
    ## Head
    for i, item in enumerate(listaDeActuadores[5]):
        for j, item2 in enumerate(listaDeActuadores[5][j]):
            listaDeActuadores[5][i][j] = round((listaDeActuadores[5][i][j] - listaDeActuadores[5][i][j]), 2)
    ## TORSO
    #No se controla el Torso directamente ya que contiene el marco de referencia

    #Genera lista con datos respecto al TORSO
    global coordenadasTORSO
    coordenadasTORSO = [listaDeActuadores[0], listaDeActuadores[1], listaDeActuadores[2], listaDeActuadores[3], listaDeActuadores[5]]

    #-------------------------------------------------------------------------------
    #Base de tiempo predeterminado para cada vector de la animacion
    ##Debe ser mayor a 20 ms (tiempo que dura en resolver el balance de cuerpo completo)
    ##y dar al menos 30 ms entre cambios
    ##coef depende de los cuadros por segundo de la animacion en Motive en el momento
    ##de exportar los datos
    #Se maneja un vector de tiempos independiente para cada actuador, con longitud
    #correspondiente a la lista con coordenadas respectivo al actuador
    coef = 0.05
    #coef = 0.1
    global listaTiemposROBOT
    listaTiemposROBOT = [None]*len(coordenadasROBOT)
    for i in range(len(coordenadasROBOT)):
        listaTiemposROBOT[i]  = [round(coef*(j+1),2) for j in range(len(coordenadasROBOT[i]))]
    global listaTiemposCompletos
    listaTiemposCompletos = [None]*len(coordenadasCompletas)
    for i in range(len(coordenadasROBOT)):
        listaTiemposCompletos[i]  = [round(coef*(j+1),2) for j in range(len(coordenadasCompletas[i]))]
    global listaTiemposArriba
    listaTiemposArriba = [None]*len(coordenadasArriba)
    for i in range(len(coordenadasArriba)):
        listaTiemposArriba[i]  = [round(coef*(j+1),2) for j in range(len(coordenadasArriba[i]))]

    global listaTiemposTORSO
    listaTiemposTORSO = [None]*len(coordenadasTORSO)
    for i in range(len(coordenadasTORSO)):
        listaTiemposTORSO[i]  = [round(coef*(j+1),2) for j in range(len(coordenadasTORSO[i]))]

    print "Coordinates generated. Ready for movement."
    print "++++++++++++++++++++++++++++++++++++++++++++++++++++"

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#Interfaz de extraccion de datos

##Devuelve posiciones X,Y,Z+rot en orden correspondiente a los actuadores obtenidos
##segun el marco de referencia
def getCoordenadas(frame):
    if frame.upper() == "ROBOT":
        return coordenadasROBOT
    elif frame.upper() == "TORSO":
        return coordenadasTORSO
    elif frame.upper() == "ARRIBA":
        return coordenadasArriba
    else:
        error.abort("Did not receive a valid reference frame.", None, "CSVMOCAPFunc")

##Devuelve lista de Tiempos del movimiento
##segun el marco de referencia
def getTiempos(frame):
    if frame.upper() == "ROBOT":
        return listaTiemposROBOT
    elif frame.upper() == "TORSO":
        return listaTiemposTORSO
    elif frame.upper() == "ARRIBA":
        return listaTiemposArriba
    else:
        error.abort("Did not receive a valid reference frame.", None, "CSVMOCAPFunc")
