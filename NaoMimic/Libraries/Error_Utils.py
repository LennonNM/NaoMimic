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
    printMessage = ("\n\n++++++++++++++++++++++++++++++++++++++++++++++++++\n"
                    +   "      ERROR ON A NAO MIMIC PROCESS EXECUTION      \n\n")
    printMessage += errorMessage
    if processName is not None:
        printMessage += ("\n----------------\n"
                         + "Interrupted process: "
                         + processName
                         + "\n----------------\n")
    if sysError is not None:
        printMessage += ("\n----------------\nSystem Error: "
                        + sysError
                        + "\n----------------\n")
    printMessage +=  ("\n                 PROCESS ABORTED                  \n"
                      + "++++++++++++++++++++++++++++++++++++++++++++++++++\n")
    sys.exit()

# -------------------------------------------------------------------------------
