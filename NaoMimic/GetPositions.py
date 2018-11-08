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
import Error_Utils as error
import CSV_Utils as csvUtils

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
    except Exception as e:
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
                "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++" +
                "Writing CSV file with the data collected.")
        time.sleep(0.25)
        pass
    dataSet = [posHead, posTorso, posRArm, posLArm]
    csvUtils.writeCSVReference(dataSet, name, refFrame, specificEffectors)

    print("Finish GetPositions routine" +
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
            "\nName of CSV file: NAO_" + name +
            "\n---------------------------------------------------------\n"+
            "Starting to retrieve sensor values\n"+
            "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    elif len(sys.argv) == 5:
        robotIP = sys.argv[1]
        frame = sys.argv[2]
        name = sys.argv[3]
        specificEffectors = sys.argv[4]
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n" +
            "Using robot IP: " + robotIP + " with frame: " + frameRef
              )
        if name is None:
            print("\nName of CSV file defined by time and date\n")
        else:
            print("\nName of CSV file: NAO_" + name)
        print("\n---------------------------------------------------------\n" +
        "Starting to retrieve sensor values\n" +
        "\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
              )
    else:
        error.abort("Expected 2 to 4 arguments on call.", "GetPositions")

    time.sleep(1.0)
    main(robotIP, frameRef, name, specificEffectors)
