"""
Supports the calibration process.
"""

# Imports
import numpy as np

# Project libraries
import Error_Utils as error

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
    DoF = 6

    # Make all data positive and separate it into lists
    # Reference data
    for i in range(len(referenceData)):
        referenceX.append(abs(referenceData[i][0]))
        referenceY.append(abs(referenceData[i][1]))
        referenceZ.append(abs(referenceData[i][2]))
        referenceWX.append(abs(referenceData[i][3]))
        referenceWY.append(abs(referenceData[i][4]))
        referenceWZ.append(abs(referenceData[i][5]))

    # Data to adjust
    for i in range(len(mocapData)):
        print(i)
        print(mocapData[i][0])
        mocapDataX.append(abs(mocapData[i][0]))
        mocapDataY.append(abs(mocapData[i][1]))
        mocapDataZ.append(abs(mocapData[i][2]))
        mocapDataWX.append(abs(mocapData[i][3]))
        mocapDataWY.append(abs(mocapData[i][4]))
        mocapDataWZ.append(abs(mocapData[i][5]))

    # Find maximum on each set
    maxRef = [max(referenceX), max(referenceY), max(referenceY), max(referenceWX), max(referenceWY), max(referenceWZ)]
    maxMocap = [max(mocapDataX), max(mocapDataY), max(mocapDataZ), max(mocapDataWX), max(mocapDataWY), max(mocapDataWZ)]
    # Make sure there is only one maximum per axis
    for i in maxRef:
        if len(i) > 1:
            error.abort("Data ste has more than one maximum")
    for i in maxMocap:
        if len(i) > 1:
            error.abort("Data ste has more than one maximum")

    # Find indexes of maximums
    indxRef = [[] for k in range(DoF)]
    indxMocap = [[] for k in range(DoF)]
    # Reference data
    indxRef[0] = [index for index, item in enumerate(referenceX) if item == maxRef[0]]
    indxRef[1] = [index for index, item in enumerate(referenceY) if item == maxRef[1]]
    indxRef[2] = [index for index, item in enumerate(referenceX) if item == maxRef[2]]
    indxRef[3] = [index for index, item in enumerate(referenceWX) if item == maxRef[3]]
    indxRef[4] = [index for index, item in enumerate(referenceWY) if item == maxRef[4]]
    indxRef[5] = [index for index, item in enumerate(referenceWZ) if item == maxRef[5]]
    # MoCap data
    indxMocap[0] = [index for index, item in enumerate(mocapDataX) if item == maxMocap[0]]
    indxMocap[1] = [index for index, item in enumerate(mocapDataY) if item == maxMocap[1]]
    indxMocap[2] = [index for index, item in enumerate(mocapDataZ) if item == maxMocap[2]]
    indxMocap[3] = [index for index, item in enumerate(mocapDataWX) if item == maxMocap[3]]
    indxMocap[4] = [index for index, item in enumerate(mocapDataWY) if item == maxMocap[4]]
    indxMocap[5] = [index for index, item in enumerate(mocapDataWZ) if item == maxMocap[5]]

    # Get distance to shift MoCap Data
    shiftLen = [[] for k in range(DoF)]
    for i in range(len(shiftLen)):
        shiftLen[i] = indxRef[i] - indxMocap[i]

    # Crop MoCap sets to match maximums
    # X
    if shiftLen[0] < 0:
        # Crops from the begining to shift to the left
        del mocapDataX[0:abs(shiftLen[0])]
    else:
        # Adds elements at the begining to shift to the right
        mocapDataX.insert(0, mocapDataX[0])
    # Y
    if shiftLen[1] < 0:
        del mocapDataX[0:abs(shiftLen[1])]
    else:
        mocapDataX.insert(0, mocapDataX[1])
    # Z
    if shiftLen[2] < 0:
        del mocapDataX[0:abs(shiftLen[2])]
    else:
        mocapDataX.insert(0, mocapDataX[2])
    # WX
    if shiftLen[3] < 0:
        del mocapDataX[0:abs(shiftLen[3])]
    else:
        mocapDataX.insert(0, mocapDataX[3])
    # WY
    if shiftLen[4] < 0:
        del mocapDataX[0:abs(shiftLen[4])]
    else:
        mocapDataX.insert(0, mocapDataX[4])
    # WZ
    if shiftLen[5] < 0:
        del mocapDataX[0:abs(shiftLen[5])]
    else:
        mocapDataX.insert(0, mocapDataX[5])

    # Final crop to make reference set and MoCap set of the same length
    lenDiff = [[] for i in range(DoF)]
    lenDiff[0] = len(referenceX) - len(mocapDataX)
    lenDiff[1] = len(referenceY) - len(mocapDataY)
    lenDiff[2] = len(referenceZ) - len(mocapDataZ)
    lenDiff[3] = len(referenceWX) - len(mocapDataWX)
    lenDiff[4] = len(referenceWY) - len(mocapDataWY)
    lenDiff[5] = len(referenceWZ) - len(mocapDataWZ)
    # X
    if lenDiff[0] > 0:
        del mocapDataX[len(mocapDataX) - 1 + lenDiff[0]:len(mocapDataX) - 1]
    else:
        mocapDataX.insert(len(mocapDataX) - 1, mocapDataX[len(mocapDataX) - 1])
    # Y
    if lenDiff[1] > 0:
        del mocapDataY[len(mocapDataY) - 1 + lenDiff[1]:len(mocapDataY) - 1]
    else:
        mocapDataY.insert(len(mocapDataY) - 1, mocapDataY[len(mocapDataY) - 1])
    # Z
    if lenDiff[2] > 0:
        del mocapDataZ[len(mocapDataZ) - 1 + lenDiff[2]:len(mocapDataZ) - 1]
    else:
        mocapDataZ.insert(len(mocapDataZ) - 1, mocapDataZ[len(mocapDataZ) - 1])
    # WX
    if lenDiff[3] > 0:
        del mocapDataWX[len(mocapDataWX) - 1 + lenDiff[3]:len(mocapDataWX) - 1]
    else:
        mocapDataWX.insert(len(mocapDataWX) - 1, mocapDataWX[len(mocapDataWX) - 1])
    # WY
    if lenDiff[4] > 0:
        del mocapDataWY[len(mocapDataWY) - 1 + lenDiff[4]:len(mocapDataWY) - 1]
    else:
        mocapDataWY.insert(len(mocapDataWY) - 1, mocapDataWY[len(mocapDataWY) - 1])
    # WZ
    if lenDiff[5] > 0:
        del mocapDataWZ[len(mocapDataWZ) - 1 + lenDiff[5]:len(mocapDataWZ) - 1]
    else:
        mocapDataWZ.insert(len(mocapDataWZ) - 1, mocapDataWZ[len(mocapDataWZ) - 1])

    # Return adjusted data set
    adjustedSet = [mocapDataWX, mocapDataWY, mocapDataWZ, mocapDataX, mocapDataY, mocapDataZ]
    return adjustedSet

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
                    "\nPerson data set size: " + listPerson)

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

