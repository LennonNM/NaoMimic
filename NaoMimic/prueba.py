
# import sys
from Libraries import CSV_Utils as csvUtils
from Libraries import Calibration_Utils as calibration
from Libraries import Graph_Utils as graph

def  main(humanDir, refDir, calProfileDir):

    calibration.performFullCalibration(humanDir, refDir, calProfileDir)

if __name__ == "__main__":
    # main(sys.argv[1], sys.argv[2], sys.argv[3])
    main("Javier2/Javier", ["ref_HEAD", "ref_TORSO", "ref_ARMS"], "Javier2")
