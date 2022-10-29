class Contract:
    def preprocess(self,data):
        temp = []
        for keys in data.keys():
            temp.append(data[keys])
            
        data = np.array(temp).reshape((1,1))
        return data

    def postprocess(self,data):
        return data[0]