from twisted.spread import pb

# The root remote object, the first remote object passed to a client
class ServerRoot(pb.Root):

    self.factory = None

    def remote_echo(self, line):
        print line

    def remote_registerPi(self, name, ref):
        ref.callRemote("setID", 1)


class myBroker(pb.Broker):
    pass


class myPBServerFactory(pb.PBServerFactory):

    def __init__(self, root, unsafeTracebacks=False, security=globalSecurity):
        pb.PBServerFactory.__init__(self, root, unsafeTracebacks, globalSecurity)
        self.root.factory = self

    protocol = myBroker


def main():
    from twisted.internet import reactor

    factory = myPBServerFactory(ServerRoot())
    reactor.listenTCP(8800, factory)

    reactor.run()


if __name__ == "__main__":
    main()