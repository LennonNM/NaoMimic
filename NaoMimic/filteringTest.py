# import
from scipy import signal
import matplotlib.pyplot as plt
from os.path import dirname, abspath
import os
import numpy as np

# import sys
from Libraries import Calibration_Utils as calibration
from Libraries import  CSV_Utils as csvUtils
from Libraries import Graph_Utils as graph
from Libraries import Mimic_Utils as mimic

# ----------------------------------------------------------------------------------------------------------------------


def main(pathMocap, pathReferences, calProfileDir):
    # Get reference data
    # HeadNao = calibration.extractAxes(csvUtils.readCSVNao(pathReferences[0], "HEAD"))
    # TorsoNao = calibration.extractAxes(csvUtils.readCSVNao(pathReferences[1], "TORSO"))
    # ArmsNao = csvUtils.readCSVNao(pathReferences[2], "ARMS")
    # RArmNao = calibration.extractAxes(ArmsNao[0])
    # LArmNao = calibration.extractAxes(ArmsNao[1])
    #
    HeadNao1 = calibration.extractAxes(csvUtils.readCSVNao("Default/HEAD", "HEAD"))
    TorsoNao1 = calibration.extractAxes(csvUtils.readCSVNao("Default/TORSO", "TORSO"))
    ArmsNao1 = csvUtils.readCSVNao("Default/ARMS", "ARMS")
    RArmNao1 = calibration.extractAxes(ArmsNao1[0])
    LArmNao1 = calibration.extractAxes(ArmsNao1[1])
    #
    # HeadNao2 = calibration.extractAxes(csvUtils.readCSVNao("Default/HEAD2", "HEAD"))
    # TorsoNao2 = calibration.extractAxes(csvUtils.readCSVNao("Default/TORSO2", "TORSO"))
    # ArmsNao2 = csvUtils.readCSVNao("Default/ARMS2", "ARMS")
    # RArmNao2 = calibration.extractAxes(ArmsNao2[0])
    # LArmNao2 = calibration.extractAxes(ArmsNao2[1])

    # Read data from each single CSV from calibration routines
    HeadP = calibration.extractAxes(csvUtils.readCSVMocap(pathMocap + "Head", "HEAD"))
    TorsoP = calibration.extractAxes(csvUtils.readCSVMocap(pathMocap + "Torso", "TORSO"))
    ArmsP = csvUtils.readCSVMocap(pathMocap + "Arms", "ARMS")
    RArmP = calibration.extractAxes(ArmsP[0])
    LArmP = calibration.extractAxes(ArmsP[1])

    # for axis in range(6):
    #     graph.plotCompareSameAxis(HeadNao1[axis], HeadNao2[axis], "1", "2")
    t = range(len(LArmP[0]))
    labels = ["X", "Y", "Z", "WX", "WY", "WZ"]
    rootDir = dirname(dirname(abspath(__file__)))
    fileDir = os.path.join(rootDir, "NaoMimic/Comparisons/Validation/Javier_10_Filter/")

    HeadPFilter = calibration.filterAxesLowpassButterworth(TorsoP)
    graph.plotCompareSameAxis(TorsoP[5], HeadPFilter[5])





# ----------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    pathRefNao = ["Validation/ref_HEAD",
                  "Validation/ref_TORSO",
                  "Validation/ref_ARMS"]

    main("Validation/Naty/Take1/Naty", pathRefNao, "Validation/Javier_10_Filter/Take1/Javier")