from noisemapper.mapper import *

### Define the object mapper and start mapping


def main():
    mapper = NoiseMapper()
    mapper.calibrate()

if __name__ == "__main__":
    main()
