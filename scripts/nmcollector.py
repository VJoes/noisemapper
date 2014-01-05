#!/usr/bin/python
from noisemapper.mapper import *
#from collectors.lib import utils

### Define the object mapper and start mapping


def main():
#    utils.drop_privileges()
    mapper = NoiseMapper()
    mapper.run()

if __name__ == "__main__":
    main()
