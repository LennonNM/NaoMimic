
# import sys
from Libraries import CSV_Utils as csvUtils
from Libraries import Calibration_Utils as calibration
import matplotlib.pyplot as plt

def  main(humanDir):

    # Get reference data
    HeadNao = csvUtils.readCSVNao("ref_HEAD", "HEAD")
    TorsoNao = csvUtils.readCSVNao("ref_TORSO", "TORSO")
    ARmsNao = csvUtils.readCSVNao("ref_ARMS", "ARMS")

    # Make single CSV with adjusted data from MoCap
    # # Read data from each single CSV from calibration routines
    HeadP = csvUtils.readCSVMocap(humanDir+"Head", "HEAD")
    TorsoP = csvUtils.readCSVMocap(humanDir+"Torso", "TORSO")
    ARmsP = csvUtils.readCSVMocap(humanDir+"Arms", "ARMS")

    NaoX = list()
    NaoY = list()
    NaoZ = list()
    NaoWX = list()
    NaoWY = list()
    NaoWZ = list()
    for row in ARmsNao[0]:
        NaoX.append(row[0])
        NaoY.append(row[1])
        NaoZ.append(row[2])
        NaoWX.append(row[3])
        NaoWY.append(row[4])
        NaoWZ.append(row[5])
    PX = list()
    PY = list()
    PZ = list()
    PWX = list()
    PWY = list()
    PWZ = list()
    for row in ARmsP[0]:
        PX.append(row[0])
        PY.append(row[1])
        PZ.append(row[2])
        PWX.append(row[3])
        PWY.append(row[4])
        PWZ.append(row[5])

    # # Sync data
    HeadSync = calibration.syncData(HeadNao, HeadP)
    TorsoSync = calibration.syncData(TorsoNao, TorsoP)
    RArmSync = calibration.syncData(ARmsNao[0], ARmsP[0])
    LArmSync = calibration.syncData(ARmsNao[1], ARmsP[1])
    # dataEffectors = [HeadSync, TorsoSync, RArmSync, LArmSync]

    plt.plot(NaoX, label="Nao X")
    plt.plot(PX, label="Javier X")
    plt.plot(RArmSync[0], label="Synced X")
    plt.legend(loc='upper left', bbox_to_anchor=(0.5, -0.1))
    plt.show()
    plt.plot(NaoY, label="Nao X")
    plt.plot(PY, label="Javier X")
    plt.plot(RArmSync[1], label="Synced X")
    plt.legend(loc='upper left', bbox_to_anchor=(0.5, -0.1))
    plt.show()
    plt.plot(NaoZ, label="Nao X")
    plt.plot(PZ, label="Javier X")
    plt.plot(RArmSync[2], label="Synced X")
    plt.legend(loc='upper left', bbox_to_anchor=(0.5, -0.1))
    plt.show()
    plt.plot(NaoWX, label="Nao X")
    plt.plot(PWX, label="Javier X")
    plt.plot(RArmSync[3], label="Synced X")
    plt.legend(loc='upper left', bbox_to_anchor=(0.5, -0.1))
    plt.show()
    plt.plot(NaoWY, label="Nao X")
    plt.plot(PWY, label="Javier X")
    plt.plot(RArmSync[4], label="Synced X")
    plt.legend(loc='upper left', bbox_to_anchor=(0.5, -0.1))
    plt.show()
    plt.plot(NaoWZ, label="Nao X")
    plt.plot(PWZ, label="Javier X")
    plt.plot(RArmSync[5], label="Synced X")
    plt.legend(loc='upper left', bbox_to_anchor=(0.5, -0.1))
    plt.show()

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