"""
Used to capture the position data of the respective end effectors of the 6 humanoid robot Nao's chains
(in this order of appearance HEAD, TORSO, RARM, LARM, RLEG, LLEG). The user decides when to stop the capture of data, then it exports
it in a CSV file to the reference data specified path. The info includes coordinates XYZ (+rotaction).

"""

#External Libraries
from naoqi import ALProxy
import motion
import sys
import time
import csv
import os
from os.path import dirname, abspath

#Project Libraries
import Libraries.Error_Func as error

#----------------------------------------------------------------------------------------------------------------------
def main(robotIP, refFrame, name=None, specificEffectors="ALL"):
    """
    :param robotIP: IP of the Nao robot to connect to.
    :param frameRef: Name of the reference frame for the data collection ("ROBOT" or "TORSO").
    :param name: Name of the exported CSV file.
    :param specificEffectors: List of specific effectors to collect data. Separate each end effector with a "/". If
            "ALL" is used, all available chain effectors are used.
    """
    PORT = 9559
    print("Using Port:", PORT)

    try:
        print("Trying to create ALMotion proxy")
        motionProxy = ALProxy("ALMotion", robotIP, PORT)
    except Exception,e:
        print("Could not create proxy to ALMotion")
        print("Error was: ", e)
        sys.exit(1)

    #-------------------------------------------------------------------------------
    # Reference frame definition
    if refFrame.upper() == "ROBOT":
        frame = motion.FRAME_ROBOT
    elif refFrame.upper() == "TORSO":
        frame = motion.FRAME_TORSO
    else:
        error.abort("is not a valid frame for function", refFrame, "GetPositions")
    #True to use sensor aproximaiton of values
    useSensorValues = False

    # -------------------------------------------------------------------------------
    # Get effectors to collect
    effectors = []
    if specificEffectors.upper() != "ALL":
        effectors = specificEffectors.split("/")
        for item in effectors:
            if (
                item != "HEAD" or item != "TORSO" or item != "ARMS" or item != "RARM" or item != "LARM"
                or item != "LEGS" or item != "RLEG" or item != "LLEG"
            ):
                error.abort("is not a valid end effector", item, "GetPositions")
    else:
        effectors = ["HEAD", "TORSO", "RARM", "LARM"]
        # effectors = ["HEAD", "TORSO", "RARM", "LARM", "RLEG", "LLEG"]

    #-------------------------------------------------------------------------------
    # Create single array per chain effector
    posHead  = []
    posTorso = []
    posRArm  = []
    posLArm  = []
    # posRLeg  = []
    # posLLeg  = []
    rows = 0

    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"+
            "Starting to collect data, interrupt the process only if necessary.\n"+
            "Press Ctrl+C anytime to stop collecting data and proceed with data export.\n"+
            "Wait for completion...\n\n")
    time.sleep(0.5)

    #Data collection
    try:
        while (True):
            posHead.append(motionProxy.getPosition("Head", frame, useSensorValues))
            posTorso.append(motionProxy.getPosition("Torso", frame, useSensorValues))
            posRArm.append(motionProxy.getPosition("RArm", frame, useSensorValues))
            posLArm.append(motionProxy.getPosition("LArm", frame, useSensorValues))
            # posRLeg.append(motionProxy.getPosition("RLeg", frame, useSensorValues))
            # posLLeg.append(motionProxy.getPosition("LLeg", frame, useSensorValues))
            time.sleep(0.003) #This time matches the FPS used on Motive's export
            rows +=1
    except KeyboardInterrupt:
        print("Data collection finished.\n"+
                "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"+
                "Writing CSV file with the data collected.")
        time.sleep(0.25)
        pass
    #-------------------------------------------------------------------------------
    # CSV file export
    #
    # Header format goes as follows:
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Effector1  ,Effector1,Effector1,Effector1,Effector1,Effector1,Effector2,...
    # rotX       ,rotY     ,rotZ     ,posX     ,posY     ,posZ     ,rotX     ,...
    # valTake1   ,valTake1 ,valTake1 ,valTake1 ,valTake1 ,valTake1 ,valTake1 ,...
    # valTake2   ,valTake2 ,valTake2 ,valTake2 ,valTake2 ,valTake2 ,valTake2 ,...
    # ...
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # Default directory for files storage
    rootDir = dirname(dirname(abspath(__file__)))
    fileDir = os.path.join(rootDir, "Calibration/NAO/ReferenceData_Default/")
    if os.path.isdir(archivo) == False:
        error.abort("Directory "+fileDir+" does not exist\n")
    # Add name of the file
    if name is None:
        fileDir += frame
        fileDir += time.strftime("_%Y-%m-%d_%H-%M-%S")
    else:
        fileDir += name
        fileDir += ".csv"

    # Create the CSV file
        with open(fileDir, 'w') as csvfile:
            # Define columns
            fieldnames = []
            header = []
            if specificEffectors == "ALL":
                fieldnames = [
                    'WX Head', 'WY Head', 'WZ Head', 'X Head', 'Y Head', 'Z Head',
                    'WX Torso', 'WY Torso', 'WZ Torso', 'X Torso', 'Y Torso', 'Z Torso',
                    'WX RArm', 'WY RArm', 'WZ RArm', 'X RArm', 'Y RArm', 'Z RArm',
                    'WX LArm', 'WY LArm', 'WZ LArm', 'X LArm', 'Y LArm', 'Z LArm',
                    # 'WX RLeg', 'WY RLeg', 'WZ RLeg', 'X RLeg', 'Y RLeg', 'Z RLeg',
                    # 'WX LLeg', 'WY LLeg', 'WZ LLeg', 'X LLeg', 'Y LLeg', 'Z LLeg',
                              ]
            elif specificEffectors == "ARMS":
                fieldnames = [
                    'WX RArm', 'WY RArm', 'WZ RArm', 'X RArm', 'Y RArm', 'Z RArm',
                    'WX LArm', 'WY LArm', 'WZ LArm', 'X LArm', 'Y LArm', 'Z LArm',
                ]
            elif (
                specificEffectors == "HEAD" or specificEffectors == "TORSO" or specificEffectors == "RARM" or
                specificEffectors == "LARM" or specificEffectors == "RLEG" or specificEffectors == "LLEG"
                ):
                fieldnames = [
                    'WX', 'WY', 'WZ', 'X', 'Y', 'Z'
                ]

            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Write header info
            writer.writerow(effectors)
            writer.writeheader()
            # Write rows with data
            for i in range(rows):
                writer.writerow({
                    'WX Head': posHead[i][3], 'WY Head': posHead[i][4], 'WZ Head': posHead[i][5],
                        'X Head': posHead[i][0], 'Y Head': posHead[i][1], 'Z Head': posHead[i][2],
                    'WX Torso': posHead[i][3], 'WY Torso': posHead[i][4], 'WZ Torso': posHead[i][5],
                        'X Torso': posHead[i][0], 'Y Torso': posHead[i][1], 'Z Torso': posHead[i][2],
                    'WX RArm': posHead[i][3], 'WY RArm': posHead[i][4], 'WZ RArm': posHead[i][5],
                        'X RArm': posHead[i][0], 'Y RArm': posHead[i][1], 'Z RArm': posHead[i][2],
                    'WX LArm': posHead[i][3], 'WY LArm': posHead[i][4], 'WZ LArm': posHead[i][5],
                        'X LArm': posHead[i][0], 'Y LArm': posHead[i][1], 'Z LArm': posHead[i][2],
                    # 'WX RLeg': posHead[i][3], 'WY RLeg': posHead[i][4], 'WZ RLeg': posHead[i][5],
                    #     'X RLeg': posHead[i][0], 'Y RLeg': posHead[i][1], 'Z RLeg': posHead[i][2],
                    # 'WX LLeg': posHead[i][3], 'WY LLeg': posHead[i][4], 'WZ LLeg': posHead[i][5],
                    #    'X LLeg': posHead[i][0], 'Y LLeg': posHead[i][1], 'Z LLeg': posHead[i][2],
                                })

    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\nFile exported as: "+fileDir+
          "\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
if __name__ == "__main__":
    robotIP = "10.0.1.128" #Based on PrisNao network
    frameRef = "ROBOT"
    name = None
    specificEffectors = "ALL"

    if len(sys.argv) == 3:
        robotIP = sys.argv[1]
        frame = sys.argv[2]
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"+
            "Using robot IP: "+ robotIP +" with frame: "+ frameRef +
            "Collecting data for all available effectors.n"+
            "\nName of CSV file defined by time and date\n"+
            "---------------------------------------------------------\n"+
            "Starting to retrieve sensor values\n"+
            "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    elif len(sys.argv) == 4:
        robotIP = sys.argv[1]
        frame = sys.argv[2]
        name = sys.argv[3]
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n" +
            "Using robot IP: " + robotIP + " with frame: " + frameRef +
              "Collecting data for all available effectors.n"+
            "\nName of CSV file: NAO_"+ name +
            "\n---------------------------------------------------------\n"+
            "Starting to retrieve sensor values\n"+
            "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    elif len(sys.argv) == 5:
        robotIP = sys.argv[1]
        frame = sys.argv[2]
        name = sys.argv[3]
        specificEffectors = sys.argv[4]
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n" +
            "Using robot IP: " + robotIP + " with frame: " + frameRef)
            if name is None:
                print("\nName of CSV file defined by time and date\n")
            else:
                print("\nName of CSV file: NAO_" + name)
            print("\n---------------------------------------------------------\n"+
            "Starting to retrieve sensor values\n"+
            "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    else:
        error.abort("Expected 2 to 4 arguments on call.", "GetPositions")

    time.sleep(1.0)
    main(robotIP, frameRef, name, specificEffectors)
