
# import sys
from Libraries import CSV_Utils as csvUtils
from Libraries import Calibration_Utils as calibration
from Libraries import Graph_Utils as compare

def  main(humanDir):

    # Get reference data
    HeadNao = csvUtils.readCSVNao("ref_HEAD", "HEAD")
    TorsoNao = csvUtils.readCSVNao("ref_TORSO", "TORSO")
    ARmsNao = csvUtils.readCSVNao("ref_ARMS", "ARMS")

    # Read data from each single CSV from calibration routines
    HeadP = csvUtils.readCSVMocap(humanDir+"Head", "HEAD")
    TorsoP = csvUtils.readCSVMocap(humanDir+"Torso", "TORSO")
    ARmsP = csvUtils.readCSVMocap(humanDir+"Arms", "ARMS")

    # Sync data (now data sets are gruped by axes instead of frame)
    HeadSync = calibration.syncData(HeadP, HeadNao)
    TorsoSync = calibration.syncData(TorsoP, TorsoNao)
    RArmSync = calibration.syncData(ARmsP[0], ARmsNao[0])
    LArmSync = calibration.syncData(ARmsP[1], ARmsNao[1])

    naoRArm = calibration.extractAxes(HeadNao)
    personRArm = calibration.extractAxes(HeadP)
    for i in range(6):
        compare.plotCompareSameAxis(HeadSync[i], personRArm[i], "Synced " + str(i),
                                    "Javier RArm " + str(i), naoRArm[i], "Nao " + str(i))

    # # # Write single CSV with adjusted data
    # csvUtils.writeCSVMocapSingleAdjusted(dataEffectors, "NewSubject1/AdjustedData")
    #
    # # Create Calibration Profile from adjusted data CSV
    # # # Read synced data
    # HeadPerson = csvUtils.readCSVMocap("NewSubject1/AdjustedData", "HEAD")
    # TorsoPerson = csvUtils.readCSVMocap("NewSubject1/AdjustedData", "TORSO")
    # RArmPerson, LArmPerson = csvUtils.readCSVMocap("NewSubject1/AdjustedData", "ARMS")
    #
    # # # Get calibration terms
    # HeadCoeff = calibration.getCalibrationTerms(HeadNao, HeadPerson)
    # TorsoCoeff = calibration.getCalibrationTerms(TorsoNao, TorsoPerson)
    # RArmCoeff = calibration.getCalibrationTerms(RArmNao, RArmPerson)
    # LArmCoeff = calibration.getCalibrationTerms(LArmNao, LArmPerson)
    # coefficientsList = [HeadCoeff, TorsoCoeff, RArmCoeff, LArmCoeff]
    #
    # # # Write Calibration Profile with terms
    # csvUtils.writeCalibrationProfile(coefficientsList, "NewSubject1/AdjustedData")


if __name__ == "__main__":
    # main(sys.argv[1], sys.argv[2], sys.argv[3])
    main("Javier2/Javier")