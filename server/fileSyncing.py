import os, datetime, subprocess
from pprint import pprint

rootPath = os.path.expanduser("~/Desktop/testExperiments")

# Misc. Useful functions
def IdGenerator(myDict={}):
    """ Generator to generate ID numbers for timelapses,
    videos, mice... 
    """
    IdNo = 0
    while True:
        IdNo += 1
        if not str(IdNo) in myDict:
            yield str(IdNo)


def generateDateString():
    dt = datetime.datetime.now()
    dateString = "{:04}{:02}{:02}_{:02}{:02}".\
            format(dt.year, dt.month, dt.day, dt.hour, dt.minute)
    return dateString


def generateDateId(generator):
    return "{}_{}".format(generateDateString(), generator.next())


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


# Interface functions
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
            'path': expPath,
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

    def __init__(self, attrs):
        # This is the dict that will be saved as JSON.
        # Ideally the entire Experiment object (including subobjects)
        # Could be reconstructed from this info
        self.attributes = {
            'path': None,
            'id': None,
            'dateCreated': subprocess.check_output("date", shell=True),
            # References to each mouse's dict, timelapses and video dicts are here
            'mice': {}
        }

        self.mice = {}

        # Update attributes
        for key, val in attrs.iteritems():
            self.attributes[key] = val

        # Create generators for Ids
        self.getNextMouseId = IdGenerator(attributes['mice'])
        self.timelapseIdGenerator = IdGenerator()
        self.videoIdGenerator = IdGenerator()

# Mouse functions
    def createMouse(self, mouseId):
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
            'path': mousePath
        }

        # Create paths for timelapses, videos and logs
        for dirName, pathKey in [('timelapes', 'tlPath'), ('videos','vidPath'), ('logs','logPath')]:
            path = os.path.join(mousePath, dirName)
            ensureDirectory(path)
            attrs[pathKey] = path


        # Instantiate a mouse and reference its attributes dict
        mouse = Mouse(self, attrs)
        self.mice[mouseId] = mouse
        self.attributes['mice'][mouseId] = self.mice[mouseId].attributes

        return self.mice[mouseId]



    def ensureMouse(self, mouseId):
        if mouseId not in self.attributes['mice']:
            createMouse(mouseId)
        else:
            ensureDirectory(self.attributes['mice'][mouseId]['path'])


    def createMouseDirectory(self, mouseId):
        # Make sure the base directory is there
        ensureDirectory(self.attributes['path'])

        # Create mouse directory
        dirName = "mouse_{}".format(mouseId)
        mousePath = os.path.join(self.attributes['path'], dirName)
        if ensureDirectory(mousePath):
            return mousePath
        else:
            raise DirCreationFailed(mousePath)


class Mouse:
    """ This is the mouse class.  Instantiated for each mouse.
    Maintains timelapse, video and log paths for this mouse """

    def __init__(self, experiment, attrs):
        # Create a new attributes dict for each mouse
        self.attributes = {
            'timelapses': {},
            'videos': {},
            'logs': {}
            }
        # Reference the experiment 
        self.experiment = experiment
        # Add/update keys+values
        for key, val in attrs.iteritems():
            self.attributes[key] = val
        

    def createTimelapse(self):
        # Generate New Id, use date stamp
        tlId = generateDateId(self.experiment.timelapseIdGenerator)

        # Create Timelapse Path
        tlPath = self.createTimelapsePath(tlId)

        # Store timelapse attributes in a dict
        self.attributes['timelapses'][tlId] = {
        'path': tlPath,
        'id': tlId
        }

        # Return Timelapse attributes dict
        return self.attributes['timelapses'][tlId]


    def createTimelapsePath(self, tlId):
        dirName = "timelapse_{}".format(tlId)
        tlPath = os.path.join(self.attributes['tlPath'], dirName)
        if ensureDirectory(tlPath):
            return tlPath
        else:
            raise DirCreationFailed(tlPath)


    def createVideo(self):
        # Generate Id
        vidId = generateDateId(self.experiment.videoIdGenerator)
        # Store attributes in a dict
        self.attributes['videos'][vidId] = {
        'id': vidId,
        'path': self.attributes['vidPath']
        }
        # Return Dict
        return self.attributes['videos'][vidId]



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
    mice = {}
    for mId in range(1,5):
        mice[mId] = experiment.createMouse(mId)

    tlRefs =[]
    for mouseNo in [1, 3, 3, 2, 4, 1]:
        tlRefs.append(mice[mouseNo].createTimelapse())

    print "Timelapse References:"
    pprint(tlRefs)

    print "Experiment Attributes:"
    pprint(experiment.attributes)

if __name__ == "__main__":
    main()