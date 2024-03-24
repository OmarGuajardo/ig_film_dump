import os
class PostJob:

    POST_JOB_SUCCESS = 0
    POST_JOB_FAIL = 1
    POST_JOB_FINISHED = 2

    def __init__(self, name, timeToTrigger, instagramClient):
        self.name = name
        self.timeToTrigger = timeToTrigger
        self.instagramClient = instagramClient
        self.nextPhotoToPublishIndex = 0
        self.photosToPublish = self.extractFilePaths() 

    
    def extractFilePaths(self):
        file_paths = []
        directory = os.path.join('media', self.name)
        # Iterate through the directory
        for file_name in os.listdir(directory):
            # Construct the full file path
            file_path = os.path.join(directory, file_name)
            # Check if it's a file (not a directory)
            if os.path.isfile(file_path):
                # Add the file path to the list
                file_paths.append(file_path)
        print(file_paths)
        return file_paths

    def maybeMakePost(self):
        if(self.nextPhotoToPublishIndex < len(self.photosToPublish)):
            # Here's how you actually post it with the instagramClient
            try:
                nextPhotoToPublishImagePath = self.photosToPublish[self.nextPhotoToPublishIndex]
                storyPosted = self.instagramClient.photo_upload_to_story(nextPhotoToPublishImagePath,extra_data = {'is_paid_partnership' : 0})
                print("posting ", self.photosToPublish[self.nextPhotoToPublishIndex])
                self.nextPhotoToPublishIndex += 1
                return self.POST_JOB_SUCCESS
            except Exception as e:
                print("post job failed because of ", e)
                return self.POST_JOB_FAIL
        else:
            return self.POST_JOB_FINISHED





