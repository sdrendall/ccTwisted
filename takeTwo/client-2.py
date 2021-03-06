from twisted.spread import pb
from pprint import pprint
import socket


# A test Referencable
# In the real thing this will be a set of commands
# for camera management or data management
class myCommands(pb.Referenceable):

    def __init__(self, broker):
        self.broker = broker

    def remote_setID(self, idNo):
        self.broker.idNo = idNo
        print "Registered with ID number: %d" % idNo


class myClientBroker(pb.Broker):

    serverRoot = None
    idNo = None
    
    def connectionReady(self):
        
        def getRootFailed(err):
            err.printTraceback()

        def serverRegistrationFailed(err):
            err.printTraceback()

        # Perform the necessary built-in initializations
        pb.Broker.connectionReady(self)
        # Get serverRoot from the server and register
        d = self.factory.getRootObject()
        d.addCallbacks(got_root, getRootFailed)
        d.addCallback(self.registerRoot)
        d.addErrback(serverRegistrationFailed)


    def registerRoot(self, obj, *args):
        self.serverRoot = obj


class myPBClientFactory(pb.PBClientFactory):

    protocol = myClientBroker

    def buildProtocol(self, addr):
        proto = pb.PBClientFactory.buildProtocol(self, addr)
        proto.name = socket.gethostname()
        proto.commands = myCommands(proto)
        return proto


def main():
    from twisted.internet import reactor

    factory = myPBClientFactory()
    reactor.connectTCP("localhost", 8800, factory)

    reactor.run()

def got_root(root):
    print "got root object!"
    dic = {'one': 1, 'two': 2, 'str': 'hello world', 'd': {'fee': 'fum', 'cock': 'balls'}}
    root.callRemote("echo", dic)
    return root

if __name__ == "__main__":
    main()