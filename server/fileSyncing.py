import os
from pprint import pprint

rootPath = os.path.expanduser("~/Desktop/testExperiments")


def IdGenerator(myDict):
    """ Generator to generate ID numbers for timelapses,
    videos, mice... 
    """
    IdNo = 0
    while True:
        IdNo += 1
        if not str(IdNo) in myDict:
            yield str(IdNo)

def ensureDirectory(path):
    """ Ensures that a directory exists at the given path.  If a directory 
    is not found, attempts to make one.  Returns a boolean stating whether or not
    a directory exists at the given path"""
    if path and os.path.isdir(path):
        return True
    else:
        try:
            os.mkdir(path)
            return True
        except OSError, e:
            print "Could not create directory %r" % path
            print e
            return False


def createExperiment(expId):
    dirName = "Experiment_{}".format(expId)
    expPath = os.path.join(rootPath, dirName) 
    # Check Path for existing experiments
    if os.path.isdir(expPath):
        raise ExperimentExists(expPath)
    else:
        # Attempt to create a new experiment directory
        if ensureDirectory(expPath):
            # If the directory can be created, instantiate a new experiment
            # and return it
            attrs = {
            'basePath': expPath,
            'id': expId
            }
            experiment = Experiment(attrs)
            return experiment
        else:
            raise DirCreationFailed(expPath)



class Experiment:
    """ The base directory for each experiment.
    handles ID generation and responsible for checking for the existence of mice 
    """

    # This is the dict that will be saved as JSON.
    # Ideally the entire Experiment object (including subobjects)
    # Could be reconstructed from this info
    attributes = {
        'basePath': None,
        'id': None,
        # References to the mice, timelapses and video dicts are here
        'mice': {},
        'timelapses': {},
        'videos': {}
    }

    mice = {}
    getNextMouseId = IdGenerator(attributes['mice'])
    getNextTimelapseId = IdGenerator(attributes['timelapses'])

    def __init__(self, attrs):
        for key, val in attrs.iteritems():
            self.attributes[key] = val


# Mouse functions
    def createMouse(self, mouseId=None):
        # Create a mouse id if none was specified
        # Not sure why I would want to do this
        if mouseId is None:
            mouseId = self.getNextMouseId()

        # Create a new mouse directory
        try:
            mousePath = self.createMouseDirectory(mouseId)
        except DirCreationFailed, e:
            print "Failed to create mouse Directory!"
            print e
            return None

        # Package initializing attributes
        attrs = {
            'id': mouseId,
            'basePath': mousePath
        }

        # Instantiate a mouse and reference its attributes dict
        self.mice[mouseId] = Mouse(attrs)
        self.attributes['mice'][mouseId] = self.mice[mouseId].attributes


    def ensureMouse(self, mouseId):
        if mouseId not in self.attributes['mice']:
            createMouse(mouseId)
        else:
            ensureDirectory(self.attributes['mice'][mouseId])


    def createMouseDirectory(self, mouseId):
        # Make sure the base directory is there
        ensureDirectory(self.attributes['basePath'])

        # Create mouse directory
        dirName = "mouse_{}".format(mouseId)
        mousePath = os.path.join(self.attributes['basePath'], dirName)
        if ensureDirectory(mousePath):
            return mousePath
        else:
            raise DirCreationFailed(mousePath)


# Media functions
    def createTimelapse(self, mouseId):
        """ This function is called whenever a timelapse should be created,
        A new ID is generated and passed to the mouse with mouseId
        returns a reference to the new timelapse's attributes dict
        """
        # Ensure mouse refs and path exist
        self.ensureMouse(mouseId)

        # Generate New Id
        tlId = getNextTimelapseId()

        # Reference Timelapse Attrs
        self.attributes['timelapses'][tlId] = self.mice[mouseId].createTimelapse(tlId)

        # Send back to reference to the timelapse attributes dict
        return self.attributes['timelapses'][tlId]


class Mouse:
    """ This is the mouse class.  Instantiated for each mouse.
    Maintains timelapse, video and log paths for this mouse """

    attributes = {
    'basePath': None,
    'id': None,
    'timelapses': None,
    'videos': None,
    'logs': None
    }

    def __init__(self, attrs):
        for key, val in attrs.iteritems():
            self.attributes[key] = val
        

    def createTimelapse(self, tlId):
        # Create Timelapse Path
        dirName = "timelapse_{}".format(tlId)
        tlPath = os.path.join(self.attributes['basePath'], dirName)
        ensureDirectory(tlPath)
        ## TODO: Do something if ensureDirectory fails

        # Store timelapse attributes in a dict
        self.attributes['timelapses'][tlId] = {
        'basePath': tlPath,
        'id': tlId,
        'mouse': self.attributes['id']
        }

        # Return Timelapse attributes dict
        return self.attributes['timelapses'][tlId]


## EXCEPTIONS!
class ExperimentExists(Exception):
    def __init__(self, path):
        self.path = path
    def __str__(self):
        errString = "Experiment already exists at {}".format(path)
        return repr(errString)

class DirCreationFailed(Exception):
    def __init__(self, path):
        self.path = path
    def __str__(self):
        errString = "Failed to create a directory at {}".format(path)
        return repr(errString)


# For Debugging
def main():
    experiment = createExperiment('testExp')
    for mId in range(1,5):
        experiment.createMouse(mId)

    tlRefs =[]
    for mouseNo in [1, 3, 3, 2, 4, 1]:
        tlRefs.append(experiment.createTimelapse(mouseNo))

    print "Timelapse References:"
    pprint(tlRefs)

    print "Experiment Attributes:"
    pprint(experiment.attributes)

if __name__ == "__main__":
    main()