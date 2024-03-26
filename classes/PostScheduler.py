from apscheduler.schedulers.background import BackgroundScheduler
from classes.PostJob import PostJob
from apscheduler.triggers.cron import CronTrigger
import os

class PostScheduler(BackgroundScheduler):
    

    MEDIA_FOLDER_PATH = 'static/media'
    def __init__(self, instagramClient):
        super().__init__()
        self.instagramClient = instagramClient 

    def addPostJob(self, nameOfJob, timeToTrigger, files):
        # Saving Files
        directory = os.path.join(self.MEDIA_FOLDER_PATH, nameOfJob)
        os.makedirs(directory, exist_ok=True)

        # Save the file to the specified directory
        for file in files:
            file.save(os.path.join(directory, file.filename))

        # Making and Adding Job
        newPostJob =  PostJob(nameOfJob, timeToTrigger, self.instagramClient)
        cronTrigger = CronTrigger(
            year="*", month="*", day="*", hour = "*", minute = timeToTrigger[1], second="0"
        )
        super().add_job(func = self.executePostJob, trigger = cronTrigger, id = nameOfJob, args=[newPostJob]) 
        return 

    
    def executePostJob(self,postJob):
        postJobResult = postJob.maybeMakePost()  
        if postJobResult == PostJob.POST_JOB_SUCCESS:
            print('sucessfully made post')
        elif postJobResult == PostJob.POST_JOB_FAIL:
            print('job failed for some reason')
        else:
            super().remove_job(postJob.name)
            print('nothing else to post, lets remove the job')
        return
            







