class Contract:
    def preprocess(self,data):
        img_vect = data["image"]
        return img_vect

    def postprocess(self,data):
        return data