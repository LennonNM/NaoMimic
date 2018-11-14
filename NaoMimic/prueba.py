
# import sys
from Libraries import CSV_Utils as csvUtils
from Libraries import Calibration_Utils as calibration
import matplotlib.pyplot as plt

def  main(humanDir):

    # Get reference data
    HeadNao = csvUtils.readCSVNao("ref_HEAD", "HEAD")
    TorsoNao = csvUtils.readCSVNao("ref_TORSO", "TORSO")
    RArmNao, LArmNao = csvUtils.readCSVNao("ref_ARMS", "ARMS")
    x = range(len(RArmNao))
    plt.plot(x, RArmNao)

    # Make single CSV with adjusted data from MoCap
    # # Read data from each single CSV from calibration routines
    HeadP = csvUtils.readCSVMocap(humanDir+"Head", "HEAD")
    TorsoP = csvUtils.readCSVMocap(humanDir+"Torso", "TORSO")
    [RArmP, LArmP] = csvUtils.readCSVMocap(humanDir+"Arms", "ARMS")

    # # Sync data
    HeadSync = calibration.syncData(HeadNao, HeadP)
    TorsoSync = calibration.syncData(TorsoNao, TorsoP)
    RArmSync = calibration.syncData(RArmNao, RArmP)
    LArmSync = calibration.syncData(LArmNao, LArmP)
    dataEffectors = [HeadSync, TorsoSync, RArmSync, LArmSync]

    # # Write single CSV with adjusted data
    csvUtils.writeCSVMocapSingleAdjusted(dataEffectors, "NewSubject1/AdjustedData")

    # Create Calibration Profile from adjusted data CSV
    # # Read synced data
    HeadPerson = csvUtils.readCSVMocap("NewSubject1/AdjustedData", "HEAD")
    TorsoPerson = csvUtils.readCSVMocap("NewSubject1/AdjustedData", "TORSO")
    RArmPerson, LArmPerson = csvUtils.readCSVMocap("NewSubject1/AdjustedData", "ARMS")

    # # Get calibration terms
    HeadCoeff = calibration.getCalibrationTerms(HeadNao, HeadPerson)
    TorsoCoeff = calibration.getCalibrationTerms(TorsoNao, TorsoPerson)
    RArmCoeff = calibration.getCalibrationTerms(RArmNao, RArmPerson)
    LArmCoeff = calibration.getCalibrationTerms(LArmNao, LArmPerson)
    coefficientsList = [HeadCoeff, TorsoCoeff, RArmCoeff, LArmCoeff]

    # # Write Calibration Profile with terms
    csvUtils.writeCalibrationProfile(coefficientsList, "NewSubject1/AdjustedData")


if __name__ == "__main__":
    # main(sys.argv[1], sys.argv[2], sys.argv[3])
    main("Javier2/Javier")