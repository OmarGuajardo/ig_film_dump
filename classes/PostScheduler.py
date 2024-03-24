from apscheduler.schedulers.background import BackgroundScheduler
from classes.PostJob import PostJob
from apscheduler.triggers.cron import CronTrigger
from instagrapi import Client

class PostScheduler(BackgroundScheduler):
    
    def __init__(self, instagramClient):
        super().__init__()
        self.instagramClient = instagramClient 


    def addPostJob(self, nameOfJob, timeToTrigger, filePath):
        newPostJob =  PostJob(nameOfJob, timeToTrigger, filePath, self.instagramClient)
        cronTrigger = CronTrigger(
            year="*", month="*", day="*", hour = timeToTrigger[0], minute = timeToTrigger[1], second="*"
        )
        super().add_job(func = self.executePostJob, trigger = cronTrigger, id = nameOfJob, args=[newPostJob]) 
        return 


    def executePostJob(self,postJob):
        if postJob.maybeMakePost():
            print('sucessfully made post')
        else:
            print('nothing else to post')
        return
            







