class NoiseError(Exception):
    message = "Noise Generic Error"

    def __str__(self):
        print  repr(self.message)

class NoiseConfError(NoiseError):
    message = "Noise Configuration Error"
