"""
Supports Nao interfacing. Uses naoqi methods
"""

# Imports
import time
from naoqi import ALProxy

# Project libraries
from Libraries import Miscellaneous_Utils as misc

# ----------------------------------------------------------------------------------------------------------------------


def startCollectingData(motionProxy, frame = "ROBOT", useSensorValues = False):
    """
    This function is used to extract data from the Nao effector's sensors.

    :param motionProxy: ALMotion proxy object.
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


def setStiffness(motionProxy, stiffnessOn = True):
    """
    This function is used to toggle stiffness of Nao robot. Duration of transition is set to 1 second.

    :param motionProxy: ALMotion proxy object.
    :param stiffnessOn: True to set stiffness On, False to turn it Off.
    :return: void
    """
    bodySection = "Body"  # Sets stiffnes for the whole body
    # Stiffness value
    stiffnessValue = 1.0 if stiffnessOn else 0.0
    time = 1.0  # In seconds
    stiffnessState = "On" if stiffnessOn else "Off"

    print("Turning Nao's stiffness " + stiffnessState)
    motionProxy.stiffnessInterpolation(bodySection, stiffnessValue, time)

# ----------------------------------------------------------------------------------------------------------------------


def setNaoReadyToMimic(motionProxy, postureProxy):
    """
    This function is used to set ready the Nao prior to the Mimicking operations. Disables Fall Manager and enables
    Whole Body Manager. Sends Nao to predefined position STANDINIT.

    :param motionProxy: ALMotion proxy object.
    :param postureProxy: ALPosture proxy object.
    :return: void.
    """

    # Set stiffness On
    print("\n------------------------------------------------------------------\n"
          + "Set stiffness On")
    setStiffness(motionProxy)

    # Set the robot to a safe position
    print("\n------------------------------------------------------------------\n"
          + "Moving Nao to position: STANDINIT")
    postureProxy.goToPosture("StandInit", 0.5)

    # Disable Fall Manager
    print("\n******************************************************************"
          + "\n******************************************************************"
          + "\n******************************************************************"
          + "\n*                  Disabling Nao's Fall Manager                  *"
          + "\n*                           WARNING!!!                           *"
          + "\n*       NAO WONT REACT AUTOMATICALLY TO PROTECT FROM FALLS       *"
          + "\n*       PLEASE TAKE CARE OF THE NAO'S INTEGRITY DURING THE       *"
          + "\n*               EXECUTION OF THE MIMICKING PROCESS               *"
          + "\n******************************************************************"
          + "\n******************************************************************"
          + "\n******************************************************************")
    time.sleep(3.0)
    motionProxy.setFallManagerEnabled(False)

    # Enable Nao's Whole Body Balancer
    print("\n------------------------------------------------------------------\n"
          + "Enabling Whole Body Balance Manager")
    motionProxy.wbEnable(True)

    # # Setting balance constraints
    # # # Plane constraints
    fixedConstraint = "Fixed"  # Fixed feet position
    # planeConstraint = "Plane"  # Feet free to move along the virtual floor plane
    # freeConstraint = "Free"  # Feet free to move along the 3D space

    # # # Support effector for constraint
    supportLegs = "Legs"  # Both legs
    supportLLeg = "LLeg"  # Left leg
    supportRLeg = "RLeg"  # Right leg

    # # # Enable balance contraints for specified support effector
    motionProxy.wbFootState(fixedConstraint, supportLegs)
    # motionProxy.wbFootState(planeConstraint, supportRLeg)
    # motionProxy.wbFootState(planeConstraint, supportLLeg)

    # # Enable balance management over specified constraints
    activateConstraintsSupport = True
    motionProxy.wbEnableBalanceConstraint(activateConstraintsSupport, supportLegs)

    print("\nNao robot is ready to start Mimicking operation"
          + "\n------------------------------------------------------------------")

# ----------------------------------------------------------------------------------------------------------------------


def restNao(motionProxy, postureProxy):
    """
    This function is used to rest the Nao's motors. Enables Fall Manager and disables Whole Body Balancing. Sends the
    Nao to predefined position CROUCH.

    :param motionProxy: ALMotion proxy object.
    :param postureProxy: ALPosture proxy object.
    :return: void.
    """

    print("\n\n------------------------------------------------------------------"
          + "\nResting the Nao robot"
          + "\n------------------------------------------------------------------")

    # Stabilization time
    time.sleep(3.0)

    # Enable Fall Manager
    print("\n------------------------------------------------------------------\n"
          + "Enabling Nao's Fall Manager")
    motionProxy.setFallManagerEnabled(True)

    # Disable Nao's Whole Body Balancer
    print("\n------------------------------------------------------------------\n"
          + "Disabling Whole Body Balance Manager")
    motionProxy.wbEnable(False)

    # Moving Nao to safe position
    print("\n------------------------------------------------------------------\n"
          + "Moving Nao to position: CROUCH")
    postureProxy.goToPosture("Crouch", 0.5)

    # Resting Nao's motors
    motionProxy.rest()
    print("\n------------------------------------------------------------------\n"
          + "The Nao's motors are in state REST")

# ----------------------------------------------------------------------------------------------------------------------


def createALProxy(naoqiProxyName, robotIP, proxyPort = 9559):
    """
    This function is used to create a Naoqi proxy object.

    :param naoqiProxyName: AL proxy name. Must match the expected name according to Nao's documentation.
    :param robotIP: IP address of the Nao robot.
    :param proxyPort: Port for the proxy to use on communication.
    :return newALProxy: The proxy object.
    """

    print("\n\n------------------------------------------------------------------"
          + "Creating NAO proxy " + naoqiProxyName)
    try:
        newALProxy = ALProxy(naoqiProxyName, robotIP, proxyPort)
        print(naoqiProxyName + " creation successfully"
              + "\n\n------------------------------------------------------------------")
    except Exception as e:
        misc.abort("Could not create proxy " + naoqiProxyName, None, e)

    return newALProxy

# ----------------------------------------------------------------------------------------------------------------------


def mimicFullChoreography(motionProxy, postureProxy, adjustedChoreography, effectorsList, timeline, axisMask, frame,
                          useAbsolutes = True, fps = 30):

    # Define operation parameters

    for i in range(0, len(adjustedChoreography[0]), fps):
        try:
            motionProxy.positionInterpolations(effectorsList, frame, [
                listaCoordenadas[0][i:i + fps - 1],
                listaCoordenadas[1][i:i + fps - 1],
                listaCoordenadas[2][i:i + fps - 1],
                listaCoordenadas[3][i:i + fps - 1]
            ],
                                               axisMask, [
                listaTiempos[0][0:len(listaCoordenadas[0][i:i + fps - 1])],
                listaTiempos[1][0:len(listaCoordenadas[1][i:i + fps - 1])],
                listaTiempos[2][0:len(listaCoordenadas[2][i:i + fps - 1])],
                listaTiempos[3][0:len(listaCoordenadas[3][i:i + fps - 1])]
            ],
                                               useAbsolutes)
        except Exception as e:
            misc.abortMimic(motionProxy, postureProxy, e)

    time.sleep(1)

# ----------------------------------------------------------------------------------------------------------------------
