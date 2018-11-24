"""
Directly support the Mimic operation.
"""


# Project libraries
from Libraries import Miscellaneous_Utils as misc
from Libraries import Calibration_Utils as calibration

# ----------------------------------------------------------------------------------------------------------------------

def adjustChoreography(choreographyName, pathToCalibrationProfile):
    """
    This function is used to adjust a whole choreography CSV file using the specified Calibraiton Profile coefficients.

    :param choreographyName: Name of the choreography to adjust. The file must be located inside .../Choreography.
    :param pathToCalibrationProfile: Path to the Calibration Profile to use. Searches inside
                .../Calibration/Human/CalibrationProfiles
    :return adjustedDataSet: Data set for the adjusted choreography. Includes a set of [X, Y, Z, WX, WY, WZ] per row
                for each effector.
    """

    # Get calibration coefficients
    coefficients = csvUtils.readCalibrationFile(pathToCalibrationProfile)

    # Extract data from MoCap CSV export and place data per axis
    choreographyData = calibration.extractAxes(csvUtils.readCSVMocap(choreographyName, "ALL", True, True))

    # Adjust each axis per effector
    adjustedChoreography = [[] for k in range(choreographyData)]

    try:
        for effectorNo in range(len(choreographyData)):
            for axisNo, axis in enumerate(choreographyData[effectorNo]):
                for row, data in enumerate(axis):
                    adjustedChoreography[effectorNo][axisNo].append(data*float(coefficients[axisNo][0]) +
                                                                    float(coefficients[axisNo][1]))
    except Exception as e:
        misc.abort("Failed to adjust choreography file" + choreographyName,
                   "Adjust Choreography per Calibration Profile", e)

    # Regroup data as [X, Y, Z, WX, WY, WZ] per row]
    adjustedDataSet = [calibration.joinAxesInRow(adjustedChoreography[0]),
                       calibration.joinAxesInRow(adjustedChoreography[1]),
                       calibration.joinAxesInRow(adjustedChoreography[2]),
                       calibration.joinAxesInRow(adjustedChoreography[3])]
    return adjustedDataSet

# ----------------------------------------------------------------------------------------------------------------------

def getFixedTimeline(effectorData):
    """
    This function is used to generate a list with the time in seconds for each animation frame represented as a single
    row of axes. The base time between 2 consecutive animation frames should consider the following:
            - Kinematics resolver time to find a motion solution between frames: 20 ms
            - FPS of the MoCap recording exported data.

    :param effectorData: List with motion data from a single effector.
    :return:
    """

    timeBase = 0.05
    singleTimeline = [[0.00, 0.00, 0.00, 0.00, 0.00, 0.00]]
    for rowNo in range(len(effectorData)):
        singleTimeline.append([round(timeBase * (rowNo + 1), 2) for axis in range(6)])

    return singleTimeline

# ----------------------------------------------------------------------------------------------------------------------
