from twisted.spread import pb
from pprint import pprint

class myClientBroker(pb.Broker):
    
    def connectionReady(self):
        pb.Broker.connectionReady(self)
        def1 = self.factory.getRootObject()
        def1.addCallback(got_root, "hello world")


class myPBClientFactory(pb.PBClientFactory):

    protocol = myClientBroker

    #def clientConnectionMade(self, broker):
    #    print "clientConnectionMade"
    


def main():
    from twisted.internet import reactor

    factory = myPBClientFactory()
    reactor.connectTCP("localhost", 8800, factory)

    reactor.run()

def got_root(root, msg):

    print "got root object!"
    root.callRemote("echo", msg)

if __name__ == "__main__":
    main()