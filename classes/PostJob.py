
class PostJob:
    timesRan = 0

    def __init__(self, name, timeToTrigger, filePath,):
        self.name = name
        self.timeToTrigger = timeToTrigger
        self.filePath = filePath
    
    def makePost(self):
        print("making a post for " + self.name)
        print("times ran ", self.timesRan)
        self.timesRan += 1

    def getReadableNextExecutionTime(self):
        return 0


