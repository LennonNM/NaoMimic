"""
Supports the calibration process.
"""

# Imports
import time
import numpy as np
from collections import Counter

# Project libraries
from Libraries import Error_Utils as error
from Libraries import CSV_Utils as csvUtils

# ----------------------------------------------------------------------------------------------------------------------

def syncData(mocapData, referenceData):
    """
    This function is used to time couple 2 different sets of data. It shifts the mocapData to match the
    referenceData general shape by comparing the position in the timeline of the maximum peak.
    Each set corresponds to a single effector and includes the axes, in the corresponding order, X, Y, Z, WX, WY, WZ.

    :param mocapData: Data to adjust. Obtained from Motive export.
    :param referenceData: Set of data to be used as reference. Obtained from the Nao's sensors using GetPositions.py.
    :return finalDataSet: Complete data set time coupled with the reference data.
    """

    # Separate axes of the data sets
    mocapAxes = extractAxes(mocapData)
    referenceAxes = extractAxes(referenceData)

    # Shift data set according to reference data set
    shiftedAxes = [[] for k in range(6)]
    for axis in range(6):
        shiftedAxes[axis] = shiftDataSet(mocapAxes[axis], referenceAxes[axis])

    # Adjust data sets lengths
    finalDataSet = [[] for k in range(6)]
    for axis in range(6):
        finalDataSet[axis] = makeListSameLength(shiftedAxes[axis], referenceAxes[axis])

    return finalDataSet

# ----------------------------------------------------------------------------------------------------------------------

def getCalibrationTerms(listPerson, listReference, degree = 1):
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
        refX.append(float(listReference[i][0]))
        refY.append(float(listReference[i][1]))
        refZ.append(float(listReference[i][2]))
        refWX.append(float(listReference[i][3]))
        refWY.append(float(listReference[i][4]))
        refWZ.append(float(listReference[i][5]))
    # Data to adjust
    for i in range(len(listPerson)):
            personX.append(float(listPerson[i][0]))
            personY.append(float(listPerson[i][1]))
            personZ.append(float(listPerson[i][2]))
            personWX.append(float(listPerson[i][3]))
            personWY.append(float(listPerson[i][4]))
            personWZ.append(float(listPerson[i][5]))

    # Uses polyfit to perform pylinomial linear regression
    coefficients[0] = list(np.polyfit(personX, refX, degree))
    coefficients[1] = list(np.polyfit(personY, refY, degree))
    coefficients[2] = list(np.polyfit(personZ, refZ, degree))
    coefficients[3] = list(np.polyfit(personWX, refWX, degree))
    coefficients[4] = list(np.polyfit(personWY, refWY, degree))
    coefficients[5] = list(np.polyfit(personWZ, refWZ, degree))

    return coefficients

# ----------------------------------------------------------------------------------------------------------------------

def extractAxes(axisDataSet):
    """
    This function is used to separate a list with data sets with all axes per row, of the form [[X,Y,Z,WX,WY,WZ]], to a
    list with data sets for each axis, with the form [[X], [Y], [Z], [WX], [WY], [WZ]].

    :param axisDataSet: Set with the data to separate into axes. Each element (row) is a set of (X,Y,Z,WX,WY,WZ).
    :return axesList: List which each element is a set of the separated axes.
    """

    # Define list to store separated axes (X, Y, X, WX, WY, WZ)
    axesList = [[] for k in range(6)]

    for row in axisDataSet:
        axesList[0].append(row[0])
        axesList[1].append(row[1])
        axesList[2].append(row[2])
        axesList[3].append(row[3])
        axesList[4].append(row[4])
        axesList[5].append(row[5])

    return axesList

# ----------------------------------------------------------------------------------------------------------------------

def getBaseValueOfSet(axisDataSet):
    """
    This function is used to get the most frequent value from an axis data set.

    :param axisDataSet: Data set to find value for a single axis.
    :return: Returns the value of the most frequent item and its frequency.
    """

    mostCommonValue, frequencyOfAppereance = Counter(axisDataSet).most_common(1)[0]

    return [mostCommonValue, frequencyOfAppereance]

# ----------------------------------------------------------------------------------------------------------------------

def findMaxValue(axisDataSet):
    """
    This function is used to find the item with the maximum value of a data set.

    :param axisDataSet: Data set for a single axis.
    :return: The Index of the element with the maximum value form the data set and its Value.
    """

    maxValue = max(axisDataSet)
    index = axisDataSet.index(maxValue)

    return [maxValue, index]

# ----------------------------------------------------------------------------------------------------------------------

def rotateAxis(axisDataSet):
    """
    This function is used to rotate a data set around its base value (most common value of the set).

    :param axisDataSet: The data set to rotate. Comes from a single axis.
    :return rotatedDataSet: The rotated data set.
    """

    rotatedDataSet = list()
    [baseValue, frequencyValue] = getBaseValueOfSet(axisDataSet)

    # Define limits for rotation with a 10% tolerance margin
    if baseValue < 0:
        lowTolerance = baseValue + baseValue * 0.1
    else:
        lowTolerance = baseValue - baseValue * 0.1

    # Rotate data set around baseValue
    for value in axisDataSet:
        if value < lowTolerance:
            rotatedDataSet.append(baseValue + abs(baseValue - value))
        else:
            rotatedDataSet.append(value)

    return rotatedDataSet

# ----------------------------------------------------------------------------------------------------------------------

def shiftDataSet(axisDataSet, referenceDataSet):
    """
    This function is used to shift the data set from a single axis so that the place of its maximum value matches the
    placement of the maximum value of the reference data set. To make sure it finds a maximum value (the value can be a
    minimum due to orientation of the object) it rotates both data sets.

    :param axisDataSet: Data set to shift from a single axis.
    :param referenceDataSet: Reference data set from a single axis.
    :return axisDataSet: The shifted data set
    """

    # Make sure all curves have maximums by rotating the data sets
    rotAxes = rotateAxis(axisDataSet)
    rotRef = rotateAxis(referenceDataSet)

    # Find maximums of each data set
    [maxValueAxis, indexValueAxis] = findMaxValue(rotAxes)
    [maxValueRef, indexValueRef] = findMaxValue(rotRef)

    # Get the distance between maximums
    maxDistance = indexValueRef - indexValueAxis

    # Shift the data set
    # # Shift to the right
    if maxDistance > 0:
        for space in range(maxDistance):
            axisDataSet.insert(0, axisDataSet[0])
    # # Shift to the left
    elif maxDistance < 0:
        for space in range(abs(maxDistance)):
            del axisDataSet[0]

    return axisDataSet

# ----------------------------------------------------------------------------------------------------------------------

def makeListSameLength(axisDataSet, referenceDataSet):
    """
    This function is used to adjust a data set length to match a reference data set length. The reference data set
    is not altered.

    :param axisDataSet: The data set to adjust its length.
    :param referenceDataSet: The reference data fo compare the desired length.
    :return axisDataSet: The data set with its length adjusted to match the referenceDataSet length.
    """

    # Get lengths of each data set
    lenAxis = len(axisDataSet)
    lenRef = len(referenceDataSet)

    # Get the difference between lengths
    lenDiff = lenRef - lenAxis

    # Adjust length of axisDataSet to match the reference length
    if lenDiff > 0:
        for space in range(lenDiff):
            axisDataSet.insert(-1, axisDataSet[-1])
    elif lenDiff < 0:
        for space in range(abs(lenDiff)):
            del axisDataSet[-1]

    # Check that the lengths do match
    finalLenAxis = len(axisDataSet)
    if finalLenAxis != lenRef:
        error.abort("Failed to adjust data sets lengths", "Make List Same Length")

    return axisDataSet

# ----------------------------------------------------------------------------------------------------------------------

def joinAxesInRow(axesDataSets):
    """
    This function is used to join into "rows" the data from a list with separated axes.
    From a list of the form [[X], [Y], [Z], [WX], [WY], [WZ]] to [[X, Y, Z, WX, WY, WZ]].

    :param axesDataSets: List with the data set for each individual axis.
    :return dataSetsInRow: List with data by sets of all axes per row.
    """

    rowAxes = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    rowsLength = len(axesDataSets[0])  # All axes should be the same length
    dataSetsInRow = list()

    for row in range(rowsLength):
        for axisNo, axisValue in enumerate(axesDataSets):
            rowAxes[axisNo] = axisValue[row]
        dataSetsInRow.append(rowAxes[:])

    return dataSetsInRow

# ----------------------------------------------------------------------------------------------------------------------

def extractEffectors(mixedEffectorsSet, effectorsNumber = 4):
    """
    This function is used to extract the effectors data from a data set of the form [[X, Y, Z, WX, WY, WZ, X, Y, Z,...]]
    to the form [[X, Y, Z, WX, WY, WZ],[X, Y, Z, WX, WY, WZ]...]. Each row of the effector will contain all the axes.

    :param mixedEffectorsSet: Data set to extract effector's data
    :param effectorsNumber: Number of effectors to separate the data into.
    :return dataEffectors: Data set organized per effector.
    """

    dataEffectors = [[] for k in range(effectorsNumber)]
    for row in mixedEffectorsSet:
        for effector in range(effectorsNumber):
            dataEffectors[effector].append(row[6*effector:6+6*effector])

    return dataEffectors

# ----------------------------------------------------------------------------------------------------------------------

def cleanseDataSet(dataSetToClean):
    """
    This function is used to delete the remaining blank rows generated by the calibration process (adjust data set
    length to match reference, write single CSV with all adjusted data, extract data...). Receives a data set of a
    single effector with all axes.

    :param dataSetToClean: Data set to delete extra blank rows.
    :return: Data set cleaned.
    """

    for rowNo in range(len(dataSetToClean)):
        isRowBlank = True
        for axis in range(6):
            if dataSetToClean[rowNo][axis] != "":
                isRowBlank = False
        if isRowBlank:
            del dataSetToClean[rowNo::]
            break

    return dataSetToClean

# ----------------------------------------------------------------------------------------------------------------------

def performFullCalibration(pathMoCap, pathReferences, pathCalProfile):
    """
    This function is used to run the whole calibration process. It requires the existance of the calibration CSV files,
    the MoCap calibration data and the Nao reference data. The calibration is performed for all available effectors to
    use by default (Head, Torso, RArm, LArm). It uses the default directories to store/read each involved file.

    :param pathMoCap: Path inside Calibration/Human/MoCap_Export to read the MoCap export file.
    :param pathReferences: Path inside Calibration/NAO/ReferenceData(/Default)
    :param pathCalProfile: Path inside Calibration/Human/CalibrationProfiles to store the Calibration Profile files.
    :return: void
    """


    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
          + "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
          + "                   Starting Calibration Process                   ")
    time.sleep(3)

    print("\n------------------------------------------------------------------\n"
          + "Retrieving data from CSV files"
          + "\n------------------------------------------------------------------\n")
    time.sleep(2)
    # Get reference data
    HeadNao = csvUtils.readCSVNao(pathReferences[0], "HEAD")
    TorsoNao = csvUtils.readCSVNao(pathReferences[1], "TORSO")
    ARmsNao = csvUtils.readCSVNao(pathReferences[2], "ARMS")

    # Read data from each single CSV from calibration routines
    HeadP = csvUtils.readCSVMocap(pathMoCap + "Head", "HEAD")
    TorsoP = csvUtils.readCSVMocap(pathMoCap + "Torso", "TORSO")
    ARmsP = csvUtils.readCSVMocap(pathMoCap + "Arms", "ARMS")

    # Sync data (now data sets are gruped by axes instead of frame)
    print("\n------------------------------------------------------------------\n"
          + "Syncing MoCap data to match time placement and data set size"
          + "\n------------------------------------------------------------------\n")
    time.sleep(2)
    HeadSync = syncData(HeadP, HeadNao)
    TorsoSync = syncData(TorsoP, TorsoNao)
    RArmSync = syncData(ARmsP[0], ARmsNao[0])
    LArmSync = syncData(ARmsP[1], ARmsNao[1])
    dataEffectors = [HeadSync, TorsoSync, RArmSync, LArmSync]

    # Write single CSV with adjusted data
    print("\n------------------------------------------------------------------\n"
          + "Write single CSV with synced MoCap data"
          + "\n------------------------------------------------------------------\n")
    time.sleep(2)
    singleCSVPath = pathCalProfile + "/AdjustedDataSet"
    csvUtils.writeCSVMocapSingleAdjusted(dataEffectors, singleCSVPath)

    # Create Calibration Profile from adjusted data CSV
    print("\n------------------------------------------------------------------\n"
          + "Creating Calibration Profile file"
          + "\n------------------------------------------------------------------\n")
    time.sleep(2)
    # # Read adjusted data
    dataAdjusted = csvUtils.readCalibrationFile(singleCSVPath)[1:]
    adjustedEffectors = extractEffectors(dataAdjusted)
    adjustedEffectorsFinal = [cleanseDataSet(adjustedEffectors[0]),
                              cleanseDataSet(adjustedEffectors[1]),
                              cleanseDataSet(adjustedEffectors[2]),
                              cleanseDataSet(adjustedEffectors[3])]
    # # Get calibration terms
    HeadCoeff = getCalibrationTerms(adjustedEffectorsFinal[0], HeadNao)
    TorsoCoeff = getCalibrationTerms(adjustedEffectorsFinal[1], TorsoNao)
    RArmCoeff = getCalibrationTerms(adjustedEffectorsFinal[2], ARmsNao[0])
    LArmCoeff = getCalibrationTerms(adjustedEffectorsFinal[3], ARmsNao[1])
    coefficientsList = [HeadCoeff, TorsoCoeff, RArmCoeff, LArmCoeff]
    # # Write Calibration Profile with terms
    csvUtils.writeCalibrationProfile(coefficientsList, pathCalProfile + "/" + pathCalProfile)

    print("\n\n             Calibration Process Finished Succesfully             \n"
          + "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
          + "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")