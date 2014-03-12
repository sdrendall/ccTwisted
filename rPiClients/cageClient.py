from twisted.spread import pb
import socket, clientErrbacks

class configCommands(pb.Referenceable):
    """
    I am a remotely referencable object whos methods can be called from the server
    """
    def __init__(self, broker):
        self.broker = broker


class RPiClientBroker(pb.Broker):

    serverRoot = None

    def __init__(self, isClient=1, security=globalSecurity):
        pb.Broker.__init__(self, isClient, security)
        self.name = factory.name

    # Fires once PB communication has been established
    def connectionReady(self):
        pb.Broker.connectionReady(self)
        # Get the root object from the server
        d = self.factory.getRootObject()
        d.addBoth(self.callback_registerRoot, clientErrbacks.getRootFailed)
        # Attempt to register with the server
        d.addCallback(self.callback_registerWithServer)
        d.addErrback(clientErrbacks.serverRegistrationFailed)

    def callback_registerRoot(self, root, *args):
        self.serverRoot = root

    def callback_registerWithServer(self, *args):
        d = self.serverRoot.callRemote("registerPi", self.name, self.commands)
        return d

class RPiClientFactory(pb.PBClientFactory):

    protocol = RPiClientBroker
    name = socket.gethostname()


    def __init__(self, unsafeTracebacks=False, security=globalSecurity):


