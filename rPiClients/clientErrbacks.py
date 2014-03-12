# These are Errbacks to be called by RPiClients when things dont work out

def getRootFailed(err):
    print "Failed to get Root Object!"
    err.printTraceback()

def serverRegistrationFailed(err):
    print "Failed to register with server!"
    err.printTraceback()