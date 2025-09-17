import requests
import pandas as pd
import numpy

class futbolExtract:
    def __init__(self, csv_path):
        self.csv = csv_path

    def queries(self):
        self.data = pd.read_csv(self.csv)
        self.data_info = self.data.info()

    def response(self):
        return self.data.head(15)