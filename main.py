import json
from flask import Flask, request, render_template, redirect
from Media import Media
from instagrapi import Client
from instagrapi.exceptions import LoginRequired
from flask_apscheduler import APScheduler
import logging
import json
from threading import Thread
import datetime 


from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger


# Server global variables
App = Flask(__name__)
MediaClient = Media("./media")
instagramClient = Client()
Secrets = json.load(open("secrets.json"))
logger = logging.getLogger()
scheduler = BackgroundScheduler()


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
        logger.info("Couldn't logout the user:  %s" % e)

@App.route("/dashboard", methods=['GET'])
def dashboardGET():
    try:
        instagramClient.get_timeline_feed()
        return render_template('dashboard.html', jobs=scheduler.get_jobs())
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
    print('about to check for session')
    if session:
        try:
            instagramClient.set_settings(session)
            instagramClient.login(username, password)
            print('checking trying to logging through session')

            try: 
                print('checking instagramclient')
                instagramClient.get_timeline_feed()
                logger.info("Session is VALID")
                return redirect('/dashboard')
            except Exception as e:
                print('Session is invalid, need to login via username and password')

        except Exception as e:
            print("Couldn't login user using session information", e)
            return render_template('welcome.html') 
    
    # Logging through username and password
    try:
        instagramClient.login(username, password, True, twofac)
        instagramClient.dump_settings("settings.json")
        return redirect('/dashboard')

    except Exception as e:
        logger.info("Couldn't login user using username & password: %s" % e)
        return render_template('welcome.html') 


@App.route("/schedule_task", methods=["POST"])
def scheduleTask():
    nameOfTask = request.form.get('name_of_task')
    timeOfFirstTrigger = request.form.get('time').split(':')
    print(nameOfTask)
    print(timeOfFirstTrigger)
    trigger = CronTrigger(
        year="*", month="*", day="*", hour = timeOfFirstTrigger[0], minute = timeOfFirstTrigger[1], second="*"
    )
    scheduler.add_job(func = taskToRun, trigger = trigger, id = nameOfTask, args = [nameOfTask]) 
    return redirect('/dashboard')

@App.route("/tasks")
def getTasks():
    print(scheduler.get_jobs())
    return []

def taskToRun(nameOfTask):
    print(" ")
    print(" ")
    print("running " + nameOfTask)

if __name__ == "__main__":
    scheduler.start()
    App.run(port=1234, debug=True)
