"""
This script is used to start a Mimic operation with the desired Nao robot.
Some info:
    - Reference frames: motion.FRAME_TORSO references to Nao's TORSO. Value: 0
                        motion.FRAME_WORLD references to initial state of Nao.  Value: 1
                        motion.FRAME_ROBOT references to a virtual origin calculated as the approximated center point
                                            between the Nao's feet location. Value: 2
    - Degrees of Freedom: Defined by the addition of each axis vector to control: 7 for position only, 56 for rotation
                        only and 63 for position and rotations (all three considers X, Y, Z).
                            motion.AXIS_MASK_ALL = 63
                            motion.AXIS_MASK_VEL = 56
"""

# Imports
import time
import motion
import sys

# Project libraries
from Libraries import Miscellaneous_Utils as misc
from Libraries import Nao_Utils as naoUtils
from Libraries import Mimic_Utils as mimic

# ----------------------------------------------------------------------------------------------------------------------


def main(choreographyName, pathCP, robotIP, refFrame, effectorsToUse = "UPPER"):

    print("\n\n\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
          + "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
          + "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
          + "                        NAO MIMIC INITIATED                        ")
    time.sleep(3)

    # Create motion and posture proxies
    print("\n\n------------------------------------------------------------------\n"
          + "------------------------------------------------------------------\n"
          + "Creating Motion and Posture proxies"
          + "\n------------------------------------------------------------------\n"
          + "------------------------------------------------------------------\n")
    motionProxy = naoUtils.createALProxy("ALMotion", robotIP)
    postureProxy = naoUtils.createALProxy("ALRobotPosture", robotIP)

    # -------------------------------------------------------------------------------

    # Mimic settings
    print("\n\n------------------------------------------------------------------\n"
          + "------------------------------------------------------------------\n"
          + "Setting NAO MIMIC environment"
          + "\n------------------------------------------------------------------\n"
          + "------------------------------------------------------------------\n")
    # # Reference frame to use
    if refFrame.upper() == "TORSO":
        referenceFrame = motion.FRAME_TORSO
        print("------------------------------------------------------------------\n"
              + "Reference frame to use: TORSO")
    elif refFrame.upper() == "ROBOT":
        referenceFrame = motion.FRAME_ROBOT
        print("------------------------------------------------------------------\n"
              + "Reference frame to use: ROBOT")
    else:
        misc.abort("Did not receive a valid Reference Frame", "Setting NAO MIMIC environment")
    print("Nao robot IP: " + robotIP
          + "\nCalibration Profile: " + pathCP
          + "\nName of choreography file to Mimic: " + choreographyName)

    # # True to use absolute positions
    useAbsoluteValues = True

    # # Degrees of freedom. Must include one definition per effector
    axisMask = [motion.AXIS_MASK_VEL] * 4

    # # Define effectors list
    effectorsList = ["Head", "Torso", "RArm", "LArm"]
    print("Effectors to control: " + effectorsList[0] + effectorsList[1] + effectorsList[2] + effectorsList[3])

    # # Frame per Seconds used on MoCap exported data
    fps = 30
    print("FPS: " + str(fps))

    print("\n------------------------------------------------------------------")
    time.sleep(3)

    # -------------------------------------------------------------------------------

    # Adjust choreography to mimic according to specified calirbation profile
    print("\n\n------------------------------------------------------------------\n"
          + "------------------------------------------------------------------\n"
          + "Using specified calibration profile to adjust\n" + choreographyName + " motion data"
          + "\n------------------------------------------------------------------\n"
          + "\n------------------------------------------------------------------\n")
    adjustedChoreography = mimic.adjustChoreography(choreographyName, pathCP)

    # # Timeline
    timeline = mimic.getFixedTimeline(adjustedChoreography[0])

    # -------------------------------------------------------------------------------

    # Set the robot ready for Mimic operations
    print("\n\n------------------------------------------------------------------\n"
          + "------------------------------------------------------------------\n"
          + "Setting the robot ready to start with Mimic operations"
          + "\n------------------------------------------------------------------\n"
          + "\n------------------------------------------------------------------\n")
    naoUtils.setNaoReadyToMimic(motionProxy, postureProxy)

    # -------------------------------------------------------------------------------

    # Start Mimicking
    print("\n\n------------------------------------------------------------------\n"
          + "------------------------------------------------------------------\n"
          + "Nao is Mimicking human motion in choreography...\n\n\n")
    time.sleep(1)

    naoUtils.mimicFullChoreography(motionProxy, postureProxy, adjustedChoreography, effectorsList, timeline, axisMask,
                                   referenceFrame, useAbsoluteValues, fps)

    # -------------------------------------------------------------------------------

    # Rest the Nao
    print("...finished Mimic activity"
          + "\n------------------------------------------------------------------\n"
          + "\n------------------------------------------------------------------\n")
    naoUtils.restNao()

    print("\n\n                         NAO MIMIC ENDED                         "
          + "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
          + "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
          + "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")

# ----------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    # robotIp = "10.0.1.128"  # Bato por red PrisNao
    # robotIp = "169.254.42.173" # Bato Local
    # robotIP = "10.0.1.122"  # She por red PrisNao
    robotIP = "10.0.1.193"  # Mok
    refFrame = "ROBOT"
    choreographyName = ""
    pathCP = ""

    if len(sys.argv) < 3:
        misc.abort("Needs Minimum of 2 arguments to start: Coreography to Mimic and Calibration Profile")
    elif len(sys.argv) == 3:
        choreographyName = sys.argv[1]
        pathCP = sys.argv[2]
    elif len(sys.argv) == 5:
        choreographyName = sys.argv[1]
        pathCP = sys.argv[2]
        robotIP = sys.argv[3]
        marcoRef = sys.argv[4]

    main(choreographyName, pathCP, robotIP, refFrame)
