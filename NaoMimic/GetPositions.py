"""
This script is used to capture the position data of the respective end effectors of the 6 humanoid robot Nao's chains
(in this order of appearance HEAD, TORSO, RARM, LARM, RLEG, LLEG). The user decides when to stop the capture of data,
then it exports it in a CSV file to the reference data specified path. The info includes coordinates XYZ +rotaction.
"""

# Imports
from naoqi import ALProxy
import motion
import sys
import time

# Project Libraries
from Libraries import Miscellaneous_Utils as misc
from Libraries import CSV_Utils as csvUtils
from Libraries import Nao_Utils as naoUtils

# ----------------------------------------------------------------------------------------------------------------------


def main(robotIP, refFrame, name, specificEffectors):
    """
    See file header description.

    :param robotIP: IP of the Nao robot to connect to.
    :param frameRef: Name of the reference frame for the data collection ("ROBOT" or "TORSO").
    :param name: Name of the exported CSV file.
    """

    PORT = 9559
    print("Using Port:", PORT)

    try:
        print("Trying to create ALMotion proxy")
        motionProxy = ALProxy("ALMotion", robotIP, PORT)
    except Exception as e1:
        misc.abort("Could not create proxy to ALMotion", "Creating ALMotion proxy to Get Nao Positions", e1)

    # -------------------------------------------------------------------------------

    # Reference frame definition
    if refFrame.upper() == "ROBOT":
        frame = motion.FRAME_ROBOT
    elif refFrame.upper() == "TORSO":
        frame = motion.FRAME_TORSO
    else:
        misc.abort(refFrame + " is not a valid frame", "Get Nao Positions")

    # -------------------------------------------------------------------------------

    # Data collection
    dataSet = naoUtils.startCollectingData(motionProxy, frame)

    # Write file
    print("Writing CSV file with the data collected")
    csvUtils.writeCSVReference(dataSet, name, refFrame, specificEffectors)

    print("Finish GetPositions routine\nCheck for exported data at Calibration/NAO/ReferenceData/Default/"
          + "\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

# -------------------------------------------------------------------------------


if __name__ == "__main__":
    robotIP = "10.0.1.193" # Mok on PrisNao network
    frameRef = "ROBOT"
    name = None
    specificEffectors = "ALL"

    if len(sys.argv) < 3:
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
              + "Using robot IP: " + robotIP +" with frame: " + frameRef
              + "\nCollecting data for all available effectors"
              + "\nName of CSV file defined by time and date\n"
              + "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    elif len(sys.argv) == 3:
        robotIP = sys.argv[1]
        frame = sys.argv[2]
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
              + "Using robot IP: " + robotIP +" with frame: " + frameRef
              + "Collecting data for all available effectors."
              + "\nName of CSV file defined by time and date\n"
              + "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    elif len(sys.argv) == 4:
        robotIP = sys.argv[1]
        frame = sys.argv[2]
        name = sys.argv[3]
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
              + "Using robot IP: " + robotIP + " with frame: " + frameRef
              + "Collecting data for all available effectors.n"
              + "\nName of CSV file: NAO_" + name
              + "\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    else:
        print("\nRetrieving canceled\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
        misc.abort("Expected maximum 3 arguments on call.", "GetPositions")

    time.sleep(1.0)
    main(robotIP, frameRef, name, specificEffectors)
