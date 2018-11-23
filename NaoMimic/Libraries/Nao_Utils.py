"""
Functions to support Nao interfacing.
"""

# Imports
import time

# Project libraries

# ----------------------------------------------------------------------------------------------------------------------

def startCollectingData(motionProxy, frame = "ROBOT", useSensorValues = False):
    """
    This function is used to extract data from the Nao effector's sensors.

    :param frame: Reference frame from which the data collected is referenced to.
    :param useSensorValues: Set to True to use sensor approximations for values collected.
    :return dataCollected: List with the data collected from each effector. The order of the axes is as follows:
                X, Y, Z, WX, WY, WZ
    """

    # Create single list per chain effector
    posHead = list()
    posTorso = list()
    posRArm = list()
    posLArm = list()
    # posRLeg  = list()
    # posLLeg  = list()

    rowsCounter = 0
    print("\n\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
          + "Starting to collect data, interrupt the process only if necessary.\n"
          + "Press Ctrl+C anytime to stop collecting data and proceed with data export.\n"
          + "Wait for completion...\n\n")

    # Data collection
    try:
        while (True):
            posHead.append(motionProxy.getPosition("Head", frame, useSensorValues))
            posTorso.append(motionProxy.getPosition("Torso", frame, useSensorValues))
            posRArm.append(motionProxy.getPosition("RArm", frame, useSensorValues))
            posLArm.append(motionProxy.getPosition("LArm", frame, useSensorValues))
            # posRLeg.append(motionProxy.getPosition("RLeg", frame, useSensorValues))
            # posLLeg.append(motionProxy.getPosition("LLeg", frame, useSensorValues))
            time.sleep(0.003)  # This time matches the FPS used on Motive's export
            rowsCounter += 1

    except KeyboardInterrupt as keyInterrupt:
        print("Data collection finished.\n"
              + "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n\n")
        time.sleep(0.25)
        pass

    dataCollected = [posHead, posTorso, posRArm, posLArm]
    return dataCollected

# ----------------------------------------------------------------------------------------------------------------------
