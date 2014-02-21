# This is the cageClient module for the Gray Lab Conditioning Cage Installation
# Sam Rendall

from twisted.internet.protocol import ClientFactory
from twisted.application import service
from twisted.protocols import amp
from twisted.python import log
import socket

# Commands -- These can be called remotely
class GetName(amp.Command):

#    arguments = [('arg1', amp.String())]
    response = [('name', amp.String())]


class CageClientProtocol(amp.AMP):

    def madeConnection(self):
        print "Connection Made!"

    def getName(self):
        return socket.gethostname()

    GetName.responder(getName)

class CageClientFactory(ClientFactory):

    protocol = CageClientProtocol


def connectToServer(host, port):

    from twisted.internet import reactor
    factory = CageClientFactory()
    reactor.connectTCP(host, port, factory)


def main():
    from twisted.internet import reactor

    connectToServer("localhost", 10000)
    reactor.run()

if __name__ == "__main__":
    main()