import numpy as np


class Contract:
    def preprocess(self, data):
        temp = []
        for key in data.keys():
            temp.append(data[key])

        data = np.array(temp).reshape((1, 3))

    def postprocess(self, data):
        return str(data)
