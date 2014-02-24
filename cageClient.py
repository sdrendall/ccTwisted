# This is the cageClient module for the Gray Lab Conditioning Cage Installation
# Sam Rendall

# This Version uses Perspective Broker to handle RPC

from twisted.internet.protocol import Protocol
from twisted.application import service
from twisted.spread import pb
from twisted.python import log
import socket

# The Referenceable that each client passes to the Server
class CageClientRef(pb.Referenceable):

    def remote_getName(self):
        return socket.gethostname()

    def remote_success(self):
        print "It Worked!!!!\n Way to go team!!!"


class CageClientProtocol(pb.Broker):

    ref = CageClientRef()
    name = socket.gethostname()
    idNo = None
    serverRoot = None

    def connectionMade(self):
        print "Connection Made!"
        d = self.factory.getRootObject()
        d.addErrback(log.err, "Couldn't retrieve root object")
        d.addCallback(self.registerServer)

    def registerServer(self, rootRef):
        self.serverRoot = rootRef
        print "Sending Ref to Server"
        d = self.serverRoot.callRemote(registerPi, self.name, self.ref)
        d.addErrback(log.err, "Failed to send remote reference")

    def setIdNo(self, idNo):
        self.idNo = idNo


class CageClientFactory(pb.PBClientFactory):

    protocol = CageClientProtocol
    

def main():

    from twisted.internet import reactor
    factory = CageClientFactory()
    reactor.connectTCP('localhost', 10000, factory)
    
    reactor.run()

if __name__ == "__main__":
    main()