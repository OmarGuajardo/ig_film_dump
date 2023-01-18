from instagrapi import Client

class InstagramClient:
    
    def __init__(self,username,password,twofa) -> None:
        self.username = username
        self.password = password
        self.twofa = twofa
        
    def login(self):
        self.client = Client()
        self.client.login(self.username, self.password, True, self.twofa)

    def post(self, imagePath):
        self.client.photo_upload_to_story(imagePath)