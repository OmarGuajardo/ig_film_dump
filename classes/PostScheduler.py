from apscheduler.schedulers.background import BackgroundScheduler
from classes.PostJob import PostJob
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime

class PostScheduler:
    jobs = {}
    
    def __init__(self):
        self.scheduler = BackgroundScheduler()

    def start(self):
        self.scheduler.start()

    def addPostJob(self, nameOfJob, timeToTrigger, filePath):
        newPostJob =  PostJob(nameOfJob, timeToTrigger, filePath)
        cronTrigger = CronTrigger(
            year="*", month="*", day="*", hour = timeToTrigger[0], minute = timeToTrigger[1], second="*"
        )
        self.scheduler.add_job(func = newPostJob.makePost, trigger = cronTrigger, id = nameOfJob) 
        return 


    def getJobs(self):
        copyOfJobs = self.scheduler.get_jobs()
        for job in copyOfJobs:
            time_ampm = job.next_run_time.strftime("%I:%M:%S %p")
            job.next_run_time = time_ampm   
            job.next_pic = "WIP"
        return copyOfJobs



