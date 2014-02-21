# This is the ccServer module for the Gray Lab Conditioning Cage Installation
# Sam Rendall

from twisted.internet.protocol import ServerFactory, Protocol
from twisted.application import service
from twisted.protocols import amp
from twisted.python import log
from cageClient import GetName


# Is instantiated/run for each connected Raspberry Pi
# Using AMP now instead of LineReceiver
class RaspberryPiConnectionProtocol(amp.AMP):

    name = ""
    idNo = None

    #ip = None
    #role = ""    

    def connectionMade(self):
        self.sendCommand(GetName)

    def sendCommand(self, command):
        response = self.callRemote(command)
        print response

# Handles Connections from new Raspberry Pis
class RaspberryPiServerFactory(ServerFactory):

    protocol = RaspberryPiConnectionProtocol
    currentProtocolId = 0

    def getNextProtocolId(self):
        self.currentProtocolId += 1
        return self.currentProtocolId

    def buildProtocol(self, addr):
        proto = ServerFactory.buildProtocol(self, addr)
        proto.idNo = self.getNextProtocolId()
        return proto

# Handles connection and I/O with user 
class UserFactory(ServerFactory):
    protocol = Protocol


def main():
    from twisted.internet import reactor

    factory = RaspberryPiServerFactory()

    reactor.listenTCP(10000, factory, interface='localhost')

    print "Listening on 127.0.0.1:10000 ..."

    reactor.run()

if __name__ == "__main__":
    main()