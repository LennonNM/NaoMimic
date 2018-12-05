"""
Functions for working with CSV files.
"""

# Imports
import csv
import os
import time
from os.path import dirname, abspath

# Project libraries
from Libraries import Miscellaneous_Utils as misc
from Libraries import Calibration_Utils as cal

# ----------------------------------------------------------------------------------------------------------------------
# MoCap related
# ----------------------------------------------------------------------------------------------------------------------


def readCSVMocap(pathFile, whichEffectors="ALL", includesHeader=True, isChoreography=False):
    """
    This function is used to extract the data from a MoCap recording export to CSV from Motive. The order of appearance
    of the effectors must follow: Head, Torso, RArm, LArm, RLeg, LLeg. If Header from Motive export is included,
    it is supposed that the "Error Per Marker" is not included.

    :param pathFile: Path to the CSV file containing the calibration data from a MoCap recording from Motive.
    :param whichEffectors: Used to identify the amount of effectors included on the CSV file.
                    "ALL": Head, Torso, RArm, LArm, RLeg, LLeg
                    "ARMS": RArm, LArm
                    "LEGS": RLeg, LLeg
                    "_effector_": Uses a single effector, e.g. "Head".
    :param includesHeader: True if the file includes the default header from Motive
    :param isChoreography: True to use .../Choreography as default directory to look up CSV files instead of
                .../Calibration/Human/MoCap_Export
    :return dataEffectors: List with the data extracted from the reference CSV for each effector required.
    """

    # Open file from default directory
    rootDir = dirname(dirname(abspath(__file__)))
    if isChoreography:
        dirMocap = os.path.join(rootDir, "Choreography/")
    else:
        dirMocap = os.path.join(rootDir, "Calibration/Human/MoCap_Export/")
    dirMocap = os.path.join(dirMocap, pathFile + ".csv")
    try:
        # fileMocap = open(dirMocap, 'rt', encoding="utf8")
        fileMocap = open(dirMocap, 'rt')
    except IOError as e1:
        misc.abort(dirMocap + " is not a valid directory or file", "Read CSV file with MoCap exported data", e1)
    reader = csv.reader(fileMocap)
    rowsMocap = [r for r in reader]
    fileMocap.close()
    del reader

    # ------------------------------------------------------------------------------

    # Begin extraction of the data from CSV
    # NOTE: Y and Z axis are switched on Motive in comparison with the Nao's reference frame. The respective adjustment
    # is considered.

    if includesHeader:
        # Numerical data starts from row No. 8 if the header from Motive is included
        rowsData = rowsMocap[7::]
    else:
        rowsData = rowsMocap

    # Columns "Frame" and "Time" are not used. It is supposed a 30 FPS rate
    for i, item in enumerate(rowsData):
        del rowsData[i][0]  # Removes "Frame"
        del rowsData[i][0]  # Removes "Time"

    # Begin extraction of motion tracking data
    if whichEffectors.upper() == "ALL":
        totalEffectors = 4  # 6
        for i in range(len(rowsData)):
            del rowsData[i][7 * 4::]
    elif whichEffectors.upper() == "ARMS":
        totalEffectors = 2
        for i in range(len(rowsData)):
            del rowsData[i][7 * 4::]
            del rowsData[i][0:7 * 2]
    # elif whichEffectors.upper() == "LEGS":
    #     totalEffectors = 2
    elif whichEffectors.upper() == "HEAD":
        totalEffectors = 1
        for i in range(len(rowsData)):
            del rowsData[i][7::]
    elif whichEffectors.upper() == "TORSO":
        totalEffectors = 1
        for i in range(len(rowsData)):
            del rowsData[i][7 * 2::]
            del rowsData[i][0:7]
    elif whichEffectors.upper() == "RARM":
        totalEffectors = 1
        for i in range(len(rowsData)):
            del rowsData[i][7 * 3::]
            del rowsData[i][0:7 * 2]
    elif whichEffectors.upper() == "LARM":
        totalEffectors = 1
        for i in range(len(rowsData)):
            del rowsData[i][7 * 4::]
            del rowsData[i][0:7 * 3]
    elif whichEffectors.upper() == "RLEG":
        totalEffectors = 1
    elif whichEffectors.upper() == "LLEG":
        totalEffectors = 1
    else:
        misc.abort(whichEffectors + " is not a valid Effector definition", "Read CSV file with reference data")

    dataEffectors = [[] for k in range(totalEffectors)]  # list to store the data separated by effector
    dataSet = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]  # Set of WX, WY, WZ, W, X, Y, Z
    dataSetLen = len(dataSet)

    for countEffector in range(totalEffectors):
        for rowNo, row in enumerate(rowsData):
            for columnNo in range(dataSetLen):
                    try:
                        dataSet[columnNo] = float(rowsData[rowNo].pop(0))
                    except ValueError as e2:
                        misc.abort("A value on \n" + dirMocap + "\nis not valid when converting to float",
                                    "Read CSV file with MoCap exported data", e2)

                    # All columns for a single row covered
                    if columnNo == dataSetLen - 1:
                        # Organize data to the order: X, Y, Z, WX, WY, WZ
                        dataEffectors[countEffector].append([dataSet[4], dataSet[6], dataSet[5],
                                                             dataSet[0], dataSet[2], dataSet[1]])

    if totalEffectors == 1:
        return dataEffectors[0]
    else:
        return dataEffectors

# ----------------------------------------------------------------------------------------------------------------------


def writeCSVMocapSingleAdjusted(dataSet, pathCalProf, joinAxes=True):
    """
    This function is used to write a single CSV file containing the data for each calibration routine done for a
    specific set of effectors. The data sets received must be already time adjusted using syncData() from
    Calibrate_Utils.

    :param dataSet: List with the data to write. Must include all effectors.
    :param pathCalProf: Directory file to write the CSV file.
    :param joinAxes: True if data set received is organized as axes data set [[X], [Y], [Z], [WX], [WY], [WZ]] to join
                the axes data into a data set of a row per axes set [[X, Y, Z, WX, WY, WZ]].
    :return: void
    """

    # Join axes data set into a data set of all axes per row, if needed
    if joinAxes:
        dataEffectors = [[] for k in range(len(dataSet))]
        for effectorNo, effector in enumerate(dataSet):
            dataEffectors[effectorNo] = cal.joinAxesInRow(effector)
    else:
        dataEffectors = dataSet

    # Define location to store the file
    rootDir = dirname(dirname(abspath(__file__)))
    storeDir = os.path.join(rootDir, "Calibration/Human/CalibrationProfiles/")

    if pathCalProf.find("/") == -1:
        misc.abort("Must specify the folder to store the file. Received only " + pathCalProf,
                    "Write CSV file with MoCap adjusted data")
    folder = pathCalProf.split("/")
    fileName = folder.pop(-1)
    for item in folder:
        storeDir += "/" + item

    # If directory does not exist, create it
    misc.checkDirExists(storeDir)

    # Creating file
    storeDir += "/" + fileName+ ".csv"
    storeDir = checkCSVFileExists(storeDir)

    print("\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
        + "Creating file \n" + storeDir +
          "\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
          )
    time.sleep(3)

    try:
        # with open(storeDir, 'wb') as csvfile:  # Python 2.x
        with open(storeDir, 'w', newline='') as csvfile:  # Python 3.x
            fieldnames = [
                'X Head', 'Y Head', 'Z Head', 'WX Head', 'WY Head', 'WZ Head',
                'X Torso', 'Y Torso', 'Z Torso', 'WX Torso', 'WY Torso', 'WZ Torso',
                'X RArm', 'Y RArm', 'Z RArm', 'WX RArm', 'WY RArm', 'WZ RArm',
                'X LArm', 'Y LArm', 'Z LArm', 'WX LArm', 'WY LArm', 'WZ LArm'#,
                # 'X RLeg', 'Y RLeg', 'Z RLeg', 'WX RLeg', 'WY RLeg', 'WZ RLeg',
                # 'X LLeg', 'Y LLeg', 'Z LLeg', 'WX LLeg', 'WY LLeg', 'WZ LLeg',
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            # Find maximum amount of rows
            maxRows = max(len(dataEffectors[0]), len(dataEffectors[1]), len(dataEffectors[2]), len(dataEffectors[3]))
            rowToWrite = dict()
            for rowNo in range(maxRows):
                for effectorNo in range(len(dataEffectors)):
                    for axis in range(6):
                        try:
                            rowToWrite.update({fieldnames[6*effectorNo + axis]: dataEffectors[effectorNo][rowNo][axis]})
                        except IndexError:
                            # Manage when passing over the end of a shorter effector list
                            # # Leave the space in blank because there is no important info to write
                            rowToWrite[fieldnames[6 * effectorNo + axis]] = None
                writer.writerow(rowToWrite)

    except IOError as e2:
        misc.abort("Failed to create" + storeDir, "Write CSV file with MoCap adjusted data", e2)

    print("\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
          "\nCSV file created succesfully" +
          "\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# Nao data related
# ----------------------------------------------------------------------------------------------------------------------


def writeCSVReference(dataSet, filePath=None, referenceFrame="ROBOT", whichEffectors="ALL"):
    """
    This function is used to write a CSV file with the position data exported from the Nao's sensors.
    Header of the file goes as follows:

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Effector1  ,Effector1,Effector1,Effector1,Effector1,Effector1,Effector2,...
    # rotX       ,rotY     ,rotZ     ,posX     ,posY     ,posZ     ,rotX     ,...
    # valTake1   ,valTake1 ,valTake1 ,valTake1 ,valTake1 ,valTake1 ,valTake1 ,...
    # valTake2   ,valTake2 ,valTake2 ,valTake2 ,valTake2 ,valTake2 ,valTake2 ,...
    # ...
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    :param dataSet: List with the data to export to file. Contains the set of axes for each desired effector.
    :param filePath: Directory path to store the CSV file.
    :param referenceFrame: Name of the Nao's reference frame.
    :param whichEffectors: Used to identify the amount of effectors included on the CSV file.
                    "ALL": Head, Torso, RArm, LArm, RLeg, LLeg
                    "ARMS": RArm, LArm
                    "LEGS": RLeg, LLeg
                    "_effector_": Uses a single effector, e.g. "Head".
    :return: void
    """

    # Identify if desired effectors are valid
    if whichEffectors.upper() != "ALL" and whichEffectors.upper() != "ARMS" and whichEffectors.upper() != "LEGS":
        misc.abort(whichEffectors + " is not a valid Effector definition", "Write CSV with reference data")

    # Default directory for files storage
    rootDir = dirname(dirname(abspath(__file__)))
    fileDir = os.path.join(rootDir, "Calibration/NAO/ReferenceData/Default/")
    if filePath is None:
        fileDir += referenceFrame + "_" + whichEffectors
        fileDir += time.strftime("_%Y-%m-%d_%H-%M-%S")
    else:
        fileDir += filePath
    fileDir += ".csv"

    fileDir = checkCSVFileExists(fileDir)

    # Create the CSV file
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
          "Creating CSV file as: " + fileDir +
          "\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    time.sleep(3)
    try:
        # with open(fileDir, 'wb') as csvfile:  # Python 2.x
        with open(fileDir, 'w', newline='') as csvfile:  # Python 3.x
            # Define columns
            fieldnames = list()
            if whichEffectors.upper() == "ALL":
                fieldnames = [
                    'WX Head', 'WY Head', 'WZ Head', 'X Head', 'Y Head', 'Z Head',
                    'WX Torso', 'WY Torso', 'WZ Torso', 'X Torso', 'Y Torso', 'Z Torso',
                    'WX RArm', 'WY RArm', 'WZ RArm', 'X RArm', 'Y RArm', 'Z RArm',
                    'WX LArm', 'WY LArm', 'WZ LArm', 'X LArm', 'Y LArm', 'Z LArm',
                    # 'WX RLeg', 'WY RLeg', 'WZ RLeg', 'X RLeg', 'Y RLeg', 'Z RLeg',
                    # 'WX LLeg', 'WY LLeg', 'WZ LLeg', 'X LLeg', 'Y LLeg', 'Z LLeg',
                ]
            elif whichEffectors.upper() == "ARMS" or whichEffectors.upper() == "LEGS":
                fieldnames = [
                    'WX Right', 'WY Right', 'WZ Right', 'X Right', 'Y Right', 'Z Right',
                    'WX Left', 'WY Left', 'WZ Left', 'X Left', 'Y Left', 'Z Left',
                ]
            elif (
                    whichEffectors.upper() == "HEAD" or whichEffectors.upper() == "TORSO" or
                    whichEffectors.upper() == "RARM" or whichEffectors.upper() == "LARM" or
                    whichEffectors.upper() == "RLEG" or whichEffectors.upper() == "LLEG"
            ):
                fieldnames = [
                    'WX', 'WY', 'WZ', 'X', 'Y', 'Z'
                ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Write header info
            writer.writeheader()

            # Write rows with data
            if whichEffectors == "ALL":
                for i in range(len(dataSet[0])):
                    writer.writerow({
                        'WX Head': dataSet[0][i][3], 'WY Head': dataSet[0][i][4], 'WZ Head': dataSet[0][i][5],
                        'X Head': dataSet[0][i][0], 'Y Head': dataSet[0][i][1], 'Z Head': dataSet[0][i][2],
                        'WX Torso': dataSet[1][i][3], 'WY Torso': dataSet[1][i][4], 'WZ Torso': dataSet[1][i][5],
                        'X Torso': dataSet[1][i][0], 'Y Torso': dataSet[1][i][1], 'Z Torso': dataSet[1][i][2],
                        'WX RArm': dataSet[2][i][3], 'WY RArm': dataSet[2][i][4], 'WZ RArm': dataSet[2][i][5],
                        'X RArm': dataSet[2][i][0], 'Y RArm': dataSet[2][i][1], 'Z RArm': dataSet[2][i][2],
                        'WX LArm': dataSet[3][i][3], 'WY LArm': dataSet[3][i][4], 'WZ LArm': dataSet[3][i][5],
                        'X LArm': dataSet[3][i][0], 'Y LArm': dataSet[3][i][1], 'Z LArm': dataSet[3][i][2]#,
                    # 'WX RLeg': dataSet[4][i][3], 'WY RLeg': dataSet[4][i][4], 'WZ RLeg': dataSet[4][i][5],
                    # 'X RLeg': dataSet[5][i][0], 'Y RLeg': dataSet[4][i][1], 'Z RLeg': dataSet[4][i][2],
                    # 'WX LLeg': dataSet[5][i][3], 'WY LLeg': dataSet[5][i][4], 'WZ LLeg': dataSet[5][i][5],
                    # 'X LLeg': dataSet[5][i][0], 'Y LLeg': dataSet[5][i][1], 'Z LLeg': dataSet[5][i][2]
                    })
            elif whichEffectors == "ARMS" or whichEffectors == "LEGS":
                for i in range(len(dataSet[0])):
                    writer.writerow({
                        'WX Right': dataSet[0][i][3], 'WY Right': dataSet[0][i][4], 'WZ Right': dataSet[0][i][5],
                        'X Right': dataSet[0][i][0], 'Y Right': dataSet[0][i][1], 'Z Right': dataSet[0][i][2],
                        'WX Left': dataSet[1][i][3], 'WY Left': dataSet[1][i][4], 'WZ Left': dataSet[1][i][5],
                        'X Left': dataSet[1][i][0], 'Y Left': dataSet[1][i][1], 'Z Left': dataSet[1][i][2]
                    })
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
              "CSV file created succesfully" +
              "\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    except Exception as e1:
        misc.abort("Failed to create file " + fileDir, "Write CSV with reference data", e1)

# ----------------------------------------------------------------------------------------------------------------------


def readCSVNao(pathFile, whichEffectors="ALL"):
    """
    This function is used to extract the data from a CSV  file with data from the Nao's motion sensors. The order of
    appearance of the effectors must follow: Head, Torso, RArm, LArm, RLeg, LLeg. The CSV file is custom for the project
    and includes a single row header.

    :param pathFile: Path to the CSV file containing the reference calibration data extracted from the Nao with
                    GetPositions.
    :param whichEffectors: Used to identify the amount of effectors included on the CSV file.
                    "ALL": Head, Torso, RArm, LArm, RLeg, LLeg
                    "ARMS": RArm, LArm
                    "LEGS": RLeg, LLeg
                    "_effector_": Uses a single effector, e.g. "Head".
    :return dataEffectors: List with the data extracted from the reference CSV for each effector required.
    """

    # Open file from default directory
    rootDir = dirname(dirname(abspath(__file__)))
    dirNao = os.path.join(rootDir, "Calibration/NAO/ReferenceData/")
    # Check if received path points to other dir rather tha Default
    if pathFile.find("/") == -1:
        dirNao = os.path.join(dirNao, "Default/")
    dirNao = os.path.join(dirNao, pathFile + ".csv")
    try:
        # fileNao = open(dirNao, 'rt', encoding="utf8")
        fileNao = open(dirNao, 'rt')
    except IOError as e1:
        misc.abort(dirNao + " is not a valid directory or file", "Read CSV file with reference data", e1)
    reader = csv.reader(fileNao)
    rowsMocap = [r for r in reader]
    fileNao.close()
    del reader

    # ------------------------------------------------------------------------------

    # Begin extraction of the data from CSV

    # Numerical data starts from row No. 1
    rowsData = rowsMocap[1::]

    # Begin extraction of motion tracking data
    if whichEffectors.upper() == "ALL":
        totalEffectors = 4  # 6
    elif whichEffectors.upper() == "ARMS":
        totalEffectors = 2
        for i in range(len(rowsData)):
            del rowsData[i][6 * 4::]
            del rowsData[i][0:6 * 2]
    # elif whichEffectors.upper() == "LEGS":
    #     totalEffectors = 2
    elif whichEffectors.upper() == "HEAD":
        totalEffectors = 1
        for i in range(len(rowsData)):
            del rowsData[i][6::]
    elif whichEffectors.upper() == "TORSO":
        totalEffectors = 1
        for i in range(len(rowsData)):
            del rowsData[i][6 * 2::]
            del rowsData[i][0:6]
    elif whichEffectors.upper() == "RARM":
        totalEffectors = 1
        for i in range(len(rowsData)):
            del rowsData[i][6 * 3::]
            del rowsData[i][0:6 * 2]
    elif whichEffectors.upper() == "LARM":
        totalEffectors = 1
        for i in range(len(rowsData)):
            del rowsData[i][6 * 4::]
            del rowsData[i][0:6 * 3]
    elif whichEffectors.upper() == "RLEG":
        totalEffectors = 1
    elif whichEffectors.upper() == "LLEG":
        totalEffectors = 1
    else:
        misc.abort(whichEffectors + " is not a valid Effector definition", "Read CSV file with reference data")

    dataEffectors = [[] for k in range(totalEffectors)]
    dataSet = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]  # Set of WX, WY, WZ, X, Y, Z
    dataSetLen = len(dataSet)

    for countEffector in range(totalEffectors):
        for rowNo, row in enumerate(rowsData):
            for columnNo in range(dataSetLen):
                try:
                    dataSet[columnNo] = float(rowsData[rowNo].pop(0))
                except TypeError as e:
                    misc.abort("A value on " + fileNao + " is not valid when converting to float",
                                "Read CSV file with reference data", e)

                # Last column for a single row extracted
                if columnNo == dataSetLen - 1:
                    # Organize data to the order: X, Y, Z, WX, WY, WZ
                    dataEffectors[countEffector].append([dataSet[3], dataSet[4], dataSet[5],
                                                         dataSet[0], dataSet[1], dataSet[2]])

    if totalEffectors == 1:
        return dataEffectors[0]
    else:
        return dataEffectors

# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# Calibration Profiles related
# ----------------------------------------------------------------------------------------------------------------------


def readCalibrationFile(filePath):
    """
    This function reads a Calibration Profile CSV file and returns a list with all the coefficients contained.
    The coefficients are ordered per row and per effector's axis, meaning first 6 rows corresponds to the axes
    X, Y, Z, WX, WY, WZ for Head effector, the next 6 rows the same for Torso and so on.

    :param filePath: Path to the desired Calibration Profile.
    :return coefficients: Coefficients that conforms the Calibration Profile.
    """

    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
          + "Reading Calibration Profile from default directory \n.../Calibration/Human/CalibrationProfiles/")
    time.sleep(3)

    # Define path
    rootDir = dirname(dirname(abspath(__file__)))
    fileDir = os.path.join(rootDir, "Calibration/Human/CalibrationProfiles/")
    fileDir += filePath + ".csv"

    # Extract all data from file
    try:
        print("\n------------------------------------------------------------------\nOpening file:\n" + fileDir)
        time.sleep(3)
        f = open(fileDir, 'rt')
        reader = csv.reader(f)
        coefficients = [row for row in reader]  # Each row contains the coefficients of a single axis
        f.close()
    except Exception as e:
        misc.abort("Could not open " + fileDir, "Read Calibration Profile", e)

    print("\nData extracted from Calibration Profile \n" + fileDir
          + "\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

    return coefficients

# ----------------------------------------------------------------------------------------------------------------------


def writeCalibrationProfile(coefficients, filePath):
    """
    This functions is used to create a CSV file containing the coefficients to adjust a data set. The file does not
    include a header. Each row corresponds to the coefficients of a single axis, each effector uses 6 rows
    (X, Y, Z, WX, WY, WZ).

    :param coefficients: List with the coefficients to write into the Calibration Profile.
    :param filePath: Name of the Calibration Profile file. If "None" a generic name will be used.
    :return: void
    """

    # Define path
    rootDir = dirname(dirname(abspath(__file__)))
    calPath = os.path.join(rootDir, "Calibration/Human/CalibrationProfiles/")
    if filePath.find("/") == -1:
        misc.abort("Must specify the folder to store the file. Received only " + filePath, "Write Calibration Profile")

    folder = filePath.split("/")
    fileName = folder.pop(-1)
    for item in folder:
        calPath += item + "/"

    # Check if directory exists
    misc.checkDirExists(calPath)

    # Check if file exists
    calPath += fileName + "_CP.csv"
    calPath = checkCSVFileExists(calPath)

    # Create file
    print("\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
          + "Creating Calibration Profile as:\n" + calPath)
    time.sleep(3)
    try:
        # with open(calPath, 'wb') as csvfile:  # Python 2.x
        with open(calPath, 'w', newline='') as csvfile:  # Python 3.x
            writer = csv.writer(csvfile)
            for item in coefficients:
                for element in item:
                    writer.writerow(element)
    except IOError as e2:
        misc.abort("Could not create Calibration Profile", "Write Calibration Profile", e2)

    print("\nCalibration Profile Created Successfully as:\n" + calPath
          + "\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

# ----------------------------------------------------------------------------------------------------------------------


def checkCSVFileExists(pathToFile):
    """
    This function is used to check if the desired file to be created already exists on specified directory. Prompts the
    user to input the new name of the file or to overwrite the existing one.

    :param pathToFile: Full path to the file to check.
    :return filePath: Verified path to file to create.
    """

    # Split file name and path
    pathSplit = pathToFile.split("/")
    fileName = pathSplit.pop(-1)
    # Rejoin path
    filePath = ""
    for item in pathSplit:
        filePath += item + "/"
    # Check if file name already has extension
    if fileName.find(".") != -1:
        fileName = fileName.split(".")[0]  # Delete extension

    checkFile = True
    while (checkFile):
        if os.path.exists(filePath + fileName + ".csv"):
            print("\n------------------------------------------------------------------\n"
                  + "File already exists as :\n" + filePath + fileName + ".csv")
            # response = raw_input("OVERWRITE FILE? (Y/N):  ").upper()  # Python 2.x
            response = input("OVERWRITE FILE? (Y/N):  ").upper()  # Python 3.x
            if response == "N":
                # fileName = raw_input("Write the NAME of the file to create and then press [ENTER]."
                #                  + "\nPath of folder remains the same.\n")  # Python 2.x
                fileName = input("Write the NAME of the file to create and then press [ENTER]."
                                 + "\nPath of folder remains the same.\n")
                checkFile = True
            elif response == "Y":
                filePath += fileName + ".csv"
                print("File will be overwritten.")
                checkFile = False
            else:
                print("Wrong input received.")
                checkFile = True
        else:
            filePath += fileName + ".csv"
            checkFile = False

    return filePath

# ----------------------------------------------------------------------------------------------------------------------
