import numpy as np


class Contract:
    def preprocess(self, data):
        temp = []

        for key in data.keys():
            temp.append(data[key])

        data = np.array(temp).reshape((1, 1))

    def postprocess(self, data):
        class_type = "null"
        if data.text == "0.0":
            class_type = "Class 0"
        elif data.text == "1.0":
            class_type = "Class 1"
        elif data.text == "2.0":
            class_type = "Class 2"

        return data
