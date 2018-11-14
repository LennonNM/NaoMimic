"""
Functions for managing known errors to gracefully terminate the process.
"""

# Imports
import sys

# -------------------------------------------------------------------------------

def abort(errorMessage, processName = None, sysError = None):
    """
    This function is used to terminate the current process with a user defined error messages on terminal.

    :param errorMessage: Error message text to be displayed.
    :param error: Exception type variable from a 'catch-except'.
    :param processName: User defined name of the process being terminated.
    :return: void
    """

    # Build error message
    printMessage = ("\n\n++++++++++++++++++++++++++++++++++++++++++++++++++\n"
                    +   "      ERROR ON A NAO MIMIC PROCESS EXECUTION      \n\n")
    printMessage += errorMessage
    if processName is not None:
        printMessage += ("\n----------------\n"
                         + "Interrupted process: "
                         + processName
                         + "\n----------------\n")

    # Print error message and abort
    print(printMessage)

    # Message addition if there is system error info
    if sysError is not None:
        print("\n----------------\nSystem Error: ")
        print(sysError)
        print("\n----------------\n")

    # Print final section of message
    print("\n                 PROCESS ABORTED                  \n"
        + "++++++++++++++++++++++++++++++++++++++++++++++++++\n")

    sys.exit()

# -------------------------------------------------------------------------------
