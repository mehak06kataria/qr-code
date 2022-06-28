from PIL import Image, ImageOps, ImageChops
from PIL import ImageDraw

import numpy as np


def crop_to_circle(im):
    bigsize = (im.size[0] * 3, im.size[1] * 3)
    mask = Image.new('L', bigsize, 0)
    ImageDraw.Draw(mask).ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(im.size, Image.Resampling.LANCZOS)
    mask = ImageChops.darker(mask, im.split()[-1])
    im.putalpha(mask)

#smiley detection pattern
image = Image.new('I',(25,25),'white')
draw = ImageDraw.Draw(image)
draw.ellipse((0,0,25,25),'black')
draw.ellipse((25/3.6,20/3.6,35/3.6,30/3.6),'white')
draw.ellipse((50/3.6,20/3.6,60/3.6,30/3.6),'white')
draw.arc((20/3.6,40/3.6,70/3.6,70/3.6), 0, 180, fill = 'white')
fp = open('smiley.png','wb')
image.save(fp)

#image = Image.open("Downloads/rippling_dp.png")

im_flipped_right = image.transpose(method=Image.Transpose.FLIP_LEFT_RIGHT)
fp = open('smiley-horizontal-mirror.png','wb')
im_flipped_right.save(fp)

im_flipped_bottom = image.transpose(method=Image.Transpose.FLIP_TOP_BOTTOM)
fp = open('smiley-vertical-mirror.png','wb')
im_flipped_bottom.save(fp)

qr_url = input("Enter url to generate QR code : ")

import pyqrcode
url = pyqrcode.create(qr_url, version = 15)
url.png('qr_url.png', scale=8)

#print(url.get_png_size())

img1 = Image.open("qr_url.png")
img2 = Image.open("smiley.png")
#img2 = Image.open("Downloads/rippling_dp.png")
img3 = Image.open("smiley-horizontal-mirror.png")
img4 = Image.open("smiley-vertical-mirror.png")

print(img1.size)

img2 = img2.resize((25,25))
img3 = img3.resize((25,25))
img4 = img4.resize((25,25))
Image.Image.paste(img1, img2, (47,47))
Image.Image.paste(img1, img3, (608,47))
Image.Image.paste(img1, img4, (47,608))

fp = open('new-qr.png','wb')
img1.save(fp)
img_new = Image.open("new-qr.png").convert("L")

img_new = ImageOps.colorize(img_new, black="black", white="white")

#my_img = Image.open("Downloads/Snapchat-1826503189 (1).jpg")
#fp = open('my-img.jpg','wb')
#my_img.save(fp)

centre_image = input("Enter location of the image you want to place at centre of the url : ")

#my_img = Image.open("Downloads/Snapchat-1826503189 (1).jpg").convert('RGBA')
my_img = Image.open(centre_image).convert('RGBA')
#my_img.show()
#my_img = my_img.resize((50,50))
crop_to_circle(my_img)
my_img = my_img.resize((100,100))
fp = open('cropped.png','wb')
my_img.save(fp)
my_img = Image.open('cropped.png')

#my_img.show()

mask = Image.fromarray(np.uint8(255*(np.random.rand(100, 100) > 0)))
Image.Image.paste(img_new, my_img,(280,280),mask)

#print(img_new.size)

img_new.show()

