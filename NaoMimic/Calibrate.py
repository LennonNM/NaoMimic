"""
This script is used to run the calibration process to generate a calibration profile.

Parameters
----------
pathMocap : Path to the MoCap CSV export with the data from the person to calibrate. Directory must be inside
            .../Calibration/Human/MoCap_Export/
pathReferences : Path to the reference CSV files with Nao's data. Directory must be inside
            .../Calibration/NAO/ReferenceData/. If no path is specified, the default path will be used to read the
            reference data -> .../Calibration/NAO/ReferenceData/Default/
calProfileDir : Path to store the Calibration Profile. Must be inside .../Calibration/Human/CalibrationProfiles/


Files created
-------------
AdjustedDataSet : CSV file with the main data sets of each individual calibration routine MoCap export. The data
            contained is fully adjusted to be used to generate the main Calibration Profile file.
CalibrationProfile : Identified as ´CP´ file. Contains the coefficients of the mathematical relation obtained by the
            calibration process for the specified person according to the specified reference data.

Notes on usage
--------------
The default reference files are recognize by the name format ´ref_EFFECTORNAME´ (e.g. ref_ARMS.csv contains reference
            data for RArm and LArm).
"""

# Project libraries
from Libraries import Calibration_Utils as calibration
from Libraries import Miscellaneous_Utils as misc

# ----------------------------------------------------------------------------------------------------------------------


def main(pathMocap, calProfileDir, pathReferences="Defaul"):

    calibration.performFullCalibration(pathMocap, pathReferences, calProfileDir)

# ----------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":

    if len(sys.argv) == 4:
        pathMocap = sys.argv[1]
        calProfileDir = sys.argv[2]
        pathReferences = sys.argv[3]
    elif len(sys.argv) == 3:
        pathMocap = sys.argv[1]
        calProfileDir = sys.argv[2]
    else:
        misc.abort("Expected 2 to 3 arguments.")

    time.sleep(1.0)
    main(pathMocap, calProfileDir, pathReferences)
