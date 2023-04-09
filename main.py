import json
from flask import Flask, request
from Media import Media
from instagrapi import Client
import json
import os

# ChatGpt Class to handle text generation and image generation?
# Instagram Class to handle posting, captions and sequence

# Server global variables
app = Flask(__name__)
media = Media("./media")
instagramClient = Client()
secrets = json.load(open("secrets.json"))


@app.route("/login")
def login():
    twofac = request.args.get("twofac")
    if instagramClient.login(secrets["username"], secrets["password"], True, twofac):
        return "You have logged in!"
    else:
        return "We couldn't log you in"


@app.route("/post")
def post():
    imgPath = request.args.get("img_path")
    storyPosted = instagramClient.photo_upload_to_story("media_portrait/" + imgPath)
    if storyPosted:
        return "We posted to your story!"
    else:
        return "We couldn't post your story :("


@app.route("/logout")
def logout():
    if instagramClient.logout():
        return "You're logged out!"
    else:
        return "We couldn't log you out!"


@app.route("/")
def home():
    return media.getMedia()


if __name__ == "__main__":
    app.run(port=1234, debug=True)
