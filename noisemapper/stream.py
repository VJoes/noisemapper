import pyaudio
from singleton import *


class NStream(object):
    __metaclass__ = Singleton
    def __init__(self, config):

        self.format = pyaudio.paInt16
        self.rate = config.getint('audio','rate')
        self.chunk = config.getint('audio','chunk')
        self.channels = config.getint('audio','channels')

        self.pa = pyaudio.PyAudio()
        self.stream = self.pa.open(
            format = self.format,
            channels = self.channels,
            rate = self.rate,
            input = True,
            output = False,
            start = False,
            frames_per_buffer = self.chunk)

    def read(self):
        if self.stream.is_stopped():
            self.stream.start_stream()
        return self.stream.read(self.chunk)
