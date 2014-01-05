import xmlrpclib
from time import time


class NoiseClient(object):

    def __init__(self, config):
        url = config.get('rrd', 'url')
        self.location = config.get('poi', 'location')
        self.proxy = xmlrpclib.ServerProxy(url)
        
    def update(self, leq):
            t0 = int((time()))
            self.proxy.update(self.location, t0, leq)
