"""
Functions for working with CSV files.
"""

# Imports
import csv
import os
import time
from os.path import dirname, abspath

# Project libraries
import Error_Utils as error

# ----------------------------------------------------------------------------------------------------------------------
# MoCap related
# ----------------------------------------------------------------------------------------------------------------------

def readCSVMocap(pathFile, whichEffectors = "ALL", includesHeader = True):
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
    :return dataHead, dataTorso, dataRArm, dataLArm, dataRLeg, dataLLeg: Each one a list with the data extracted from
        the CSV for each effector required.
    """

    # Open file from default directory
    rootDir = dirname(dirname(abspath(__file__)))
    dirNao = os.path.join(rootDir, "Calibration/Human/MoCap_Export/")
    dirNao = os.path.join(dirNao, pathFile + ".csv")
    try:
        fileNao = open(dirNao, 'rt', encoding="utf8")
    except Exception:
        error.abort("is not a valid directory or file", dirNao, "CalibrateFunc")
    reader = csv.reader(fileNao)
    rowsMocap = [r for r in reader]
    fileNao.close()
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
    if whichEffectors == "ALL":
        totalEffectors = 4 # 6
    elif whichEffectors == "ARMS" or whichEffectors == "LEGS":
        totalEffectors = 2
    elif (
            whichEffectors.upper() == "HEAD" or whichEffectors.upper() == "TORSO" or
            whichEffectors.upper() == "RARM" or whichEffectors.upper() == "LARM" or
            whichEffectors.upper() == "RLEG" or whichEffectors.upper() == "LLEG"
    ):
        totalEffectors = 1
    else:
        error.abort("is not a valid Effector definition", whichEffectors)

    dataEffector = [[] for k in range(totalEffectors)]  # list to store the data separated by effector
    countColumn = 0  # Counter to keep track of each set of axes per effector
    dataSet = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]  # Set of WX, WY, WZ, W, X, Y, Z
    countEffector = 1  # Counter of effectors passed per set extracted
    dataSetLen = len(dataSet)

    for i, item in enumerate(rowsData):
        for column in range(dataSetLen):
                try:
                    dataSet[countColumn] = float(rowsData[i].pop(0))
                except Exception:
                    error.abort("A value on " + dirNao + " is not valid when converting to float.")
                countColumn += 1

                # All columns for a single row covered
                if countColumn == dataSetLen - 1:
                    try:
                        dataSet[countColumn] = float(rowsData[i].pop(0))
                    except Exception:
                        error.abort("A value on " + dirNao + " is not valid when converting to float.")
                    countColumn = 0

                    # Organize data to the order: X, Y, Z, WX, WY, WZ
                    dataEffector[countEffector - 1].append([dataSet[4], dataSet[6], dataSet[5], dataSet[0], dataSet[2], dataSet[1]])

                    countEffector = 1 if countEffector == totalEffectors else countEffector + 1

    return dataEffector

# ----------------------------------------------------------------------------------------------------------------------

def writeCSVMocapSingleAdjusted(dataEffectors, pathCalProf):
    """
    This function is used to write a single CSV file containing the data for each calibration routine done for a specific
    set of effectors. The data sets received must be already time adjusted using syncData() from Calibrate_Utils.

    :param dataEffectors: List with the data to write. Must include all effectors.
    :param pathCalProf: Directory file to write the CSV file.
    :return: void
    """

    # Define location to store the file
    rootDir = dirname(dirname(abspath(__file__)))
    storeDir = os.path.join(rootDir, "Calibration/Human/CalibrationProfiles/")

    if pathCalProf.find("/") == -1:
        error.abort("Must specify the folder to store the file. Received only " + pathCalProf)
    folder = pathCalProf.split("/")
    storeDir = os.path.join(storeDir, folder[0])

    # If directory does not exist, create it
    if not os.path.exists(storeDir):
        print("Specified directory does not exist into CalibrationProfiles/" +
              "\nCreating " + storeDir
              )
        try:
            os.makedirs(storeDir)
        except Exception:
            error.abort("Failed to create directory " + storeDir)
        print("Directory " + storeDir + " successfully created")

    # Creating file
    storeDir += "/" + folder[1] + ".csv"
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
        + "Creating file " + storeDir +
          "\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
          )
    try:
        with open(storeDir, 'w') as csvfile:
            fieldnames = [
                'X Head', 'Y Head', 'Z Head', 'WX Head', 'WY Head', 'WZ Head',
                'X Torso', 'Y Torso', 'Z Torso', 'WX Torso', 'WY Torso', 'WZ Torso',
                'X RArm', 'Y RArm', 'Z RArm', 'WX RArm', 'WY RArm', 'WZ RArm',
                'X LArm', 'Y LArm', 'Z LArm', 'WX LArm', 'WY LArm', 'WZ LArm',
                # 'X RLeg', 'Y RLeg', 'Z RLeg', 'WX RLeg', 'WY RLeg', 'WZ RLeg',
                # 'X LLeg', 'Y LLeg', 'Z LLeg', 'WX LLeg', 'WY LLeg', 'WZ LLeg',
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for i in range(len(dataEffectors)):
                for j in range(len(dataEffectors[i])):
                    writer.writerow({
                        fieldnames[i*6]: dataEffectors[i][j][0], fieldnames[i*6+1]: dataEffectors[i][j][1],
                        fieldnames[i*6+2]: dataEffectors[i][j][2], fieldnames[i*6+3]: dataEffectors[i][j][3],
                        fieldnames[i*6+4]: dataEffectors[i][j][4], fieldnames[i*6+5]: dataEffectors[i][j][5],
                    })
    except Exception as e:
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
              "Failed to create" + storeDir +
              "\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        error.abort("")

    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
          "CSV file created succesfully" +
          "\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# Nao data related
# ----------------------------------------------------------------------------------------------------------------------

def writeCSVReference(dataSet, filePath = None, referenceFrame = "ROBOT", whichEffectors = "ALL"):
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

    :param filePath: Directory path to store the CSV file.
    :param dataSet: List with the data to export to file. Contains the set of axes for each desired effector.
    :param whichEffectors: Used to identify the amount of effectors included on the CSV file.
                    "ALL": Head, Torso, RArm, LArm, RLeg, LLeg
                    "ARMS": RArm, LArm
                    "LEGS": RLeg, LLeg
                    "_effector_": Uses a single effector, e.g. "Head".
    :return: void
    """

    # Identify involved effectors
    if whichEffectors.upper() == "ALL":
        # effectors = ["HEAD", "TORSO", "RARM", "LARM", "RLEG", "LLEG"]
        effectors = ["HEAD", "TORSO", "RARM", "LARM"]
    elif whichEffectors.upper() == "ARMS":
        effectors = ["RARM", "LARM"]
    elif whichEffectors.upper() == "LEGS":
        effectors = ["RLEG", "LLEG"]
    else:
        error.abort("is not a valid Effector definition", whichEffectors)

    # Default directory for files storage
    rootDir = dirname(dirname(abspath(__file__)))
    fileDir = os.path.join(rootDir, "Calibration/NAO/ReferenceData/Default/")
    if filePath is None:
        fileDir += referenceFrame + "_" + whichEffectors
        fileDir += time.strftime("_%Y-%m-%d_%H-%M-%S")
    else:
        fileDir += filePath
    fileDir += ".csv"

    # Create the CSV file
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
          "Creating CSV file as: " + fileDir +
          "\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    try:
        with open(fileDir, 'w') as csvfile:
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
    except Exception:
        error.abort("Failed to create file " + fileDir)

# ----------------------------------------------------------------------------------------------------------------------

def readCSVNao(pathFile, whichEffectors = "ALL"):
    """
    This function is used to extract the data from a CSV  file with data from the Nao's motion sensors. The order of
    appearance of the effectors must follow: Head, Torso, RArm, LArm, RLeg, LLeg. The CSV file is custom for the project
    and includes a single row header.

    :param pathFile: Path to the CSV file containing the calibration data from a MoCap recording from Motive.
    :param whichEffectors: Used to identify the amount of effectors included on the CSV file.
                    "ALL": Head, Torso, RArm, LArm, RLeg, LLeg
                    "ARMS": RArm, LArm
                    "LEGS": RLeg, LLeg
                    "_effector_": Uses a single effector, e.g. "Head".
    :return dataHead, dataTorso, dataRArm, dataLArm, dataRLeg, dataLLeg: Each one a list with the data extracted from
        the CSV for each effector required.
    """
    # Define return lists
    dataHead  = list()
    dataTorso = list()
    dataRArm  = list()
    dataLArm  = list()
    # dataRLeg  = list()
    # dataLLeg  = list()

    # Open file from default directory
    rootDir = dirname(dirname(abspath(__file__)))
    dirNao = os.path.join(rootDir, "Calibration/NAO/ReferenceData/")
    # Check if received path points to other dir rather tha Default
    if pathFile.find("/") == -1:
        dirNao = os.path.join(dirNao, "Default/")
    dirNao = os.path.join(dirNao, pathFile + ".csv")
    try:
        fileNao = open(dirNao, 'rt', encoding="utf8")
    except Exception:
        error.abort("is not a valid directory or file", dirNao, "Calibrate_Utils")
    reader = csv.reader(fileNao)
    rowsMocap = [r for r in reader]
    fileNao.close()
    del reader

    # ------------------------------------------------------------------------------

    # Begin extraction of the data from CSV

    # Numerical data starts from row No. 3
    rowsData = rowsMocap[2::]

    # Begin extraction of motion tracking data
    if whichEffectors.upper() == "ALL":
        totalEffectors = 4  # 6
    elif whichEffectors.upper() == "ARMS" or whichEffectors.upper() == "LEGS":
        totalEffectors = 2
    elif (
            whichEffectors.upper() == "HEAD" or whichEffectors.upper() == "TORSO" or
            whichEffectors.upper() == "RARM" or whichEffectors.upper() == "LARM" or
            whichEffectors.upper() == "RLEG" or whichEffectors.upper() == "LLEG"
    ):
        totalEffectors = 1
    else:
        error.abort("is not a valid Effector definition", whichEffectors)

    countColumn = 0  # Counter to keep track of each set of axes per effector
    dataSet = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]  # Set of WX, WY, WZ, X, Y, Z
    countEffector = 1  # Counter of effectors passed per set extracted
    dataSetLen = len(dataSet)

    for i, item in enumerate(rowsData):
        for column in range(dataSetLen):
            # try:
            dataSet[countColumn] = float(rowsData[i].pop(0))
            # except Exception:
            #     error.abort("A value on " + dirNao + " is not valid when converting to float.")
            countColumn += 1

            # All columns for a single row covered
            if countColumn == dataSetLen - 1:
                try:
                    dataSet[countColumn] = float(rowsData[i].pop(0))
                except Exception:
                    error.abort("A value on " + dirNao + " is not valid when converting to float.")
                countColumn = 0

                # Organize data to the order: X, Y, Z, WX, WY, WZ
                if countEffector == 1:
                    dataHead.append([dataSet[4], dataSet[5], dataSet[6], dataSet[0], dataSet[1], dataSet[2]])
                elif countEffector == 2:
                    dataTorso.append([dataSet[4], dataSet[5], dataSet[6], dataSet[0], dataSet[1], dataSet[2]])
                elif countEffector == 3:
                    dataRArm.append([dataSet[4], dataSet[5], dataSet[6], dataSet[0], dataSet[1], dataSet[2]])
                elif countEffector == 4:
                    dataLArm.append([dataSet[4], dataSet[5], dataSet[6], dataSet[0], dataSet[1], dataSet[2]])
                # elif countEffector == 5:
                #     dataRLeg.append([dataSet[4], dataSet[5], dataSet[6], dataSet[0], dataSet[1], dataSet[2]])
                # elif countEffector == 6:
                #     dataLLeg.append([dataSet[4], dataSet[5], dataSet[6], dataSet[0], dataSet[1], dataSet[2]])

                countEffector = 1 if countEffector == totalEffectors else countEffector + 1

    # return dataHead, dataTorso, dataRArm, dataLArm, dataRLeg, dataLLeg
    return dataHead, dataTorso, dataRArm, dataLArm

# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# Calibration Profiles related
# ----------------------------------------------------------------------------------------------------------------------

def readCalibrationProfile(fileName):
    """
    This function reads a Calibration Profile CSV file and returns a list with all the coefficients contained.

    :param fileName: Path to the desired Calibration Profile.
    :return coefficients: Coefficients that conforms the Calibration Profile.
    """

    print("Reading Calibration Profile from default directory .../Calibration/Human/CalibrationProfiles/")

    # Define path
    rootDir = dirname(dirname(abspath(__file__)))
    file = os.path.join(rootDir, "Calibration/Human/CalibrationProfiles/")
    file += fileName

    # Extract all data from file
    try:
        print("Opening file: " + fileName + ".csv")
        f = open(file, 'rt')
        reader = csv.reader(f)
        coefficients = [r for r in reader]  # Each row contains the coefficients of a single axis
        f.close()
    except Exception:
        error.abort("Could not open " + file)

    print("Data extracted from Calibration Profile " + file)

    return coefficients

# ----------------------------------------------------------------------------------------------------------------------

def writeCalibrationProfile(coefficients, fileName):
    """
    This functions is used to create a CSV file containing the coefficients to adjust a data set. The file does not
    include a header. Each row corresponds to a single axis, each effector uses 6 rows (X, Y, Z, WX, WY, WZ).

    :param coefficients: List with the coefficients to write into the Calibration Profile.
    :param fileName: Name of the Calibration Profile file. If "None" a generic name will be used.
    :return: void
    """

    # Define path
    rootDir = dirname(dirname(abspath(__file__)))
    file = os.path.join(rootDir, "Calibration/Human/CalibrationProfiles/")
    if fileName.find("/") == -1:
        error.abort("Must specify the folder to store the file. Received only " + fileName)
    folder = fileName.split("/")
    file = os.path.join(file, folder[0])
    if not os.path.exists(file):
        print("Specified directory does not exist into CalibrationProfiles/" +
              "\nCreating " + file
              )
        try:
            os.makedirs(file)
        except Exception:
            error.abort("Failed to create directory " + file)
        print("Directory " + file + " successfully created")
    file += folder[1]

    # Create file
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n" +
          "Creating Calibration Profile" +
          "\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    try:
        with open(file, 'w') as csvfile:
            writer = csv.writer(csvfile)
            for item in coefficients:
                for element in item:
                    writer.writerow(element)
    except Exception as e:
        error.abort("Could not create Calibration Profile")
