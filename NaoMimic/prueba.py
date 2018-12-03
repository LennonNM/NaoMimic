
# import sys
from Libraries import Calibration_Utils as calibration
from Libraries import CSV_Utils as csvUtils
from Libraries import Graph_Utils as graph
from Libraries import Mimic_Utils as mimic

def  main(pathMocap, pathReferences, calProfileDir):

    # calibration.performFullCalibration(pathMocap, pathReferences, calProfileDir, False)

    # Get reference data
    HeadNao = calibration.extractAxes(csvUtils.readCSVNao(pathReferences[0], "HEAD"))
    TorsoNao = calibration.extractAxes(csvUtils.readCSVNao(pathReferences[1], "TORSO"))
    ArmsNao = csvUtils.readCSVNao(pathReferences[2], "ARMS")
    RArmNao = calibration.extractAxes(ArmsNao[0])
    LArmNao = calibration.extractAxes(ArmsNao[1])

    # # Read data from each single CSV from calibration routines
    # HeadP = calibration.extractAxes(csvUtils.readCSVMocap(pathMocap + "Head", "HEAD"))
    # TorsoP = calibration.extractAxes(csvUtils.readCSVMocap(pathMocap + "Torso", "TORSO"))
    # ArmsP = csvUtils.readCSVMocap(pathMocap + "Arms", "ARMS")
    # RArmP = calibration.extractAxes(ArmsP[0])
    # LArmP = calibration.extractAxes(ArmsP[1])
    #
    # coefficients = csvUtils.readCalibrationFile(calProfileDir + "/Javier2_CP")
    mimic.adjustChoreography("CoreografiaPrueba", calProfileDir + "/Javier2_CP")
    
    adjustedHead = [[] for k in range(6)]
    adjustedTorso = [[] for k in range(6)]
    adjustedRArm = [[] for k in range(6)]
    adjustedLArm = [[] for k in range(6)]

    for axisNo, axis in enumerate(HeadP):
        for row, data in enumerate(axis):
            adjustedHead[axisNo].append(data*float(coefficients[axisNo][0]) + float(coefficients[axisNo][1]))
    for axisNo, axis in enumerate(TorsoP):
        for row, data in enumerate(axis):
            adjustedTorso[axisNo].append(data * float(coefficients[axisNo+6][0]) + float(coefficients[axisNo+6][1]))
    for axisNo, axis in enumerate(RArmP):
        for row, data in enumerate(axis):
            adjustedRArm[axisNo].append(data * float(coefficients[axisNo+6*2][0]) + float(coefficients[axisNo+6*2][1]))
    for axisNo, axis in enumerate(LArmP):
        for row, data in enumerate(axis):
            adjustedLArm[axisNo].append(data * float(coefficients[axisNo+6*3][0]) + float(coefficients[axisNo+6*3][1]))

    finalHead = [[] for k in range(6)]
    for axis in range(6):
        finalHead[axis] = calibration.shiftDataSet(adjustedHead[axis], HeadNao[axis])
    finalTorso = [[] for k in range(6)]
    for axis in range(6):
        finalTorso[axis] = calibration.shiftDataSet(adjustedTorso[axis], TorsoNao[axis])
    finalRArm = [[] for k in range(6)]
    for axis in range(6):
        finalRArm[axis] = calibration.shiftDataSet(adjustedRArm[axis], RArmNao[axis])
    finalLArm = [[] for k in range(6)]
    for axis in range(6):
        finalLArm[axis] = calibration.shiftDataSet(adjustedLArm[axis], LArmNao[axis])

    axesLabels = ["X", "Y", "Z", "WX", "WY", "WZ"]
    for axis in range(6):
        graph.plotCompareSameAxis(HeadP[axis], finalHead[axis], "MoCap Orig " + axesLabels[axis],
                                  "MoCap Adjusted " + axesLabels[axis],
                                  HeadNao[axis], "Nao " + axesLabels[axis], True,
                                  "Default/JavierAdjusted_Head_" + axesLabels[axis], True)
    for axis in range(6):
        graph.plotCompareSameAxis(TorsoP[axis], finalTorso[axis], "MoCap Orig " + axesLabels[axis],
                                  "MoCap Adjusted " + axesLabels[axis],
                                  TorsoNao[axis], "Nao " + axesLabels[axis], True,
                                  "Default/JavierAdjusted_Torso_" + axesLabels[axis], True)
    for axis in range(6):
        graph.plotCompareSameAxis(RArmP[axis], finalRArm[axis], "MoCap Orig " + axesLabels[axis],
                                  "MoCap Adjusted " + axesLabels[axis],
                                  RArmNao[axis], "Nao " + axesLabels[axis], True,
                                  "Default/JavierAdjusted_RArm_" + axesLabels[axis], True)
    for axis in range(6):
        graph.plotCompareSameAxis(LArmP[axis], finalLArm[axis], "MoCap Orig " + axesLabels[axis],
                                  "MoCap Adjusted " + axesLabels[axis],
                                  LArmNao[axis], "Nao " + axesLabels[axis], True,
                                  "Default/JavierAdjusted_LArm_" + axesLabels[axis], True)

if __name__ == "__main__":
    # main(sys.argv[1], sys.argv[2], sys.argv[3])
    main("Javier2/Javier", ["ref_HEAD", "ref_TORSO", "ref_ARMS"], "Javier2")
