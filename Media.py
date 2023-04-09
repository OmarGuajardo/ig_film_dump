import os 
class Media:
    
    def __init__(self,path) -> None:
        self.media = os.listdir(path)
        pass

    def getMedia(self):
        return  self.media