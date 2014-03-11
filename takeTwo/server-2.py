from twisted.spread import pb

class ServerRoot(pb.Root):

    def remote_echo(self, line):
        print line


class myBroker(pb.Broker):
    pass

class myPBServerFactory(pb.PBServerFactory):

    protocol = myBroker


def main():
    from twisted.internet import reactor

    factory = myPBServerFactory(ServerRoot())
    reactor.listenTCP(8800, factory)

    reactor.run()


if __name__ == "__main__":
    main()