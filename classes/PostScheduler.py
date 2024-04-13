from apscheduler.schedulers.background import BackgroundScheduler
from classes.PostJob import PostJob
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
import datetime
import pytz
import os

class PostScheduler(BackgroundScheduler):
    

    MEDIA_FOLDER_PATH = 'static/media'
    def __init__(self, instagramClient, App):
        super().__init__()
        self.instagramClient = instagramClient 
        self.App = App

    def addPostJob(self, nameOfJob, dateToTrigger,timeToTrigger, files):
        # Saving Files
        directory = os.path.join(self.MEDIA_FOLDER_PATH, nameOfJob)
        os.makedirs(directory, exist_ok=True)

        # Save the file to the specified directory
        for file in files:
            file.save(os.path.join(directory, file.filename))

        # Making and Adding Job
        newPostJob =  PostJob(nameOfJob, timeToTrigger, self.instagramClient, self.App)
        
        start_date = datetime.datetime(year = dateToTrigger[0], 
                                       month = dateToTrigger[1], 
                                       day = dateToTrigger[2], 
                                       hour = timeToTrigger[0], 
                                       minute = timeToTrigger[1], 
                                       second = 0,)  


        intervalTrigger = IntervalTrigger(
            minutes=30,
            start_date=start_date ,
        )

        super().add_job(func = self.executePostJob, 
                        trigger = intervalTrigger, 
                        id = nameOfJob, 
                        args=[newPostJob]) 
        return 

    
    def executePostJob(self,postJob):
        postJobResult = postJob.maybeMakePost()  
        if postJobResult == PostJob.POST_JOB_SUCCESS:
            self.App.logger.debug('sucessfully made post')
        elif postJobResult == PostJob.POST_JOB_FAIL:
            self.App.logger.debug('job failed for some reason')
        else:
            super().remove_job(postJob.name)
            self.App.logger.debug('nothing else to post, lets remove the job')
        return
            







