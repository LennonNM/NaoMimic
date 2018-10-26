#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#Manejo de errores de uso de la aplicacion. Recibe explicacion del error,
#script donde se dio el error, y entrada recibida que ocasiono el error (opcional)
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#Imports
import sys

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#abort: ocasiona un aborto de la operacion en proceso
def abort(explanation, value=None, program=None, called=None):
    print "---------------------------------------------------"
    print "ERROR on Teleoperation Execution:"
    if value is not None:
        print "        Received", value
        print "   ", explanation
        if called is not None:
            print "        Called from:", called
        if program is not None:
            print "    Aborting from file:", program
        else:
            print "    Aborting process"
    else:
        print "   ", explanation
        if called is not None:
            print "        Called from:", called
        if program is not None:
            print "    Aborting from file:", program
        else:
            print "    Aborting process"
    print "---------------------------------------------------"
    sys.exit()
#-------------------------------------------------------------------------------
