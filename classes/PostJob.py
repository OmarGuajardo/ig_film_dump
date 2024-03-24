
from instagrapi import Client

class PostJob:

    def __init__(self, name, timeToTrigger, filePath, instagramClient):
        self.name = name
        self.timeToTrigger = timeToTrigger
        self.filePath = filePath
        self.instagramClient = instagramClient
        self.nextPhotoToPublishIndex = 0
        self.photosToPublish = [1,2,3,4,5,6]
    
    def maybeMakePost(self):
        # I'll need to return a multi variable here for:
        # succeeded, 
        # failed bc of instagram 
        # or all photos publish, terminate this job
        if(self.nextPhotoToPublishIndex < len(self.photosToPublish)):
            print("posting ", self.photosToPublish[self.nextPhotoToPublishIndex])
            self.nextPhotoToPublishIndex += 1
            return True
        else:
            return False





