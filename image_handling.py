from PIL import Image
import PIL.ExifTags

def main():
    size = 720,1080
    exifImageHeightKey = 'ExifImageHeight'
    exifImageWidthKey = 'ExifImageWidth'
    
    image = Image.open("./media/image_horizantal.jpg")
    exif = {
        PIL.ExifTags.TAGS[k]: v
        for k, v in image._getexif().items()
        if k in PIL.ExifTags.TAGS
    }

    print(exif[exifImageHeightKey])
    print(exif[exifImageWidthKey])
    if exif[exifImageHeightKey] < exif[exifImageWidthKey]: 
        print('rotating')
        image=image.rotate(-90, expand=True)

    image.save('./media/exif_new_image.jpg',dpi=(size))

if __name__ == "__main__":
    main()
