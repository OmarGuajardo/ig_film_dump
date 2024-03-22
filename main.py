import json
from flask import Flask, request, render_template
from Media import Media
from instagrapi import Client
from instagrapi.exceptions import LoginRequired
import logging
import schedule
import time
import json
import os
from threading import Thread
import datetime


# Server global variables
App = Flask(__name__)
MediaClient = Media("./media")
instagramClient = Client()
Secrets = json.load(open("secrets.json"))
logger = logging.getLogger()



@App.route("/")
def home():
    return render_template('welcome.html')

@App.route("/login", methods=['GET'])
def loginGET():
    return render_template('login.html')

@App.route("/dashboard", methods=['GET'])
def dashboardGET():
    try:
        instagramClient.get_timeline_feed()
    except LoginRequired:
        return 'youre not logged in get out of here'

# POST Access Points
@App.route("/login", methods=['POST'])
def loginPOST():
    username = request.form.get("username")
    password = request.form.get("password")
    twofac = request.form.get("twofac")

    session = instagramClient.load_settings("settings.json")

    # Logging through session
    if session:
        try:
            instagramClient.set_settings(session)
            instagramClient.login(username, password)

            try: 
                instagramClient.get_timeline_feed()
                logger.info("Session is VALID")
                return render_template('dashboard.html') 
            except Exception as e:
                logger.info("Session is invalid, need to login via username and password")
                return render_template('welcome.html') 

        except Exception as e:
            print("Couldn't login user using session information", e)
            return render_template('welcome.html') 
    
    # Logging through username and password
    try:
        instagramClient.login(username, password, True, twofac)
        instagramClient.dump_settings("settings.json")
        return render_template('dashboard.html') 

    except Exception as e:
        logger.info("Couldn't login user using username & password: %s" % e)
        return render_template('welcome.html') 


@App.route("/post")
def post():
    imgPath = request.args.get("img_path")
    # storyPosted = instagramClient.photo_upload_to_story("media_portrait/" + imgPath)
    storyPosted = instagramClient.photo_upload_to_story("cityexploring/" + imgPath)
    if storyPosted:
        return "We posted to your story!"
    else:
        return "We couldn't post your story :("


@App.route("/logout")
def logout():
    if instagramClient.logout():
        return "You're logged out!"
    else:
        return "We couldn't log you out!"


def job():
    # Do some work that only needs to happen once...
    print("=== JOB EXECUTED ===")
    # return schedule.CancelJob


@App.route("/jobs")
def jobs():
    return f"The scheduled job is {'running' if schedule.jobs else 'not running'}"


@App.route("/start")
def start():
    schedule.every().day.at("23:17").do(job)
    return "job starting"



@App.route("/media")
def media():
    mediaDir = request.args.get("dir")
    if mediaDir:
        return MediaClient.getMedia(mediaDir)
        pass
    else:
        return MediaClient.getMedia(None)


def runSchedule():
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    t = Thread(target=runSchedule)
    t.start()
    App.run(port=1234, debug=True)
