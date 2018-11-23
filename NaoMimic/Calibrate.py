#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#Utiliza las funciones definidas en CalibrateFunc.py para realizar el proceso de
#calibracion para la teleoperacion del NAO, los factores generados por este
#proceso son usados en CSV_read.py para el ajuste de las coordenadas.
##
#Realiza la calibracion segun las grabaciones de datos para calibrar dentro del
#directorio local ../Calibration/NAO para las del robot NAO, y ../Calibration/Human para las de
#la persona. Las grabaciones del NAO son predefinidas, las de la persona en
#utilizar el sistema deben obtenerse de grabaciones previas al proceso de
#calibracion.
##
#El directorio donde se encuentran los datos de la persona se debe especificar
#y estar contenido en .../Calibration/Human con las grabaciones requeridas, cuyos nombres
#deben seguir el formato *LetraMayusculaIndicandoPrueba*_Cal_P.csv, con la
#letra en mayusucla correspondiente a la pose de calibracion del NAO.
#Si no se especifica directorio se considera que se usan los archivos predefinidos
#dentro de .../Calibration/Human
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#Imports
import sys
import time

##Custom
import Calibration_Utils as cal
import Miscellaneous_Utils as error
import CSV_Utils as csvUtils


#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
def main(polDeg, wRot, humanDir, ID, naoDir):
    #Datos para calibrar el movimiento de los brazos
    ###Obtiene datos desde los csv correspondientes para la primer pose de calibracion
    HeadNao, TorsoNao, RArmNao, LArmNao = csvUtils.readCSVNao( naoDir + "/" + "Brazos_NAO.csv")
    HeadP, TorsoP, RArmP, LArmP = csvUtils.readCSVMocap(humanDir + "/" + "Brazos_P.csv")

    ##Obtiene factores para la regresion polinomial deseada para el ajuste
    factRArm  = cal.getCalibrationTerms(RArmNao, RArmP)
    factLArm  = cal.getCalibrationTerms(LArmNao, LArmP)

    #---------------------------------------------------------------------------
    #---------------------------------------------------------------------------
    #Genera archivo CSV con los offsets finales a utilizar
    print( "++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print( "Writing offsets to file: .../Calibration/Offsets/offsets_"+ID+".csv")
    try:
        csvUtils.writeCalibrationProfile([factRArm, factLArm])
    except Exception:
        error.abort("Offset write unsuccessfull", "not valid parameters to function","OffsetFileFunc", "Calibrate")
    print( "Done")
    print( "++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print( "++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
if __name__ == "__main__":
    polDeg   = 2 #Polinomio grado 2 por defecto
    humanDir = ""
    naoDir = "RigidBody_Default"
    wRot = "yes"
    ID = ""

    if len(sys.argv) == 4:
        try:
            polDeg   = int(sys.argv[1])
            wRot     = (sys.argv[2]).lower()
            humanDir = sys.argv[3]
            print( "++++++++++++++++++++++++++++++++++++")
            print( "Using Pol degree:", polDeg)
            print( "Include rotations:", wRot)
            print( "Reading Human data from dir:", humanDir)
            print( "Reading NAO data from default directory .../Calibration/Nao/RigidBody_Default")
            print( "------------------------------------")
            print( "Starting calibration process...")
            print( "++++++++++++++++++++++++++++++++++++")
        except ValueError as e:
            error.abort("Expected int as argument in main function", None,"Calibrate")
    elif len(sys.argv) == 5:
        try:
            polDeg   = int(sys.argv[1])
            wRot     = (sys.argv[2]).lower()
            humanDir = sys.argv[3]
            ID       = sys.argv[4]
            print( "++++++++++++++++++++++++++++++++++++")
            print( "Using Pol degree:", polDeg)
            print( "Include rotations:", wRot)
            print( "Reading Human data from dir:", humanDir)
            print( "Reading NAO data from dir:", naoDir)
            print( "Adding extension name to offsets file:", ID)
            print( "------------------------------------")
            print( "Starting calibration process...")
            print( "++++++++++++++++++++++++++++++++++++")
            time.sleep(1.5) #Tiempo para que el usuario lea las indicaciones
        except ValueError as e:
            error.abort("Expected int as argument in main function", None,"Calibrate")
    elif len(sys.argv) == 6:
        try:
            polDeg = int(sys.argv[1])
            wRot     = (sys.argv[2]).lower()
            humanDir = sys.argv[3]
            ID       = sys.argv[4]
            naoDir   = sys.argv[5]
            print( "++++++++++++++++++++++++++++++++++++")
            print( "Using Pol degree:", polDeg)
            print( "Include rotations:", wRot)
            print( "Reading Human data from dir:", humanDir)
            print( "Reading NAO data from dir:", naoDir)
            print( "Adding extension name to offsets file:", ID)
            print( "------------------------------------")
            print( "Starting calibration process...")
            print( "++++++++++++++++++++++++++++++++++++")
            time.sleep(1.5) #Tiempo para que el usuario lea las indicaciones
        except ValueError as e:
            error.abort("Expected int as argument in main function", None,"Calibrate")
    else:
        error.abort("Expected 3, 4 or 5 arguments on call.", None, "Calibrate")

    time.sleep(1.0)
    main(polDeg, wRot, humanDir, ID, naoDir)
