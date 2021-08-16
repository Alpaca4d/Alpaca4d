from PIL import Image
import os
import sys

imagePath = sys.argv[1]
outputDir = os.path.dirname(imagePath)
fileName = os.path.join(outputDir, 'instagramPicture.png')

def crop_center(pil_img, crop_width, crop_height):
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))



def crop_max_square(pil_img):
    return crop_center(pil_img, min(pil_img.size), min(pil_img.size))



im = Image.open(imagePath)
im_new = crop_max_square(im)
im_new.save(fileName, quality=95)
print("I have finished")



