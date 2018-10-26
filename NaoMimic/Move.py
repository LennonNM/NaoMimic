#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#Programa principal para la ejecucion de la Teleoperacion del robot NAO.
#Se encarga del control del NAO por grabaciones guardadas.. Recibe vectores
#de tiempos y coordenadas listos para ser enviados directamente al robot NAO.
#Solicita al usuario IP del robot a conectarse y nombre del archivo CSV que
#contiene los datos de la grabacion de MoCap que se quiere utilizar para que el
#robot "imite" los movimientos. (Primer argumento es el nombre del archivo y
#el segundo es la direccion IP)
##
#Utiliza los API's del robot NAO para efectuar su control.
##
#Permite utilizar marco de referencia ROBOT y TORSO, segun defina el usuario, por
#defecto se trabaja con ROBOT.
##
#Hace uso del balanceador de cuerpo completo incluido en las herramientas de
#desarrollo de las librerias del robot humanoide NAO. Para realizar un mejor
#balance se requiere manipular los puntos de apoyo del balance segun la
#posicion que se esta llevando a cabo.
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# -*- encoding: UTF-8 -*-
#Imports
import sys
import time
import numpy as np
from naoqi import ALProxy
import motion

##Custom
import CSVMOCAP_Func as csvMocap
import Error_Func as error

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
# Control de la rigidez de los motores
def StiffnessOn(proxy):
    # Body representa elconjunto de todas las articulaciones
    pNames = "Body"
    pStiffnessLists = 1.0
    pTimeLists = 1.0
    proxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)
#-------------------------------------------------------------------------------
def main(robotIP,coreo,marcoRef,offFile):
    #SetUp
    PORT = 9559 #Puerto por defecto
    print "++++++++++++++++++++++++++++++++++++++++++++++++"
    print "Creating NAO proxies for posture and movement"
    #creacion de objetos para usar los metodos de los API's del Nao
    try:
        #Para poder utilizar funciones de movimiento de los actuadores del NAO
        motionProxy = ALProxy("ALMotion", robotIP, PORT)
    except Exception,e:
        error.abort("Could not create proxy to ALMotion.", None,"Move")
    try:
        #Para utilizar posiciones preestablecidas del NAO
        postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
    except Exception, e:
        error.abort("Could not create proxy to ALRobotPosture.", None,"Move")
    print "Connection to NAO available."
    print "++++++++++++++++++++++++++++++++++++++++++++++++"
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#Inicializacion de parametros necesarios para el movimiento del NAO
    print "----------------------------------"
    print "    Setting frame"
    ##Marco de Referencia a utilizar
        #referencia = motion.FRAME_TORSO #Referencia centro del Torso
                                    #Vale 0
        #referencia = motion.FRAME_WORLD #Referencia estado inicial del robot al iniciar animacion
                                    #Vale 1
        #referencia = motion.FRAME_ROBOT #Referencia origen justo debajo del NAO entre los pies
                                    #Vale 2
    if marcoRef.upper() == "TORSO":
        referencia = motion.FRAME_TORSO
        print "        Frame set to TORSO"
    elif marcoRef.upper() == "ROBOT" or marcoRef.upper() == "ARRIBA":
        referencia = motion.FRAME_ROBOT
        print "        Frame set to ROBOT"
    else:
        error.abort("Did not receive a valid Reference Frame.", "Move")

    ##Relacion coordenadas con marco de referencia
        #True para usar coordenadas absolutas respecto al marco de referencia
    absolutos = True

    ##Grados de libertad a utilizar
    ###Debe incluir un elemento por cada actuador a controlar
    #### AXIS_MASK_ALL controla XYZ y rotacion
    #### AXIS_MASK_VEL controla solo XYZ
    #axisMask = [ motion.AXIS_MASK_ALL, motion.AXIS_MASK_ALL, motion.AXIS_MASK_ALL, motion.AXIS_MASK_ALL, motion.AXIS_MASK_ALL, motion.AXIS_MASK_ALL ]
    if marcoRef.upper() == "ARRIBA":
        axisMask = [ motion.AXIS_MASK_VEL ]*2
    elif marcoRef.upper() == "ROBOT":
        axisMask = [ motion.AXIS_MASK_VEL ]*4
    elif marcoRef.upper() == "TORSO":
        axisMask = [ motion.AXIS_MASK_VEL ]*4

#-------------------------------------------------------------------------------
#Obtencion de la informacion del archivo CVS
    print "----------------------------------"
    print "    Starting adjustment of data..."
    #Realiza ajuste de los datos de la grabacion
    csvMocap.startAdjustData(coreo,offFile)

    print "    Adjustment completed."
    print "++++++++++++++++++++++++++++++++++++++++++++++++"
    ##Lista con vectores de las posiciones de los actuadores en orden correspondiente
    ##al orden de los actuadores a utilizar
    print "    Getting coordinates"
    print "------------------------------------------------"
    #Obtiene lista con coordenadas
    listaCoordenadas = csvMocap.getCoordenadas(marcoRef)

    print "    Getting times"
    print "------------------------------------------------"
    ##Lista de Tiempos
    listaTiempos = csvMocap.getTiempos(marcoRef)

    print "    Getting actuator names"
    print "------------------------------------------------"
    ##Lista de Actuadores en el orden a ser usadas
    ###Orden Preferido "RArm", "RLeg", "LLeg", "LArm", "Torso", "Head"
    if marcoRef.upper() == "ROBOT":
        listaActuadores = ["RArm", "LArm", "Head"]
    elif marcoRef.upper() == "TORSO":
        #listaActuadores = ["RArm", "RLeg", "LLeg", "LArm", "Head"]
        listaActuadores = ["RArm", "RLeg", "LLeg", "LArm"]
    elif marcoRef.upper() == "ARRIBA":
        #listaActuadores = ["RArm", "LArm", "Torso"]
        listaActuadores = ["RArm", "LArm"]

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#Control del movimiento del NAO -- Teleoperacion
    #---------------------------------------------------------------------------
    print "++++++++++++++++++++++++++++++++++++++++++++++++"
    print "Setting up movement conditions"
    print "++++++++++++++++++++++++++++++++++++++++++++++++"
    #Preparativos iniciales para mover el NAO

    ##Iniciando motores y activando rigidez para poder iniciar el movimiento
    ##en el NAO, si la rigidez no esta puesta el Nao no se mueve
    #motionProxy.wakeUp()
    print "    Stiffness is ON"
    StiffnessOn(motionProxy)

    print "    NAO standing"
    ##Llevando al NAO a una pose segura para moverse
    postureProxy.goToPosture("StandInit", 0.5)
    #postureProxy.goToPosture("Stand", 0.5) #Pose preferente

    ##Una vez que esta en una posicion segura se puede inhabilitar el contorlador
    ##automatico de caidas, esto para que no restrinja ciertas posiciones del Nao
    ### **Tener en cuenta que ahora corre peligro de caidas daninas, el Nao Debe
    ### estar en un ambiente controlado y el usuario atento a caidas para que
    ### no sufra danos evitables**
    print "++++++++++++++++++++++++++++++++++++++++++++++++"
    print "++++++++++++++++++++++++++++++++++++++++++++++++"
    print "          Disabling Fall Manager            "
    print "                  WARNING:                  "
    print "   NAO wont react automatically to falls.   "
    print "Please take care of the NAO robot during the"
    print "       execution of the teleoperation       "
    print "++++++++++++++++++++++++++++++++++++++++++++++++"
    print "++++++++++++++++++++++++++++++++++++++++++++++++"
    time.sleep(3.0)
    motionProxy.setFallManagerEnabled(False)

    ##Habilita Balanceo de Cuerpo Completo Automatico
    motionProxy.wbEnable(True)

    ##Restriccion de soporte para las piernas
    ###Condicion de operacion
    estadoFijo  = "Fixed" # Posicion Fija
    estadoPlano = "Plane" # Permite desplazamiento sobre el plano
    estadoLibre = "Free"  # Libre movimiento en el espacio
    ###Actuador de soporte
    #### Legs usa ambas piernas, sin embargo se puede manejar la restriccion
    #### para cada pierna de manera independiente
    soportePiernas = "Legs" # Ambas piernas
    soporteIzq     = "LLeg" # Pierna izquierda
    soporteDer     = "RLeg" # Pierna derecha

    ###Habilita soporte de ambas piernas con restricciones
    motionProxy.wbFootState(estadoFijo, soportePiernas)
    ###Para usar piernas con estados individuales
    #motionProxy.wbFootState(estadoFijo, soporteDer)
    #motionProxy.wbFootState(estadoLibre, soporteIzq)

    ##Habilita balance del cuerpo sobre el soporte definido
    soporteActivo = True
    motionProxy.wbEnableBalanceConstraint(soporteActivo, soportePiernas)
    print "    Balance constraints set"

    #---------------------------------------------------------------------------
    print "++++++++++++++++++++++++++++++++++++++++++++++++"
    print "++++++++++++++++++++++++++++++++++++++++++++++++"
    print "NAO movement started..."
    #Inicio del movimiento

    ##Tiempo de espera para iniciar movimiento
    time.sleep(1.0)
    ##Ejecucion de las posiciones obtenidas del archivo csvMocap, todo de un solo
    #motionProxy.positionInterpolations(listaActuadores, referencia, listaCoordenadas, axisMask, listaTiempos, absolutos)
    ##Ejecucion de las posiciones obtenidas del archivo csvMocap, por cuadros (30 FPS)
    fps = 30
    COM = [0.0,0.0,0.0]
    listaTorsoX = list()
    listaTorsoY = list()
    balancePiernas = "centro"

    #motion.wbEnableEffectorOptimization(effectorName, isActive);

    #Utiliza 3 actuadores: RArm, LArm y Torso
    if marcoRef.upper() == "ARRIBA":
        for i in range(0,len(listaCoordenadas[0]),fps):
            #Calcula promedio de la posicion del torso deseada
            #for item in listaCoordenadas[2][i:i+fps-1]:
            #    listaTorsoX.append(item[0])
            #    listaTorsoY.append(item[1])
            #promTorsoX = np.mean(listaTorsoX)
            #promTorsoY = np.mean(listaTorsoY)

            #Obtiene posicion del COM general
            #COM = motionProxy.getCOM("Body",referencia, True)
            #Para apoyarse sobre alguna pierna se analiza donde se va a posicionar al
            #torso sobre el eje Y (izq y der)
            #if promTorsoY < -0.025:
                #motionProxy.wbGoToBalance(soporteDer, 1.0)
            #elif promTorsoY > 0.025:
                #motionProxy.wbGoToBalance(soporteDer, 1.0)
            #else:
                #motionProxy.wbGoToBalance(soportePiernas, 1.0)

            #Luego de evaluar el mejor apoyo para el posicionamiento deseado se
            #realiza el movimiento del resto de los actuadores
            motionProxy.positionInterpolations(listaActuadores, referencia, [
                                                                             listaCoordenadas[0][i:i+fps-1],
                                                                             listaCoordenadas[1][i:i+fps-1]
                                                                            ],
                                                                axisMask,   [
                                                                             listaTiempos[0][0:len(listaCoordenadas[0][i:i+fps-1])],
                                                                             listaTiempos[1][0:len(listaCoordenadas[1][i:i+fps-1])]
                                                                            ],
                                                                absolutos)

    #Utiliza 4 actuadores: RArm, LArm, Torso y Head
    elif marcoRef.upper() == "ROBOT":
        for i in range(0,len(listaCoordenadas[0]),fps):
            motionProxy.positionInterpolations(listaActuadores, referencia,[
                                                                            listaCoordenadas[0][i:i+fps-1],
                                                                            listaCoordenadas[1][i:i+fps-1],
                                                                            listaCoordenadas[2][i:i+fps-1],
                                                                            listaCoordenadas[3][i:i+fps-1]
                                                                          ],
                                                                axisMask, [
                                                                            listaTiempos[0][0:len(listaCoordenadas[0][i:i+fps-1])],
                                                                            listaTiempos[1][0:len(listaCoordenadas[1][i:i+fps-1])],
                                                                            listaTiempos[2][0:len(listaCoordenadas[2][i:i+fps-1])],
                                                                            listaTiempos[3][0:len(listaCoordenadas[3][i:i+fps-1])]
                                                                          ],
                                                                absolutos)


    #Utiliza 6 actuadores: RArm, RLeg, LLeg, LArm, Torso y Head
    elif marcoRef.upper() == "TORSO":
        for i in range(0,len(listaCoordenadas[0]),fps):
            #Calcula promedio de la posicion del torso deseada
            for item in listaCoordenadas[2][i:i+fps-1]:
                listaTorsoX.append(item[0])
                listaTorsoY.append(item[1])
            promTorsoX = np.mean(listaTorsoX)
            promTorsoY = np.mean(listaTorsoY)

            #Obtiene posicion del COM general
            COM = motionProxy.getCOM("Body",referencia, True)
            #Para apoyarse sobre alguna pierna se analiza donde se va a posicionar al
            #torso sobre el eje Y (izq y der)
            if promTorsoY < -0.03:
                if balancePiernas != "der":
                    motionProxy.wbGoToBalance(soporteDer, 0.5)
                    balancePiernas = "der"
            elif promTorsoY > 0.03:
                if balancePiernas != "izq":
                    motionProxy.wbGoToBalance(soporteDer, 0.5)
                    balancePiernas = "izq"
            else:
                if balancePiernas != "centro":
                    motionProxy.wbGoToBalance(soportePiernas, 0.5)
                    balancePiernas = "centro"

            motionProxy.positionInterpolations(listaActuadores, referencia,[
                                                                            listaCoordenadas[0][i:i+fps-1],
                                                                            listaCoordenadas[1][i:i+fps-1],
                                                                            listaCoordenadas[2][i:i+fps-1],
                                                                            listaCoordenadas[3][i:i+fps-1]
                                                                          ],
                                                                axisMask, [
                                                                            listaTiempos[0][0:len(listaCoordenadas[0][i:i+fps-1])],
                                                                            listaTiempos[1][0:len(listaCoordenadas[1][i:i+fps-1])],
                                                                            listaTiempos[2][0:len(listaCoordenadas[2][i:i+fps-1])],
                                                                            listaTiempos[3][0:len(listaCoordenadas[3][i:i+fps-1])]
                                                                          ],
                                                                absolutos)

    print "------------------------------------------------"
    print "NAO movement ended. Resting NAO."
    print "++++++++++++++++++++++++++++++++++++++++++++++++"
    print "++++++++++++++++++++++++++++++++++++++++++++++++"
    ##Tiempo de espera entre ultimo movimiento y estado de reposo del Nao, para
    ##agregar estabilidad
    time.sleep(2.0)

    print "    NAO moving to posture: Crouch"
    print "------------------------------------------------"
    ##Posicion de reposo seguras para finalizar la accion
    postureProxy.goToPosture("Crouch", 0.5)

    #Se habilita nuevamente el controlador automatico de caidas
    ##****IMPORTANTE REALIZAR ESTE PASO****##
    motionProxy.setFallManagerEnabled(True)
    ##Desactiva Balance de Cuerpo Completo **Debe ir al final del movimiento**
    motionProxy.wbEnable(False)
    print "**********************"
    print "Fall Manager Enabled"
    print "**********************"

    motionProxy.rest() # Apaga los motores del Nao
    ## **Si no se apagan es posible que se sobrecalienten aun estando en reposo**
    print "    NAO is resting."
    print "++++++++++++++++++++++++++++++++++++++++++++++++"
    print "Teleoperation ended."
    print "++++++++++++++++++++++++++++++++++++++++++++++++"
    print "++++++++++++++++++++++++++++++++++++++++++++++++"

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
if __name__ == "__main__":
    robotIp = "10.0.1.128" #Bato por red PrisNao
    #robotIp = "169.254.42.173" #Bato Local
    coreo = ""
    marcoRef = "ROBOT"
    offFile = "offsets.csv"

    if len(sys.argv) == 4:
        robotIp  = sys.argv[1]
        coreo    = sys.argv[2]
        marcoRef = sys.argv[3]
        print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
        print "Using robot IP:", robotIp
        print "Choreography file to read:", coreo
        print "Using reference plane:", marcoRef
        print "Using calibration data from default:", offFile
        print "------------------------------------"
        print "Initializing Teleoperation with Data from a MoCap recording"
        print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
        time.sleep(1.5) #Tiempo para que el usuario lea las indicaciones
    elif len(sys.argv) == 5:
        robotIp  = sys.argv[1]
        coreo    = sys.argv[2]
        marcoRef = sys.argv[3]
        offFile  = sys.argv[4]
        print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
        print "Using robot IP:", robotIp
        print "Choreography file to read:", coreo
        print "Using reference plane:", marcoRef
        print "Using calibration data from file:", offFile
        print "------------------------------------"
        print "Initializing Teleoperation with Data from a MoCap recording"
        print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
        time.sleep(1.5) #Tiempo para que el usuario lea las indicaciones
    else:
        error.abort("Expected 3 or 4 arguments on call.", "Move")

    main(robotIp,coreo,marcoRef,offFile)
