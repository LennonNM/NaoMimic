
# import sys
# import Calibrate_Func as cal
# import OffsetFile_Func as offset
import CSV_Utils as csv

def main(humanDir):
    # RArmNaoA, RLegNaoA, LLegNaoA, LArmNaoA, TorsoNaoA, HeadNaoA, RArmPA, RLegPA, LLegPA, LArmPA, TorsoPA, HeadPA = cal.setCalData(naoDir, humanDir, wRot)
    # RArmCorr = cal.syncData(RArmNaoA, RArmPA)
    # offset.writeOffsets(1, RArmCorr, wRot, "123")
    # HeadPA, TorsoPA, RArmPA, LArmPA = csv.readCSVMocap(humanDir)
    HeadNao, TorsoNao, RArmNao, LArmNao = csv.readCSVNao(humanDir)
    print(HeadNao)


if __name__ == "__main__":
    # main(sys.argv[1], sys.argv[2], sys.argv[3])
    # main("Javier/ArmsJavier")
    main("Brazos_NAO")