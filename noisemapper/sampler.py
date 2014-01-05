from threading import Thread
from datetime import datetime
from numpy import *
from stream import *
import pyaudio
import sys
import gc


class NSampler(Thread):

    def __init__(self, config, log):

        super(NSampler, self).__init__()

        self.log = log
        self.config = config
        self.tags = {}
        for tag in self.config.options('tags'):
            self.tags[tag] = self.config.get('tags',tag)
        self.stream = NStream(config)

        self.OFFSET = self.config.getfloat('audio','offset')
        self.TBR = self.config.getint('audio','timebaseRec')
        self.TBP = self.config.getint('audio','timebasePost')




    def rms(self, vect, offset=True):
        gc.collect()
        dco = mean(vect)
        result  = sum(power(subtract(vect, dco),2))        
        if result/len(vect) == 0:
            return (25)        
        if not offset:
            return(((10*math.log(result/len(vect),10)), dco))
        return(((10*math.log(result/len(vect),10))-self.OFFSET, dco))


    def logMean(self, vect):
        return round(10*math.log(mean(pow(10,vect * 0.1)),10),1)


    def read(self):

        """
        Start stream and continuously read one second of data  from it,
        returns array() buffer of float64 values
        """

        count = 0
        t0 = datetime.now()
        vect = array([], float64)

        while count < self.stream.rate:
            chunk = ""

            try:
                chunk = self.stream.read()
            except IOError,e:
                if e[1] == pyaudio.paInputOverflowed:
                    print e

            if chunk:
                try:
                    vect = append(vect, array(frombuffer(chunk, int16), float64))
                except MemoryError, e:
                    print "Read Error: ", e.message
                    return array([], float64)
                
            count += self.stream.chunk

        del gc.garbage[:]
        return (vect, t0)


    def run(self):
        tags = ""
        for t in self.tags.items():
            tags += "%s=%s " % (t[0],t[1])

        longleq = array([],float64) 

        while True:
            vect, t0 = self.read()
            leq, dco = self.rms(vect)
            del vect

            if len(longleq) == self.TBP/self.TBR:
                # Media logaritmica su "timebasePost/timebaseRec" minuti
                value = self.logMean(longleq)
                del longleq
                longleq = array([],float64)

            self.log.debug("%s,%s,%s" % (t0.strftime("%Y%m%d"), t0.strftime("%H%M%S"), round(leq,1)))

            longleq = append(longleq, leq)            
            print "noise %s %s %s" % (t0.strftime('%s'), round(leq,1), tags)
            sys.stdout.flush()




