from apscheduler.schedulers.background import BackgroundScheduler
from classes.PostJob import PostJob
from apscheduler.triggers.cron import CronTrigger
import os

class PostScheduler(BackgroundScheduler):
    
    def __init__(self, instagramClient):
        super().__init__()
        self.instagramClient = instagramClient 


    def addPostJob(self, nameOfJob, timeToTrigger, files):
        # Saving Files
        directory = os.path.join('media', nameOfJob)
        os.makedirs(directory, exist_ok=True)

        # Save the file to the specified directory
        for file in files:
            file.save(os.path.join(directory, file.filename))

        # Making and Adding Job
        newPostJob =  PostJob(nameOfJob, timeToTrigger, self.instagramClient)
        cronTrigger = CronTrigger(
            year="*", month="*", day="*", hour = timeToTrigger[0], minute = timeToTrigger[1], second="*"
        )
        super().add_job(func = self.executePostJob, trigger = cronTrigger, id = nameOfJob, args=[newPostJob]) 
        return 

    
    def executePostJob(self,postJob):
        if postJob.maybeMakePost():
            print('sucessfully made post')
        else:
            super().remove_job(postJob.name)
            print('nothing else to post, lets remove the job')
        return
            







