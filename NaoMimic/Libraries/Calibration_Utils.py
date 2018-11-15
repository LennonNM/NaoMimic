"""
Supports the calibration process.
"""

# Imports
import numpy as np

# Project libraries
from Libraries import Error_Utils as error

# ----------------------------------------------------------------------------------------------------------------------

def syncData(referenceData, mocapData):
    """
    This function is used to time couple 2 different sets of data. It shifts the mocapData to match the
    referenceData general shape by comparing the position in the timeline of the maximum peak.
    Each set corresponds to a single effector and includes the axes, in the corresponding order, X, Y, Z, WX, WY, WZ.

    :param referenceData: Set of data to be used as reference. Obtained from the Nao's sensors using GetPositions.py.
    :param mocapData: Data to adjust. Obtained from Motive export.
    :return adjustedSet: Complete data set time coupled with the reference data. Set for a single effector.
    """
    referenceX = list()
    referenceY = list()
    referenceZ = list()
    referenceWX = list()
    referenceWY = list()
    referenceWZ = list()
    mocapDataX = list()
    mocapDataY = list()
    mocapDataZ = list()
    mocapDataWX = list()
    mocapDataWY = list()
    mocapDataWZ = list()
    mocapDataAbsX = list()
    mocapDataAbsY = list()
    mocapDataAbsZ = list()
    mocapDataAbsWX = list()
    mocapDataAbsWY = list()
    mocapDataAbsWZ = list()
    DoF = 6

    # Make all data positive and separate it into lists
    # Reference data
    for axesRefSet in referenceData:
        referenceX.append(abs(axesRefSet[0]))
        referenceY.append(abs(axesRefSet[1]))
        referenceZ.append(abs(axesRefSet[2]))
        referenceWX.append(abs(axesRefSet[3]))
        referenceWY.append(abs(axesRefSet[4]))
        referenceWZ.append(abs(axesRefSet[5]))

    # Data to adjust
    for axesModSet in mocapData:
        # Data all positive
        mocapDataAbsX.append(abs(axesModSet[0]))
        mocapDataAbsY.append(abs(axesModSet[1]))
        mocapDataAbsZ.append(abs(axesModSet[2]))
        mocapDataAbsWX.append(abs(axesModSet[3]))
        mocapDataAbsWY.append(abs(axesModSet[4]))
        mocapDataAbsWZ.append(abs(axesModSet[5]))
        # Data separated by axis
        mocapDataX.append(abs(axesModSet[0]))
        mocapDataY.append(abs(axesModSet[1]))
        mocapDataZ.append(abs(axesModSet[2]))
        mocapDataWX.append(abs(axesModSet[3]))
        mocapDataWY.append(abs(axesModSet[4]))
        mocapDataWZ.append(abs(axesModSet[5]))

    # Find maximum on each set
    maxRef = [max(referenceX), max(referenceY), max(referenceZ), max(referenceWX), max(referenceWY), max(referenceWZ)]
    maxMocap = [max(mocapDataAbsX), max(mocapDataAbsY), max(mocapDataAbsZ), max(mocapDataAbsWX), max(mocapDataAbsWY), max(mocapDataAbsWZ)]

    # Find indexes of maximums
    indxRef = [[] for k in range(DoF)]
    indxMocap = [[] for k in range(DoF)]
    # # Reference data
    indxRef[0] = referenceX.index(maxRef[0])
    indxRef[1] = referenceY.index(maxRef[1])
    indxRef[2] = referenceZ.index(maxRef[2])
    indxRef[3] = referenceWX.index(maxRef[3])
    indxRef[4] = referenceWY.index(maxRef[4])
    indxRef[5] = referenceWZ.index(maxRef[5])
    # # MoCap data
    indxMocap[0] = mocapDataX.index(maxMocap[0])
    indxMocap[1] = mocapDataY.index(maxMocap[1])
    indxMocap[2] = mocapDataZ.index(maxMocap[2])
    indxMocap[3] = mocapDataWX.index(maxMocap[3])
    indxMocap[4] = mocapDataWY.index(maxMocap[4])
    indxMocap[5] = mocapDataWZ.index(maxMocap[5])

    # Get distance to shift MoCap Data
    shiftLen = [[] for k in range(DoF)]
    for i in range(len(shiftLen)):
        shiftLen[i] = indxRef[i] - indxMocap[i]

    # Crop MoCap sets to match maximums
    # X
    if shiftLen[0] < 0:
        # Crops from the begining to shift to the left
        del mocapDataX[0:abs(shiftLen[0])]
    elif shiftLen[0] > 0:
        # Adds elements at the begining to shift to the right
        for spaces in range(abs(shiftLen[0])):
            mocapDataX.insert(0, mocapDataX[0])
    # Y
    if shiftLen[1] < 0:
        del mocapDataY[0:abs(shiftLen[1])]
    elif shiftLen[1] > 0:
        for spaces in range(abs(shiftLen[1])):
            mocapDataY.insert(0, mocapDataY[0])
    # Z
    if shiftLen[2] < 0:
        del mocapDataZ[0:abs(shiftLen[2])]
    elif shiftLen[2] > 0:
        for spaces in range(abs(shiftLen[2])):
            mocapDataZ.insert(0, mocapDataZ[0])
    # WX
    if shiftLen[3] < 0:
        del mocapDataWX[0:abs(shiftLen[3])]
    elif shiftLen[3] > 0:
        for spaces in range(abs(shiftLen[3])):
            mocapDataWX.insert(0, mocapDataWX[0])
    # WY
    if shiftLen[4] < 0:
        del mocapDataWY[0:abs(shiftLen[4])]
    elif shiftLen[4] > 0:
        for spaces in range(abs(shiftLen[4])):
            mocapDataWY.insert(0, mocapDataWY[0])
    # WZ
    if shiftLen[5] < 0:
        del mocapDataZ[0:abs(shiftLen[5])]
    elif shiftLen[5] > 0:
        for spaces in range(abs(shiftLen[5])):
            mocapDataWZ.insert(0, mocapDataWZ[0])

    # Final crop to make reference set and MoCap set of the same length
    lenDiff = [[] for i in range(DoF)]
    lenDiff[0] = len(referenceX) - len(mocapDataX)
    lenDiff[1] = len(referenceY) - len(mocapDataY)
    lenDiff[2] = len(referenceZ) - len(mocapDataZ)
    lenDiff[3] = len(referenceWX) - len(mocapDataWX)
    lenDiff[4] = len(referenceWY) - len(mocapDataWY)
    lenDiff[5] = len(referenceWZ) - len(mocapDataWZ)

    # X
    if lenDiff[0] < 0:
        for i in range(abs(lenDiff[0])):
            del mocapDataX[- 1]
    elif lenDiff[0] > 0:
        for i in range(lenDiff[0]):
            mocapDataX.insert(- 1, mocapDataX[- 1])
    # Y
    if lenDiff[1] < 0:
        for i in range(abs(lenDiff[1])):
            del mocapDataY[- 1]
    elif lenDiff[1] > 0:
        for i in range(lenDiff[1]):
            mocapDataY.insert(- 1, mocapDataY[- 1])
    # Z
    if lenDiff[2] < 0:
        for i in range(abs(lenDiff[2])):
            del mocapDataZ[- 1]
    elif lenDiff[2] > 0:
        for i in range(lenDiff[2]):
            mocapDataZ.insert(- 1,mocapDataZ[- 1])
    # WX
    if lenDiff[3] < 0:
        for i in range(abs(lenDiff[3])):
            del mocapDataWX[- 1]
    elif lenDiff[3] > 0:
        for i in range(lenDiff[3]):
            mocapDataWX.insert(- 1, mocapDataWX[- 1])
    # WY
    if lenDiff[4] < 0:
        for i in range(abs(lenDiff[4])):
            del mocapDataWY[- 1]
    elif lenDiff[4] > 0:
        for i in range(lenDiff[4]):
            mocapDataWY.insert(- 1, mocapDataWY[- 1])
    # WZ
    if lenDiff[5] < 0:
        for i in range(abs(lenDiff[5])):
            del mocapDataWZ[- 1]
    elif lenDiff[5] > 0:
        for i in range(lenDiff[5]):
            mocapDataWZ.insert(- 1, mocapDataWZ[- 1])

    # Return adjusted data set
    adjustedData = [mocapDataX, mocapDataY, mocapDataZ, mocapDataWX, mocapDataWY, mocapDataWZ]
    return adjustedData

# ----------------------------------------------------------------------------------------------------------------------

def getCalibrationTerms(listReference, listPerson, degree = 1):
    """
    This function performs the linear regression coupling between the 2 data sets received. The sets correspond to a
    single effector. The default polynomial degree for the regression is set to 1. This function uses polyfit from
    numpy to perform the linear regression. It supposes that both sets received are of the same size.
    
    :param listReference: Data set to be used as reference for the data coupling. Includes all the axes of the effector.
    :param listPerson: Data set to be adjusted.
    :param degree: Degree of the polynomial model to use for the linear regression.
    :return calibrationTerms: The coefficients of the polynomial fit between data sets, per axis of the effector.
    """

    # Makes sure data sets are same size
    if len(listReference) != len(listPerson):
        error.abort("Sizes of the data sets are not equal." +
                    "\nReference data set size: " + listReference +
                    "\nPerson data set size: " + listPerson, "Generation of calibration terms")

    # Create lists 
    refX = list()
    refY = list()
    refZ = list()
    refWX = list()
    refWY = list()
    refWZ = list()
    personX = list()
    personY = list()
    personZ = list()
    personWX = list()
    personWY = list()
    personWZ = list()
    coefficients = [[] for k in range(6)]  # Always does X, Y, Z, WX, WY, WZ

    # Separates each axis
    # Reference data
    for i in range(len(listReference)):
        refX.append(listReference[i][0])
        refY.append(listReference[i][1])
        refZ.append(listReference[i][2])
        refWX.append(listReference[i][3])
        refWY.append(listReference[i][4])
        refWZ.append(listReference[i][5])
    # Data to adjust
    for i in range(len(listPerson)):
            personX.append(listPerson[i][0])
            personY.append(listPerson[i][1])
            personZ.append(listPerson[i][2])
            personWX.append(listPerson[i][3])
            personWY.append(listPerson[i][4])
            personWZ.append(listPerson[i][5])

    # Uses polyfit to perform pylinomial linear regression
    coefficients[0] = list(np.polyfit(personX, refX, degree))
    coefficients[1] = list(np.polyfit(personY, refY, degree))
    coefficients[2] = list(np.polyfit(personZ, refZ, degree))
    coefficients[3] = list(np.polyfit(personWX, refWX, degree))
    coefficients[4] = list(np.polyfit(personWY, refWY, degree))
    coefficients[5] = list(np.polyfit(personWZ, refWZ, degree))

    return coefficients

