import json
from flask import Flask, request, render_template
from Media import Media
from instagrapi import Client
import schedule
import time
import json
import os
from threading import Thread
import datetime


# ChatGpt Class to handle text generation and image generation?
# Instagram Class to handle posting, captions and sequence

# Server global variables
App = Flask(__name__)
MediaClient = Media("./media")
instagramClient = Client()
Secrets = json.load(open("secrets.json"))


@App.route("/")
def home():
    return render_template('welcome.html')

@App.route("/login")
def login():
    return render_template('login.html')
    # twofac = request.args.get("twofac")
    # if instagramClient.login(Secrets["username"], Secrets["password"], True, twofac):
    #     return "You have logged in!"
    # else:
    #     return "We couldn't log you in"


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
