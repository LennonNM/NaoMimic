#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#Al ejecutarse inicia la toma de datos de las posiciones de los actuadores
#correspondientes a los 6 efectores finales del robot humanoide NAO
#(RArm, RLeg, LLeg, LArm, Torso, Head). Se toman "rows" cantidad de sets de
#coordenadas. Se incluye coordenadas XYZ (+rotaciones si se especifica por el
#usuario)
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#Imports
import sys
import time
from naoqi import ALProxy
import motion
import csv
import os
from itertools import islice
from os.path import dirname, abspath

##Custom
import Error_Func as error

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#Recibe IP del robot NAO, marco de referencia de las coordenadas y si se quiere
#tomar datos de las rotaciones.
#Devuelve un archivo CSV con la informacion solicitada, siguiende el formato
#general de exportacion de archivo CSV de Motive
def main(robotIP, frameRef, rotation, name=None):
    PORT = 9559
    print "Using Port:", PORT
    if rotation.lower() != "no":
        if rotation.lower() != "yes":
            error.abort("Expected a yes or no input for rotation data inclussion", "GetPositions")

    try:
        print "Trying to create ALMotion proxy"
        motionProxy = ALProxy("ALMotion", robotIP, PORT)
    except Exception,e:
        print "Could not create proxy to ALMotion"
        print "Error was: ", e
        sys.exit(1)
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#Ajustes iniciales

    #Marco de referencia para la obtencion de datos
    if frameRef.upper() == "ROBOT":
        space = motion.FRAME_ROBOT
    elif frameRef.upper() == "TORSO":
        space = motion.FRAME_TORSO
    else:
        error.abort("is not a valid frame for function", frame, "GetPositions")
    #Uso de sensores adicionales para aproximar el estado del actuador
    useSensorValues = False
#-------------------------------------------------------------------------------
#Obtencion de los datos

    posRArm = []
    posRLeg = []
    posLLeg = []
    posLArm = []
    posTorso = []
    posHead = []
    rows = 0

    print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    print "Starting to collect data, interrupt the process only if necessary"
    print "Wait for completion"
    print "Press Ctrl+C to stop collecting data and proceed with data writting"
    time.sleep(0.5)

    try:
        while (True):
            posRArm.append(motionProxy.getPosition("RArm", space, useSensorValues))
            posRLeg.append(motionProxy.getPosition("RLeg", space, useSensorValues))
            posLLeg.append(motionProxy.getPosition("LLeg", space, useSensorValues))
            posLArm.append(motionProxy.getPosition("LArm", space, useSensorValues))
            posTorso.append(motionProxy.getPosition("Torso", space, useSensorValues))
            posHead.append(motionProxy.getPosition("Head", space, useSensorValues))
            time.sleep(0.003)

            rows +=1
    except KeyboardInterrupt:
        print "Data collection finished"
        print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
        print "Writing CSV with data"
        time.sleep(0.25)
        pass
#-------------------------------------------------------------------------------
#Guardado de los datos en un archivo CSV

    #Se utiliza el formato de Motive para el acomodo de los datos en el CSV
    ## 2 columnas con cuadros y tiempos (no se ocupan), 3 columnas (XYZ) por cada
    ## marcador involucrado(actuador) /// Filas 1 a 6 no dan informacion valiosa,
    ## en la fila 7 va el identificador de cada columna, a partir de la fila 8
    ## inician los datos de las posiciones
    rootDir = dirname(dirname(abspath(__file__)))
    archivo = os.path.join(rootDir, "Ver_Release/Cal/NAO/GetPositions_Generated/NAO_")
    if name is None:
        archivo += frameRef
        if rotation.lower() == "yes":
            archivo += "-wROT"
        archivo += time.strftime("_%Y-%m-%d_%H-%M-%S")
    else:
        archivo += name
    archivo += ".csv"

    #Archivo incluyendo rotaciones del NAO
    if rotation.lower() == "yes":
        with open(archivo, 'w') as csvfile:
            fieldnames = ['C1', 'C2', 'X RArm', 'Y RArm', 'Z RArm', 'WX RArm', 'WY RArm', 'WZ RArm', 'X RLeg', 'Y RLeg', 'Z RLeg', 'WX RLeg', 'WY RLeg', 'WZ RLeg',
                            'X LLeg', 'Y LLeg', 'Z LLeg', 'WX LLeg', 'WY LLeg', 'WZ LLeg', 'X LArm', 'Y LArm', 'Z LArm', 'WX LArm', 'WY LArm', 'WZ LArm',
                            'X Torso', 'Y Torso', 'Z Torso', 'WX Torso', 'WY Torso', 'WZ Torso', 'X Head', 'Y Head', 'Z Head', 'WX Head', 'WY Head', 'WZ Head']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            for x in range(6):
                writer.writerow({})
            writer.writeheader()
            for i in range(rows):
                writer.writerow({'X RArm': posRArm[i][0], 'Y RArm': posRArm[i][1], 'Z RArm': posRArm[i][2], 'WX RArm': posRArm[i][3], 'WY RArm': posRArm[i][4], 'WZ RArm': posRArm[i][5],
                                    'X RLeg': posRLeg[i][0], 'Y RLeg': posRLeg[i][1], 'Z RLeg': posRLeg[i][2], 'WX RLeg': posRLeg[i][3], 'WY RLeg': posRLeg[i][4], 'WZ RLeg': posRLeg[i][5],
                                    'X LLeg': posLLeg[i][0], 'Y LLeg': posLLeg[i][1], 'Z LLeg': posLLeg[i][2], 'WX LLeg': posLLeg[i][3], 'WY LLeg': posLLeg[i][4], 'WZ LLeg': posLLeg[i][5],
                                    'X LArm': posLArm[i][0], 'Y LArm': posLArm[i][1], 'Z LArm': posLArm[i][2], 'WX LArm': posLArm[i][3], 'WY LArm': posLArm[i][4], 'WZ LArm': posLArm[i][5],
                                    'X Torso': posTorso[i][0], 'Y Torso': posTorso[i][1], 'Z Torso': posTorso[i][2], 'WX Torso': posTorso[i][3], 'WY Torso': posTorso[i][4], 'WZ Torso': posTorso[i][5],
                                    'X Head': posHead[i][0], 'Y Head': posHead[i][1], 'Z Head': posHead[i][2], 'WX Head': posHead[i][3], 'WY Head': posHead[i][4], 'WZ Head': posHead[i][5],
                                })
        #Archivo sin rotaciones
    else:
            with open(archivo, 'w') as csvfile:
                fieldnames = ['C1', 'C2', 'X RArm', 'Y RArm', 'Z RArm', 'X RLeg', 'Y RLeg', 'Z RLeg', 'X LLeg', 'Y LLeg', 'Z LLeg', 'X LArm', 'Y LArm', 'Z LArm',
                                  'X Torso', 'Y Torso', 'Z Torso', 'X Head', 'Y Head', 'Z Head']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                for x in range(6):
                    writer.writerow({})
                writer.writeheader()
                for i in range(rows):
                    writer.writerow({'X RArm': posRArm[i][0], 'Y RArm': posRArm[i][1], 'Z RArm': posRArm[i][2], 'X RLeg': posRLeg[i][0], 'Y RLeg': posRLeg[i][1], 'Z RLeg': posRLeg[i][2],
                                        'X LLeg': posLLeg[i][0], 'Y LLeg': posLLeg[i][1], 'Z LLeg': posLLeg[i][2], 'X LArm': posLArm[i][0], 'Y LArm': posLArm[i][1], 'Z LArm': posLArm[i][2],
                                        'X Torso': posTorso[i][0], 'Y Torso': posTorso[i][1], 'Z Torso': posTorso[i][2], 'X Head': posHead[i][0], 'Y Head': posHead[i][1], 'Z Head': posHead[i][2],
                                    })

    print "END"
    print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
if __name__ == "__main__":
    robotIP = "10.0.1.128" #Bato en red PrisNAO
    frameRef = "ROBOT"
    rotation = "no"
    name = None

    if len(sys.argv) == 4:
        robotIP = sys.argv[1]
        frame = sys.argv[2]
        rotation = sys.argv[3]
        print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
        print "Using robot IP:", sys.argv[1], " with frame:", frameRef
        print "Include rotations:", rotation
        print "Name of CSV file default by system date and time"
        print "---------------------------------------------------------"
        print "Starting to retrieve sensor values"
        print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    elif len(sys.argv) == 5:
        robotIP = sys.argv[1]
        frame = sys.argv[2]
        rotation = sys.argv[3]
        name = sys.argv[4]
        print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
        print "Using robot IP:", sys.argv[1], " with frame:", frameRef
        print "Include rotations:", rotation
        print "Name of CSV file: NAO_", name
        print "---------------------------------------------------------"
        print "Starting to retrieve sensor values"
        print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    else:
        error.abort("Expected 3 or 4 arguments on call.", "GetPositions")

    time.sleep(1.0)
    main(robotIP, frameRef, rotation, name)
