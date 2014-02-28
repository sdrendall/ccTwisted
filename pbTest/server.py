#!/usr/bin/env python

# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

from twisted.spread import pb
from twisted.internet import reactor

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

  
    ## FROM THE TUTORIAL!!      
    def remote_takeTwo(self, two):
        print "received a Two called", two
        print "telling it to print(12)"
        two.callRemote("print", 12)


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

reactor.listenTCP(8800, RaspberryPiServerFactory(ServerRoot()))
reactor.run()