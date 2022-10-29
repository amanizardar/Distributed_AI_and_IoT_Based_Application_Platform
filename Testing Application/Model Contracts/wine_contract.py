import numpy as np


class Contract:
    def preprocess(self, data):
        return data

    def postprocess(self, data):
        return str(data)
