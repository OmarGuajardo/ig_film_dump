# Insagram x ChatGPT x Film Photos

## Inspiration
I have way too many film photos that I have never posted, I want to show them off on Instagram but give them the *flir* they deserve, with some AI generated poetry

## MVP
- There should be a theme to each set
- There should be an AI Generated Image corresponding to the image set
- Post `n` pictures a day 
- Each picture will have a verse of the `n` verse poem associated with the set
- `n` is the max of amount of requests I can make per day for either the ChatGPT API or Instagrapi


## Technologies that I plan to use
- [instagrapi](https://github.com/adw0rd/instagrapi)
  - Using this instead of the Instagram Social Graph API because it's easier hahah
- [OpenAI](https://openai.com/api/)
  - Most popular AI at the moment, seems pretty powerful for text generation which is what I need right now
  
- [Flask](https://flask.palletsprojects.com/en/2.2.x/)
  - Using Flask because that's what I'm familiar with and it let's you create an API which will be useful if I decide to make a website out of this to track progress
  
