import gc
import time
import ConfigParser
import logging.handlers

from numpy import *
from error import *
from client import *
from sampler import *
from nsobject import *

from Queue import  Queue
from threading import Event


class NoiseMapper(Thread):
    """
    Global stream var
    """
    OFFSET  = float(0)
    cfpath  = "/etc/noisemapper/nm.conf"

    def __init__(self, interactive=False):
        """
        Init connection to wordpress and ftp server, then set stream object
        """
        # Setup Audio stuff
        super(NoiseMapper, self).__init__()

        # Load data from config file
        self.readConfig()

        #Garbage collector
        if not gc.isenabled():
            gc.enable()
            print "Garbage Collector Activated !"
            gc.set_debug(gc.DEBUG_LEAK)

        # Logging
        handlerLog = logging.handlers.RotatingFileHandler(
            self.LOG_FILENAME, maxBytes=41943040, backupCount=500)

        handlerError = logging.handlers.RotatingFileHandler(
            self.ERRLOG_FILENAME, maxBytes=41943040, backupCount=500)

        # error log
        self.errlog = logging.getLogger('errLog')
        self.errlog.setLevel(logging.DEBUG)
        self.errlog.addHandler(handlerError)

        # data log
        self.log = logging.getLogger('Log')
        self.log.setLevel(logging.DEBUG)
        self.log.addHandler(handlerLog)

        # remote log
        self.remote = NoiseClient(self.config)

        # Setup queue consumer and producer

        self.sampler  = NSampler(self.config, self.log)

        self.log.debug("DEBUG: Start Recording %s @ %s ######" % (datetime.now(),  self.LOCATION ))
        
        if interactive:
            self.calibrate()


    def readConfig(self):
        try:
            self.config = ConfigParser.ConfigParser()
            self.config.read(self.cfpath)

            self.THREAD = self.config.getboolean('audio','threading')
            self.LOCATION = self.config.get('poi','location')
            self.LOG_FILENAME = '%s/noisemapper-%s.log' % (self.config.get('path','logpath'), self.config.get('poi','name'))
            self.ERRLOG_FILENAME = '%s/noisemapper-%s.err' % (self.config.get('path','logpath'), self.config.get('poi','name'))
        except NoiseError, e:
            return None

    
    def calibrate(self):
        """

        Calibrate the mic using a calibrator with a known value of power in db
        """
        text = """
           *** Stai per calibrare la scheda audio ***
           1) Imposta il volume d'ingresso  della scheda audio al 50%
           2) Accendi il calibratore a 1 khz
           3) Livello sonoro di calibrazione in db:"""

        answer = raw_input("Vuoi calibrare il microfono (y/N): ")

        if answer == 'y' or answer == 'Y':
            level = raw_input(text)

            if float(level):
                self.OFFSET = self.mono.rms(self.mono.read(False)[0], offset=False)[0] - float(level)

            self.config.set('audio', 'offset', self.OFFSET)

            try:
                with open(self.cfpath, 'wb') as configfile:
                    self.config.write(configfile)
                print "Saved in %s " % self.cfpath
            except e:
                pass

        else:
            self.OFFSET = self.config.getfloat('audio','offset')

        self.errlog.debug("DEBUG: time:%s\tcalibration offset:%s\tLoc:%s\n" % (datetime.now(), self.OFFSET, self.location ))
        self.sampler.OFFSET = self.OFFSET


    def run(self):
        self.sampler.start()

