import sys
sys.path.insert(0, '/Users/saltQ/sbaProject')
from util.file_handler import FileReader
import pandas as pd
import numpy as np

class Model:    # entity + service

    def __init__(self):
        self.fileReader = FileReader()

    def new_model(self, payload):
        this = self.fileReader
        this.context = '/Users/saltQ/sbaProject/price_prediction/data/'
        this.fname = payload
        return pd.read_csv(this.context + this.fname)


if __name__ == '__main__':
    m = Model()
    dframe = m.new_model('price_data.csv')
    print(dframe.head())
    