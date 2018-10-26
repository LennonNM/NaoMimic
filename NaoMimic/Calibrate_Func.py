#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#Incluye las funciones a utilizar para el proceso de calibracion definido en
#Calibrate.py
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#Imports
import csv
import os
import numpy as np
from scipy.interpolate import *
from itertools import islice
from os.path import dirname, abspath
from copy import deepcopy

#Custom
import Error_Func as error
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#Globales
###Listas de coordenadas para cada actuador
RArmPCal  = list()
RLegPCal  = list()
LLegPCal  = list()
LArmPCal  = list()
TorsoPCal = list()
HeadPCal  = list()
###Listas de coordenadas para cada actuador
RArmNaoCal  = list()
RLegNaoCal  = list()
LLegNaoCal  = list()
LArmNaoCal  = list()
TorsoNaoCal = list()
HeadNaoCal  = list()

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#Recibe archivos con las grabaciones de calibracion de una pose, del NAO y de
#la persona. Devuelve listas individuales para cada actuador del NAO y de la
#persona.
def setCalData(archNao, archP, wRot):
    #Limpia listas por usos previos
    RArmPCal[:] = []
    RLegPCal[:] = []
    LLegPCal[:] = []
    LArmPCal[:] = []
    TorsoPCal[:] = []
    HeadPCal[:] = []
    RArmNaoCal[:] = []
    RLegNaoCal[:] = []
    LLegNaoCal[:] = []
    LArmNaoCal[:] = []
    TorsoNaoCal[:] = []
    HeadNaoCal[:] = []

    #Directorios con los datos de calibracion
    ##Root (../Code)
    rootDir = dirname(dirname(abspath(__file__)))
    ##Archivos con posiciones del Nao
    dirNao = os.path.join(rootDir, "Ver_Release/Calibration/NAO/")
    dirNao = os.path.join(dirNao, archNao)
    ##Archivos con posiciones de la PERSONA_ROBOT
    dirPersona = os.path.join(rootDir, "Ver_Release/Calibration/Human/")
    dirPersona = os.path.join(dirPersona, archP)

    #Obteniendo contenidos
    ##Nao
    try:
        fNao = open(dirNao, 'rt')
    except Exception,e:
        error.abort("is not a valid directory", dirNao, "CalibrateFunc")

    ##Obteniendo datos completos y cerrando archivo
    reader = csv.reader(fNao)
    filasNao = [r for r in reader]
    fNao.close()
    ##Persona
    try:
        fPersona = open(dirPersona, 'rt')
    except Exception,e:
        error.abort("is not a valid directory", dirPersona, "CalibrateFunc")
    ##Obteniendo datos completos y cerrando archivo
    reader = csv.reader(fPersona)
    filasPersona = [r for r in reader]
    fPersona.close()

    #-------------------------------------------------------------------------------
    #-------------------------------------------------------------------------------
    #Extraccion datos del Nao
    ##Datos numericos a partir de la fila #8
    filasDatosNao = filasNao[7::]
    ##Eliminando columnas de Cuadro y Tiempos
    for i,item in enumerate(filasDatosNao):
        del filasDatosNao[i][0]
        del filasDatosNao[i][0]

    if wRot.lower() == "no":
        #Sin rotaciones
        contXYZ = 0
        trioXYZ = [0.0,0.0,0.0]
        contAct = 0

        for i,item in enumerate(filasDatosNao):
            for contTrio in range(0,18): #3DoF*6Actuadores
                if contXYZ < 2:
                    trioXYZ[contXYZ] = float(filasDatosNao[i].pop(0))
                    contXYZ+=1

                elif contXYZ == 2:
                    trioXYZ[contXYZ] = float(filasDatosNao[i].pop(0))
                    contXYZ = 0

                    if (contAct == 0):
                        RArmNaoCal.append( [trioXYZ[0], trioXYZ[1], trioXYZ[2]])
                    elif (contAct == 1):
                        RLegNaoCal.append( [trioXYZ[0], trioXYZ[1], trioXYZ[2]])
                    elif (contAct == 2):
                        LLegNaoCal.append( [trioXYZ[0], trioXYZ[1], trioXYZ[2]])
                    elif (contAct == 3):
                        LArmNaoCal.append( [trioXYZ[0], trioXYZ[1], trioXYZ[2]])
                    elif (contAct == 4):
                        TorsoNaoCal.append([trioXYZ[0], trioXYZ[1], trioXYZ[2]])
                    elif (contAct == 5):
                        HeadNaoCal.append( [trioXYZ[0], trioXYZ[1], trioXYZ[2]])

                    if (contAct == 5):
                        contAct = 0
                    else:
                        contAct+=1

    elif wRot.lower() == "yes":
        #Con rotaciones
        contXYZ = 0
        trioXYZ = [0.0,0.0,0.0,0.0,0.0,0.0]
        contAct = 0

        for i,item in enumerate(filasDatosNao):
            for contTrio in range(0,36):#6Dof*6Actuadores
                if contXYZ < 5:
                    trioXYZ[contXYZ] = float(filasDatosNao[i].pop(0))
                    contXYZ+=1
                elif contXYZ == 5:
                    trioXYZ[contXYZ] = float(filasDatosNao[i].pop(0))
                    contXYZ = 0

                    if (contAct == 0):
                        RArmNaoCal.append( [trioXYZ[0], trioXYZ[1], trioXYZ[2], trioXYZ[3], trioXYZ[4], trioXYZ[5]])
                    elif (contAct == 1):
                        RLegNaoCal.append( [trioXYZ[0], trioXYZ[1], trioXYZ[2], trioXYZ[3], trioXYZ[4], trioXYZ[5]])
                    elif (contAct == 2):
                        LLegNaoCal.append( [trioXYZ[0], trioXYZ[1], trioXYZ[2], trioXYZ[3], trioXYZ[4], trioXYZ[5]])
                    elif (contAct == 3):
                        LArmNaoCal.append( [trioXYZ[0], trioXYZ[1], trioXYZ[2], trioXYZ[3], trioXYZ[4], trioXYZ[5]])
                    elif (contAct == 4):
                        TorsoNaoCal.append([trioXYZ[0], trioXYZ[1], trioXYZ[2], trioXYZ[3], trioXYZ[4], trioXYZ[5]])
                    elif (contAct == 5):
                        HeadNaoCal.append( [trioXYZ[0], trioXYZ[1], trioXYZ[2], trioXYZ[3], trioXYZ[4], trioXYZ[5]])

                    if (contAct == 5):
                        contAct = 0
                    else:
                        contAct+=1

    #-------------------------------------------------------------------------------
    #Extraccion datos de la persona
    #NOTA: ejes Y y Z estan invertidos
    ##Obtencion del orden de aparicion de los marcadores(actuadores)
    filasActuadores = filasPersona[3]
    ###Remueve primeros dos espacios siempre en blanco
    filasActuadores.remove('')
    filasActuadores.remove('')
    j = 0
    listaActuadores = [None]*6 #Se trabaja con cadenas de accion del NAO
    if wRot.lower() == "no":
        for i, item in enumerate(filasActuadores):
            #Se repite el nombre del marcador 3 veces(XYZ)
            if i==0 or i==3 or i==6 or i==9 or i==12 or i==15:
                listaActuadores[j] = str(item)
                j+=1
    elif wRot.lower() == "yes":
        for i, item in enumerate(filasActuadores):
            #Se repite el nombre del marcador 3 veces(XYZ)
            if i==0 or i==8 or i==16 or i==24 or i==32 or i==40:
                listaActuadores[j] = str(item)
                j+=1

    ##Datos numericos a partir de la fila #8
    filasDatosP = filasPersona[7::]
    ##Eliminando columnas de Cuadro y Tiempos
    for i,item in enumerate(filasDatosP):
        del filasDatosP[i][0]
        del filasDatosP[i][0]

    #Sin rotaciones
    if wRot.lower() == "no":
        contXYZ = 0
        trioXYZ = [0.0,0.0,0.0]
        contAct = 0

        for i,item in enumerate(filasDatosP):
            for contTrio in range(0,18):
                if contXYZ < 2:
                    temp = filasDatosP[i].pop(0)
                    try:
                        trioXYZ[contXYZ] = float(temp)
                    except ValueError:
                        trioXYZ[contXYZ] = temp
                    contXYZ+=1

                elif contXYZ == 2:
                    temp = filasDatosP[i].pop(0)
                    try:
                        trioXYZ[contXYZ] = float(temp)
                    except ValueError:
                        trioXYZ[contXYZ] = temp
                    contXYZ = 0

                    if listaActuadores[contAct] == "RArm":
                        RArmPCal.append( [trioXYZ[0], trioXYZ[2], trioXYZ[1]])
                    elif listaActuadores[contAct] == "RLeg":
                        RLegPCal.append( [trioXYZ[0], trioXYZ[2], trioXYZ[1]])
                    elif listaActuadores[contAct] == "LLeg":
                        LLegPCal.append( [trioXYZ[0], trioXYZ[2], trioXYZ[1]])
                    elif listaActuadores[contAct] == "LArm":
                        LArmPCal.append( [trioXYZ[0], trioXYZ[2], trioXYZ[1]])
                    elif listaActuadores[contAct] == "Torso":
                        TorsoPCal.append([trioXYZ[0], trioXYZ[2], trioXYZ[1]])
                    elif listaActuadores[contAct] == "Head":
                        HeadPCal.append( [trioXYZ[0], trioXYZ[2], trioXYZ[1]])

                    if (contAct == 5):
                        contAct = 0
                    else:
                        contAct+=1
    #Con rotaciones
    elif wRot.lower() == "yes":
        contXYZ = 0
        trioXYZ = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0] #Incluye wX,wY,wZ,W,X,Y,Z,Error
        contAct = 0
        temp = 0

        for i,item in enumerate(filasDatosP):
            for contTrio in range(0,48):
                if contXYZ < 7:
                    temp = filasDatosP[i].pop(0)
                    try:
                        trioXYZ[contXYZ] = float(temp)
                    except ValueError:
                        #Es una celda marcada como invalida, luego se procesa
                        ##Las celdas invalidas no se usan para calibracion porque no dan
                        ##un buen ajuste temporal entre los datos, se marcan con la palabra
                        ##'Empty' de manera manual en el CSV a leer
                        trioXYZ[contXYZ] = temp
                    contXYZ+=1

                elif contXYZ == 7:
                    temp = filasDatosP[i].pop(0)
                    try:
                        trioXYZ[contXYZ] = float(temp)
                    except ValueError:
                        trioXYZ[contXYZ] = temp
                    contXYZ = 0

                    #Y y Z estan intercambiadas, al igual que wY y wZ
                    #Solo se ocupan X,Y,Z,wX,wY,wZ
                    if listaActuadores[contAct] == "RArm":
                        RArmPCal.append( [trioXYZ[4],trioXYZ[6],trioXYZ[5],trioXYZ[0], trioXYZ[2], trioXYZ[1]])
                    elif listaActuadores[contAct] == "RLeg":
                        RLegPCal.append( [trioXYZ[4],trioXYZ[6],trioXYZ[5],trioXYZ[0], trioXYZ[2], trioXYZ[1]])
                    elif listaActuadores[contAct] == "LLeg":
                        LLegPCal.append( [trioXYZ[4],trioXYZ[6],trioXYZ[5],trioXYZ[0], trioXYZ[2], trioXYZ[1]])
                    elif listaActuadores[contAct] == "LArm":
                        LArmPCal.append( [trioXYZ[4],trioXYZ[6],trioXYZ[5],trioXYZ[0], trioXYZ[2], trioXYZ[1]])
                    elif listaActuadores[contAct] == "Torso":
                        TorsoPCal.append([trioXYZ[4],trioXYZ[6],trioXYZ[5],trioXYZ[0], trioXYZ[2], trioXYZ[1]])
                    elif listaActuadores[contAct] == "Head":
                        HeadPCal.append( [trioXYZ[4],trioXYZ[6],trioXYZ[5],trioXYZ[0], trioXYZ[2], trioXYZ[1]])

                    if (contAct == 5):
                        contAct = 0
                    else:
                        contAct+=1

    return RArmNaoCal,RLegNaoCal,LLegNaoCal,LArmNaoCal,TorsoNaoCal,HeadNaoCal,RArmPCal,RLegPCal,LLegPCal,LArmPCal,TorsoPCal,HeadPCal

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#Realiza la regresion polinomial deseada para encontrar los terminos del ajuste
#Recibe la lista con datos de coordenadas XYZ para un solo actuador, del NAO
#y de la persona, asi como el grado polinomial.
#Devuelve una lista con los terminos del ajuste polinomial para X, Y y Z del
#actuador recibido
def getTerms(listNAO, listP, degree, wRot):
    naoX  = list()
    naoY  = list()
    naoZ  = list()
    naowX = list()
    naowY = list()
    naowZ = list()
    pX    = list()
    pY    = list()
    pZ    = list()
    pwX    = list()
    pwY    = list()
    pwZ    = list()
    dif = 0

    if wRot.lower() == "no":
        pl = [None]*3
    elif wRot.lower() == "yes":
        pl = [None]*6

    #---------------------------------------------------------------------------
	#Separa datos X, Y y Z en grupos

    if wRot.lower() == "no":
            #Datos NAO
        for i in range(len(listNAO)):
            naoX.append(listNAO[i][0])
            naoY.append(listNAO[i][1])
            naoZ.append(listNAO[i][2])
            #Daos MoCap
        for i in range(len(listP)):
            pX.append(listP[i][0])
            pY.append(listP[i][1])
            pZ.append(listP[i][2])
    elif wRot.lower() == "yes":
            #Datos NAO
        for i in range(len(listNAO)):
            naoX.append(listNAO[i][0])
            naoY.append(listNAO[i][1])
            naoZ.append(listNAO[i][2])
            naowX.append(listNAO[i][3])
            naowY.append(listNAO[i][4])
            naowZ.append(listNAO[i][5])
            #Datos MoCap
        for i in range(len(listP)):
            ##X
            if isinstance(listP[i][0], float):
                pX.append(listP[i][0])
            ##Y
            if isinstance(listP[i][1], float):
                pY.append(listP[i][1])
            ##Z
            if isinstance(listP[i][2], float):
                pZ.append(listP[i][2])
            ##wX
            if isinstance(listP[i][3], float):
                pwX.append(listP[i][3])
            ##wY
            if isinstance(listP[i][4], float):
                pwY.append(listP[i][4])
            ##wZ
            if isinstance(listP[i][5], float):
                pwZ.append(listP[i][5])

        #Manejo de diferentes longitudes de las listas, hace que las listas tengan
        #la misma longitud si correrlas temporalmente, segun como estaban acomodadas
        #desde la comparacio grafica
        ##X
        dif = len(pX)-len(naoX)
        if dif < 0:
            del naoX[len(naoX)-1+dif:len(naoX)-1]
        elif dif > 0:
            del pX[len(pX)-1-dif:len(pX)-1]
        ##Y
        dif = len(pY)-len(naoY)
        if dif < 0:
            del naoY[len(naoY)-1+dif:len(naoY)-1]
        elif dif > 0:
            del pY[len(pY)-1-dif:len(pY)-1]
        ##Z
        dif = len(pZ)-len(naoZ)
        if dif < 0:
            del naoZ[len(naoZ)-1+dif:len(naoZ)-1]
        elif dif > 0:
            del pZ[len(pZ)-1-dif:len(pZ)-1]
        ##wX
        dif = len(pwX)-len(naowX)
        if dif < 0:
            del naowX[len(naowX)-1+dif:len(naowX)-1]
        elif dif > 0:
            del pwX[len(pwX)-1-dif:len(pwX)-1]
        ##wY
        dif = len(pwY)-len(naowY)
        if dif < 0:
            del naowY[len(naowY)-1+dif:len(naowY)-1]
        elif dif > 0:
            del pwY[len(pwY)-1-dif:len(pwY)-1]
        ##wZ
        dif = len(pwZ)-len(naowZ)
        if dif < 0:
            del naowZ[len(naowZ)-1+dif:len(naowZ)-1]
        elif dif > 0:
            del pwZ[len(pwZ)-1-dif:len(pwZ)-1]

    #---------------------------------------------------------------------------
	#Obtiene los terminos de la relacion polinomial con grado 'degree'
    ##Se ocupa que ambos arreglos a comparar tengan la misma cantidad de datos,
    ##por lo que se supone que en el estudio de comparaciones se ajusto las
    ##longitudes para que sean iguales

    pl[0] = list(np.polyfit(pX,naoX,degree))
    pl[1] = list(np.polyfit(pY,naoY,degree))
    pl[2] = list(np.polyfit(pZ,naoZ,degree))

    if wRot.lower() == "yes":
        pl[3] = list(np.polyfit(pwX,naowX,degree))
        pl[4] = list(np.polyfit(pwY,naowY,degree))
        pl[5] = list(np.polyfit(pwZ,naowZ,degree))

    return pl
