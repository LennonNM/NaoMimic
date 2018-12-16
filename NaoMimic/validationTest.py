
# import sys
from Libraries import Calibration_Utils as calibration
from Libraries import  CSV_Utils as csvUtils
from Libraries import Graph_Utils as graph
from Libraries import Mimic_Utils as mimic

# ----------------------------------------------------------------------------------------------------------------------


def main(pathMocap, pathReferences, calProfileDir):

    # Generating Calibration Profiles
    for subjectNo, subject in enumerate(pathMocap):
        for takeNo, take in enumerate(subject):
            calibration.performFullCalibration(pathMocap[subjectNo][takeNo],
                                               pathReferences,
                                               calProfileDir[subjectNo][takeNo],
                                               True)
    # calibration.performFullCalibration(pathMocap[0][0], pathReferences, calProfileDir[0][0], True)

    # ------------------------------------------------------------------------------------------------------------------

    

# ----------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    pathSubject1 = ["Validation3/Javier/Take1/Javier",
                    "Validation3/Javier/Take2/Javier",
                    "Validation3/Javier/Take3/Javier",
                    "Validation3/Javier/Take4/Javier",
                    "Validation3/Javier/Take5/Javier"]
    pathSubject2 = ["Validation3/Naty/Take1/Naty_",
                    "Validation3/Naty/Take2/Naty_",
                    "Validation3/Naty/Take3/Naty_",
                    "Validation3/Naty/Take4/Naty_",
                    "Validation3/Naty/Take5/Naty_"]
    pathCalibrationFile = ["Validation3/Javier_FPSAdjust/Take1/Javier",
                    "Validation3/Javier_FPSAdjust/Take2/Javier",
                    "Validation3/Javier_FPSAdjust/Take3/Javier",
                    "Validation3/Javier_FPSAdjust/Take4/Javier",
                    "Validation3/Javier_FPSAdjust/Take5/Javier"]
    # pathRefNao = ["Validation2/ref_HEAD",
    #               "Validation2/ref_TORSO",
    #               "Validation2/ref_ARMS"]
    # pathRefNao = ["Validation3/ref_Head_Val3",
    #               "Validation3/ref_Torso_Val3",
    #               "Validation3/ref_Arms_Val3"]
    pathRefNao = ["Validation3/Head_prueba",
                  "Validation3/Torso_prueba",
                  "Validation3/Arms_prueba"]

    # main([pathSubject2], pathRefNao, [pathSubject2])
    main([pathSubject1, pathSubject2], pathRefNao, [pathSubject1, pathSubject2])
