from flask import Flask, request, render_template, redirect
from instagrapi import Client
import logging
from logging import StreamHandler

from datetime import datetime
from classes.PostScheduler import PostScheduler

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger


# Server global variables
App = Flask(__name__)
instagramClient = Client()
logger = logging.getLogger()
postScheduler = PostScheduler(instagramClient)

# Configure the root logger to print to stdout
handler = StreamHandler()
handler.setLevel(logging.INFO)
App.logger.addHandler(handler)
App.logger.setLevel(logging.DEBUG)


@App.route("/")
def home():
    return render_template('welcome.html')

@App.route("/login", methods=['GET'])
def loginGET():
    return render_template('login.html')

@App.route("/logout")
def logout():
    try: 
        instagramClient.logout()
        return redirect('/')
    except Exception as e:
        App.logger.debug("Couldn't logout the user:  %s" % e)

@App.route("/dashboard", methods=['GET'])
def dashboardGET():
    try:
        instagramClient.get_timeline_feed()
        return render_template('dashboard.html', jobs=postScheduler.get_jobs())
    except Exception as e:
        return redirect('/')

# POST Access Points
@App.route("/login", methods=['POST'])
def loginPOST():
    username = request.form.get("username")
    password = request.form.get("password")
    twofac = request.form.get("twofac")

    session = instagramClient.load_settings("settings.json")

    # Logging through session
    App.logger.debug('about to check for session')
    if session:
        try:
            instagramClient.set_settings(session)
            instagramClient.login(username, password)
            App.logger.debug('checking trying to logging through session')

            try: 
                App.logger.debug('checking instagramclient')
                instagramClient.get_timeline_feed()
                logger.info("Session is VALID")
                return redirect('/dashboard')
            except Exception as e:
                App.logger.debug('Session is invalid, need to login via username and password')

        except Exception as e:
            App.logger.debug("Couldn't login user using session information", e)
            return render_template('welcome.html') 
    
    # Logging through username and password
    try:
        instagramClient.login(username, password, True, twofac)
        instagramClient.dump_settings("settings.json")
        return redirect('/dashboard')

    except Exception as e:
        logger.info("Couldn't login user using username & password: %s" % e)
        return render_template('welcome.html') 



@App.route('/remove_job/<job_to_be_removed>')
def removeJob(job_to_be_removed):
    postScheduler.remove_job(job_to_be_removed)
    return redirect('/dashboard') 

@App.route("/schedule_task", methods=["POST"])
def scheduleTask():
    if isUserLoggedIn() and request.method == 'POST':
        # getting data from request
        nameOfTask = request.form.get('name_of_task')
        timeOfFirstTrigger = request.form.get('time').split(':')
        files = request.files.getlist('file')

        instagramClient.photo_upload_to_story
        # creating job using my PostScheduler
        postScheduler.addPostJob(nameOfTask,timeOfFirstTrigger, files)

        return redirect('/dashboard')
    return redirect('/') 

def isUserLoggedIn():
    try: 
        instagramClient.get_timeline_feed()
        return True
    except Exception as e:
        App.logger.debug('use is not logged in')
        return False



if __name__ == "__main__":
    postScheduler.start()
    App.logger.debug("Scheduler Starting")
    App.run(host="0.0.0.0",port=1234, debug=True)
