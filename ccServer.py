# This is the ccServer module for the Gray Lab Conditioning Cage Installation
# Sam Rendall

# This Version uses Perspective Broker to handle RPC

from twisted.internet.protocol import ServerFactory, Protocol
from twisted.application import service
from twisted.protocols import amp
from twisted.python import log
from twisted.spread import pb


# This is the root object for the server.
# The client gets this as soon as it connects and uses it
# To run some registration commands
class ServerRoot(pb.Root):

    clientNames = []
    clientRefs = {}

    def remote_success(self):
        print "Success!"

    def remote_registerPi(self, name, ref):
        self.clientNames.append(name)
        self.clientRefs[name] = ref

        # Some stuff to see if it worked. For Debugging
        print self.clientNames
        self.clientRefs[name].callRemote(success)


# Is instantiated/run for each connected Raspberry Pi
# Using Perspective Broker (PB) now instead of LineReceiver
class RaspberryPiConnectionProtocol(pb.Broker):

    clientName = None
    idNo = None

    #ip = None
    #role = ""    
    def connectionMade(self):
        print "Connection Made!"

    # Stores the the hostname of the connected client in self.clientName
    def setClientName(self, name):
        print "recieved:", result
        self.clientName = name
        print "Client No:", self.idNo, "Is named:", self.clientName


# Handles Connections from new Raspberry Pis
class RaspberryPiServerFactory(pb.PBServerFactory):

    protocol = RaspberryPiConnectionProtocol
    currentProtocolId = 0

    def getNextProtocolId(self):
        self.currentProtocolId += 1
        return self.currentProtocolId

    def buildProtocol(self, addr):
        print "Building Protocol!"
        proto = pb.PBServerFactory.buildProtocol(self, addr)
        proto.idNo = self.getNextProtocolId()
        return proto


def main():
    from twisted.internet import reactor

    serverRoot = ServerRoot()
    factory = RaspberryPiServerFactory(serverRoot)

    reactor.listenTCP(10000, factory, interface='localhost')

    print "Listening on 127.0.0.1:10000 ..."

    reactor.run()

if __name__ == "__main__":
    main()