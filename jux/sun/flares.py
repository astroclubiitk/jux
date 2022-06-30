from astropy.table import Table

from .helper.preprocessing import Preprocessing
from .helper.detection import DetectFlares
from .helper.modelling import ModelFlares

class Flares():
    """
    Class that accepts raw time and count rate.
    Returns a DataFrame containing the information regarding the flares found.
    """
    def __init__(self, time, rate):
        self.data = Preprocessing(time, rate)
        self.identified = DetectFlares(self.data.time, self.data.rate)
        self.model = ModelFlares(self.data.time, self.data.rate, self.identified.s5, self.identified.p5, self.identified.e1)

    def print_details(self):
        print("")
        print(self.model.data)

def read_lc_file(path_to_lc):
    table = Table.read(path_to_lc)
    time = table['TIME']
    rate = table['RATE']
    return time, rate