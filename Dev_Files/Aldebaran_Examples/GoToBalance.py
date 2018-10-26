import sys
from naoqi import ALProxy


def main(robotIP):
    PORT = 9559

    try:
        motionProxy = ALProxy("ALMotion", robotIP, PORT)
    except Exception,e:
        print "Could not create proxy to ALMotion"
        print "Error was: ",e
        sys.exit(1)

    try:
        postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
    except Exception, e:
        print "Could not create proxy to ALRobotPosture"
        print "Error was: ", e

    # Send NAO to Pose Init
    postureProxy.goToPosture("StandInit", 0.5)

    motionProxy.setStiffnesses("Body", 1.0)
    motionProxy.moveInit()
    motionProxy.wbEnable(True)

    # Example showing how to com go to LLeg.
    supportLeg = "LLeg"
    duration   = 2.0
    motionProxy.wbGoToBalance(supportLeg, duration)

    motionProxy.wbEnable(False)


if __name__ == "__main__":
    robotIp = "10.0.1.128"

    if len(sys.argv) <= 1:
        print "Usage python almotion_wbgotobalance.py robotIP (optional default: 127.0.0.1)"
    else:
        robotIp = sys.argv[1]

    main(robotIp)
