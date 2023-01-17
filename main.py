from instagrapi import Client
from PIL import Image
import PIL.ExifTags

def main():
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
    cl.login("username", "pwd", True, '111222')

    # Posting image to photo
    cl.photo_upload_to_story('./media/exif_new_image.jpg','test')


if __name__ == "__main__":
    main()
