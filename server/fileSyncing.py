import os

rootPath = "~/Desktop"


def IdGenerator(di):
    """ Generator to generate ID numbers for timelapses,
    videos, mice... 
    """
    mouseId = 0
    while True:
        mouseId += 1
        if not str(mouseId) in di:
            yield str(mouseId)


class Experiment():

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
    mouseIdGenerator = IdGenerator(contents['mice'])

    def createExperimentDirectory(self):
        dirName = "experiment_{}".format(self.expIdNo)
        basePath = os.path.join(rootPath, dirName)
        if os.path.isdir(basePath):
            # I should probably check to make sure this isn't 
            # a different, already existing experiment
            # Or warn user of a merge
            print "Directory Already Exists!"
        else:
            os.mkdir(basePath)
        return basePath


    def createMouse(self, mouseId=None):
        if mouseId is None:
            mouseId = self.getNextMouseId()
        # Make sure the base directory is there
        self.checkExperimentDirectory()
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
        self.basePath = createMouseDirectory
        self.id = mouseId
        self.experiment = experiment

    def createMouseDirectory(self):
        # Create mouse directory
        dirName = "mouse_{}".format(mouseId)
        mousePath = os.path.join(self.basePath, mousePath)
        if not os.path.isdir(mousePath):
            os.mkdir(mousePath)
            self.mousePaths[mouseId] = mousePath
        else:
            print "Directory corresponding to mouse {} already exists in current experiment!".format(mouseId)
        # Store id (probably unnecessary)
        if not mouseId in self.mouseIds:
            self.mouseIds.append(mouseId)


    def checkExperimentDirectory(self):


    def createNewTimelapsePath(self):

