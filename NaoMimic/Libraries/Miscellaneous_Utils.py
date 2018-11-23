"""
Functions to support general activities.
"""

# Imports
import sys
import os
import time

# -------------------------------------------------------------------------------

def abort(errorMessage, processName = None, sysError = None):
    """
    This function is used to terminate the current process with a defined error messages on terminal.

    :param errorMessage: Error message text to be displayed.
    :param error: Exception type variable from a 'catch-except'.
    :param processName: User defined name of the process being terminated.
    :return: void
    """

    # Build error message
    printMessage = ("\n\n**************************************************\n"
                    + "**************************************************\n"
                    + "      ERROR ON A NAO MIMIC PROCESS EXECUTION      \n\n")
    printMessage += errorMessage + "\n"
    if processName is not None:
        printMessage += ("\n----------------\n"
                         + "Interrupted process: "
                         + processName
                         + "\n----------------")

    # Print error message and abort
    print(printMessage)

    # Message addition if there is system error info
    if sysError is not None:
        print("\n----------------\nSystem Error: ")
        print(sysError)
        print("\n----------------\n")

    # Print final section of message
    print("\n                 PROCESS ABORTED                  \n"
          + "**************************************************\n"
          + "**************************************************\n")

    sys.exit()

# ----------------------------------------------------------------------------------------------------------------------

def checkDirExists(storeDir):
    """
    This function is used to check if the specified directory exists. If it does not exist, it creates it into the
    desired path.

    :param storeDir: Path of the directory to check.
    :return: void.
    """

    if not os.path.exists(storeDir):
        print("\n---------------------------------------\n"
              + storeDir + " does not exist.\n\n"
              + "\n\nCreating " + storeDir)
        time.sleep(3)
        try:
            os.makedirs(storeDir)
        except Exception as e1:
            error.abort("Failed to create directory \n" + storeDir, "Write CSV file with MoCap adjusted data", e1)
        print("\n\nDirectory\n" + storeDir + "\nsuccessfully created"
              + "\n---------------------------------------\n")

# ----------------------------------------------------------------------------------------------------------------------
