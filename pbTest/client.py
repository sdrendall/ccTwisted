#!/usr/bin/env python

# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

from twisted.spread import pb
from twisted.internet import reactor
import socket

class Two(pb.Referenceable):

    def remote_print(self, arg):
        print "Two.print() called with", arg


class CageClientProtocol(pb.Broker):

    ref = CageClientRef()
    name = socket.gethostname()
    idNo = None
    serverRoot = None

   # def connectionReady(self):
   #     print "Connection Ready!"
    #    d = self.factory.getRootObject()
    #    d.addErrback(log.err, "Couldn't retrieve root object")
    #    d.addCallback(self.registerServer)

  #  def registerServer(self, rootRef):
  #      self.serverRoot = rootRef
  #      print "Sending Ref to Server"
  #      d = self.serverRoot.callRemote(registerPi, self.name, self.ref)
  #      d.addErrback(log.err, "Failed to send remote reference")

#    def setIdNo(self, idNo):
#        self.idNo = idNo


class CageClientFactory(pb.PBClientFactory):

    protocol = CageClientProtocol


def main():
    two = Two()
    factory = CageClientFactory()
    reactor.connectTCP("localhost", 10000, factory)
    def1 = factory.getRootObject()
    def1.addCallback(got_obj, two) # hands our 'two' to the callback
    reactor.run()

def got_obj(obj, two):
    print "got One:", obj
    print "giving it our two"
    obj.callRemote("takeTwo", two)

main()