# -*- encoding: UTF-8 -*-

import time
import motion
import argparse
from naoqi import ALProxy

def main(robotIP, PORT=9559):
    #Instance of naoqi modules
    motionProxy  = ALProxy("ALMotion", robotIP, PORT)
    postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)

    # Wake up robot
    motionProxy.wakeUp()

    # Send robot to Pose Init
    postureProxy.goToPosture("StandInit", 0.5)

    # Set LArm Position, using a fraction of max speed
    chainName = "LArm"
    frame     = motion.FRAME_TORSO
    useSensor = False

    # Get the current position of the chainName in the same frame
    current = motionProxy.getPosition(chainName, frame, useSensor)

    target = [
        current[0] + 0.1,
        current[1] + 0.1,
        current[2] + 0.3,
        current[3] + 0.5,
        current[4] + 0.0,
        current[5] + 0.0]

    fractionMaxSpeed = 0.3
    #axisMask         = 7 # just control position
    axisMask         = 63 # control position and rotation



    #time.sleep(3.0)

    # Example showing how to set Torso Position, using a fraction of max speed
    chainName2        = "Torso"
    frame            = motion.FRAME_ROBOT
    position         = [0.25, 0.3, 0.4, 0.0, 0.0, 0.0] # Absolute Position
    fractionMaxSpeed = 0.2
    axisMask         = 63
    motionProxy.setPositions(chainName, frame, target, fractionMaxSpeed, axisMask)
    motionProxy.setPositions(chainName2, frame, position, fractionMaxSpeed, axisMask)

    time.sleep(1.0)

    # Go to rest position
    motionProxy.rest()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.18.214",
                        help="Robot ip address")
    parser.add_argument("--port", type=int, default=9559,
                        help="Robot port number")

    args = parser.parse_args()
    main(args.ip, args.port)
