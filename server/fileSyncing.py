import os

rootPath = "~/Desktop"


def IdGenerator(id):
    """ Generator to generate ID numbers for timelapses,
    videos, mice... 
    """
    mouseId = 0
    while True:
        mouseId += 1
        if not str(mouseId) in di:
            yield str(mouseId)

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
            except OSError:
                print "Could not create directory %r" % path
                return False



class Experiment:

    # This is the dict that will be saved as JSON.
    # Ideally the entire Experiment object (including subobjects)
    # Could be reconstructed from this info
    contents = {
    'basePath': None,
    'expIdNo': 1,
    'expIdStr': None,
    'mice': {}
    }

    mice = {}
    getNextMouseId = IdGenerator(contents['mice'])

    def setBaseDirectory(self, path=self.generateExperimentDirectoryPath()):
        if ensureDirectory(path):
            self.contents['basePath'] = path
        else:
            print "Experiment directory not set!"

    def generateExperimentDirectoryPath(self):
        """ Returns a standardized path and directory name for an experiment directory
        experiment directory is named using the expIdNo"""

        dirName = "experiment_{}".format(self.contents["expIdNo"])
        basePath = os.path.join(rootPath, dirName)
        return basePath

    def createMouse(self, mouseId=None):
        if mouseId is None:
            mouseId = self.getNextMouseId()
        # Make sure the base directory is there
        ensureDirectory(self.contents['basePath'])
        self.mice[mouseId] = Mouse(self, mouseId)
        self.contents['mice'][mouseId] = self.mice[mouseId].createMouseDirectory()



class Mouse:

    contents = {
    'basePath': None,
    'id': None,
    'timelapses': None,
    'videos': None,
    'logs': None
    }

    def __init__(self, experiment, mouseId):
        ensureMouseDirectory()
        self.id = mouseId
        self.experiment = experiment

    def ensureMouseDirectory()

    def createMouseDirectory(self):
        # Create mouse directory
        dirName = "mouse_{}".format(mouseId)
        mousePath = os.path.join(self.basePath, mousePath)
        if not os.path.isdir(mousePath):
            os.mkdir(mousePath)
            self.contents['basePath'] = mousePath
        else:
            print "Directory corresponding to mouse {} already exists in current experiment!".format(mouseId)

    def createNewTimelapse

class Timelapse:

class Video:

class Log
