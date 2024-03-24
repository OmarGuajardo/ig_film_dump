
import os
class PostJob:

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
        # I'll need to return a multi variable here for:
        # succeeded, 
        # failed bc of instagram 
        # or all photos publish, terminate this job
        if(self.nextPhotoToPublishIndex < len(self.photosToPublish)):
            
            # Here's how you actually post it with the instagramClient
            #     imgPath = request.args.get("img_path")
            # storyPosted = instagramClient.photo_upload_to_story("media_portrait/" + imgPath)
            print("posting ", self.photosToPublish[self.nextPhotoToPublishIndex])
            self.nextPhotoToPublishIndex += 1
            return True
        else:
            return False





