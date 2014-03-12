# These are the classes used to Serve commands to the Raspberry Pis in the
# Gray Lab conditioning cage project
# Sam Rendall

from twisted.spread import pb
from twisted.internet.defer import maybeDeferred

class RPiRoot(pb.Root):
"""
This is the first object that will be passed to the raspberry pis, as soon as they
establish a connection.  It's methods will be called to register the Pi with the server
and coordinate cross referencing of other remote objects (i.e camera, data structures)
"""
    
    self.core = None
     
    def remote_registerPi(self, identity, refs):
        """
        Each pi will call this method first to send identifiers and references to the server

        identity is a dict containing identifiers about the pi:
            hostname: <string> the pi's hostname
            ip: <str> the pi's ip address

        refs is a dict containing remoteReferences to the pi's Referencable objects
            experimentalProtocols:
            camera:

        """
        # Unpack Identifiers

        # Unpack References

        # Return id


class RPiServerBroker(pb.Broker):
    """
    I am the broker object used to handle connections and remote function calls with the
    Raspberry Pis.  At the moment, I don't do anything
    """
    pass


class RPiServerFactory(pb.PBServerFactory):
    """
    I am the server factory for establishing connections with new raspberry pis.

    Whenever a Raspberry Pi connects to me, I insantiate a RPiBroker to handle that connection.

    When the PBClientFactory on the pi's end calls getrootobject, I return a reference to an instance
    of RPiRoot.
    """

    protocol = RPiServerBroker
    controllers = None
