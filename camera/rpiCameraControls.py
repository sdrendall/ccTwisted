# These are the camera commands to be used by the rpi clients in the Gray Lab conditioning cage system
# To control the onboard camera

import picamera
from twisted.spread import pb
from twisted.internet.task import LoopingCall
from twisted.internet import reactor


camera = picamera.PiCamera()

class CameraControls(pb.Referenceable):

    activeTimelapse = None
    activeTimelapseCanceller = None
    activeRecording = None
    activeRecordingCanceller = None

    defaultTimelapseParams = {
    'period': 10, # Frame capture period, in seconds
    'duration': None,  # Total timelapse duration, in seconds
    'width': 854,      # Frame width, in pixels
    'height': 480,      # Frame height, in pixels
    'output': 'filename' # output, default to a file
    }

    defaultVideoParams = {
    'duration': 10,    # Video duration, in seconds
    'width': 854       # Frame width, in pixels       
    'height': 480,     # Frame height, in pixels
    'output': 'filename', # Output, default to a file
    'format': 'mjpeg'
    }

    def remote_startTimelapse(self, params={}):
        # An active recording takes precedence over timelapse collection, postpone until video ends
        if self.activeRecording is not None:
            print "Camera in use for video recording!  Timelapse postponed!"

            return

        # If a timelapse is ongoing, stop it
        if self.activeTimelapse is not None:
            self.remote_stopTimelapse()

        # Load default params and update any user defined fields
        tlParams = updateParameters(self.defaultTimelapseParams, params)
        # Set some parameters
        camera.resolution = tlParams['width'], tlParams['height']

        # Start the timelapse
        self.activeTimelapse = LoopingCall(camera.capture, tlParams['output'])
        self.activeTimelapse.start(tlParams['period'])
        # Schedule an ending if a time limit is specified
        if tlParams['duration'] is not None:
            self.activeTimelapseCanceller = reactor.callLater(tlParams['duration'], self.remote_stopTimelapse)

    def remote_stopTimelapse(self):
        if self.activeTimelapse is not None:
            # Dereference the timelapse to indicate that it is over
            tl, self.activeTimelapse = self.activeTimelapse, None
            tl.stop()
            # Cancel the delayed call to stop the timelapse
            if self.activeTimelapseCanceller is not None:
                tlc, self.activeTimelapseCanceller = self.activeTimelapseCanceller, None
                tlc.cancel()
        else:
            print "No Active Timelapse!"

    def remote_recordVideo(self, params={}):
        if self.activeTimelapse is not None:
            self.remote_stopTimelapse()

        if self.activeRecording is not None:
            self.remote_stopVideo()

        # Load parameters, update user defined parameters
        vParams = updateParameters(self.defaultVideoParams, params)

        # Start the video
        camera.start_recording(vParams['output'], format=vParams['format'], resize=(vParams['width'], vParams['height']))
        self.activeRecording = True
        # Schedule the ending
        if vParams['duration'] is not None:
            self.activeRecordingCanceller = reactor.callLater(vParams['duration'], self.remote_stopVideo)





def updateParameters(baseParams, newParams={}):
    for key in newParams:
        if key in timelapseParams:
            baseParams[key] = newParams[key]
        else:
            print "Warning! Received invalid parameter name %r!" % key    
    return baseParams