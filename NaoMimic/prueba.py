
# import sys
# import Calibrate_Func as cal
# import OffsetFile_Func as offset
import CSV_Utils as csv

def main(naoDir, humanDir):

    HeadP = csv.readCSVMocap(humanDir, "HEAD")
    TorsoP = csv.readCSVMocap(humanDir, "TORSO")
    RArmP, LArmP = csv.readCSVMocap(humanDir, "ARMS")
    # RLegP, LLegP = csv.readCSVMocap(humanDir, "LEGS")


    HeadNao = csv.readCSVNao(naoDir, "HEAD")
    HeadNao = csv.readCSVNao(naoDir, "TORSO")
    HeadNao = csv.readCSVNao(naoDir, "ARMS")
    # HeadNao = csv.readCSVNao(naoDir, "LEGS")
    TorsoNao, RArmNao, LArmNao = csv.readCSVNao(naoDir)
    print(HeadNao)


if __name__ == "__main__":
    # main(sys.argv[1], sys.argv[2], sys.argv[3])
    main("Brazos_NAO", "Javier/ArmsJavier")