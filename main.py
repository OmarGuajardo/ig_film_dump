from instagrapi import Client
from PIL import Image
import PIL.ExifTags
import json

def main():
    # Loading Secretes
    secrets = json.load(open('./secrets.json'))

    ## Image Manipulation
    size = 720,1080
    imagePath = './media/000603080010.jpg'
    exifImageHeightKey = 'ExifImageHeight'
    exifImageWidthKey = 'ExifImageWidth'
    
    image = Image.open(imagePath)
    exif = {
        PIL.ExifTags.TAGS[k]: v
        for k, v in image._getexif().items()
        if k in PIL.ExifTags.TAGS
    }

    if exif[exifImageHeightKey] < exif[exifImageWidthKey]: 
        print('rotating')
        image=image.rotate(-90, expand=True)

    image.save('./media/exif_new_image.jpg',dpi=(size))

    # Defining Client
    cl = Client()

    # Logging In 
    cl.login(secrets['username'],secrets['password'], True, secrets['2fa'])

    # Posting image to photo
    cl.photo_upload_to_story('./media/exif_new_image.jpg','test')


if __name__ == "__main__":
    main()
