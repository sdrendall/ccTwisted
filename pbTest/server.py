#!/usr/bin/env python

# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

from twisted.spread import pb
from twisted.internet import reactor

class One(pb.Root):
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

    # Stores the the hostname of the connected client in self.clientName
    def setClientName(self, name):
        print "recieved:", result
        self.clientName = name
        print "Client No:", self.idNo, "Is named:", self.clientName


# Handles Connections from new Raspberry Pis
class RaspberryPiServerFactory(pb.PBServerFactory):

    protocol = pb.Broker
    currentProtocolId = 0

    def getNextProtocolId(self):
        self.currentProtocolId += 1
        return self.currentProtocolId

    def buildProtocol(self, addr):
        print "Building Protocol!"
        proto = pb.PBServerFactory.buildProtocol(self, addr)
        proto.idNo = self.getNextProtocolId()
        return proto


reactor.listenTCP(8800, RaspberryPiServerFactory(One()))
reactor.run()