import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageOps

import pyqrcode

TEMP_DIR_PATH = "tmp"


class FancyQR(object):
    def __init__(self, qr_url, version):
        self.size = None
        self.qr_url = qr_url
        self.version = version

    def generate_qr(self):
        url = pyqrcode.create(self.qr_url, version=self.version)
        url.png(f'{TEMP_DIR_PATH}/qr_url.png', scale=8)
        size = url.get_png_size(scale=8)
        self.size = size

    def create_smiley_dp(self):
        image = Image.new('I', (25, 25), 'white')
        draw = ImageDraw.Draw(image)
        draw.ellipse((0, 0, 25, 25), 'black')
        draw.ellipse((25 / 3.6, 20 / 3.6, 35 / 3.6, 30 / 3.6), 'white')
        draw.ellipse((50 / 3.6, 20 / 3.6, 60 / 3.6, 30 / 3.6), 'white')
        draw.arc((20 / 3.6, 40 / 3.6, 70 / 3.6, 70 / 3.6), 0, 180, fill='white')
        fp = open(f'{TEMP_DIR_PATH}/smiley.png', 'wb')
        image.save(fp)
        smiley_size = image.size
        return image, smiley_size

    def crop_to_circle(self, im):
        bigsize = (im.size[0] * 3, im.size[1] * 3)
        mask = Image.new('L', bigsize, 0)
        ImageDraw.Draw(mask).ellipse((0, 0) + bigsize, fill=255)
        mask = mask.resize(im.size, Image.Resampling.LANCZOS)
        mask = ImageChops.darker(mask, im.split()[-1])
        im.putalpha(mask)

    def flip_image_horizontally(self, image):
        im_flipped_right = image.transpose(method=Image.Transpose.FLIP_LEFT_RIGHT)
        fp = open(f"{TEMP_DIR_PATH}/smiley-horizontal-mirror.png", 'wb')
        im_flipped_right.save(fp)
        return im_flipped_right

    def flip_image_vertically(self, image):
        im_flipped_bottom = image.transpose(method=Image.Transpose.FLIP_TOP_BOTTOM)
        fp = open(f"{TEMP_DIR_PATH}/smiley-vertical-mirror.png", 'wb')
        im_flipped_bottom.save(fp)
        return im_flipped_bottom

    def modify_qr(self):
        # open existing qr code
        img1 = Image.open(f"{TEMP_DIR_PATH}/qr_url.png")
        image, smiley_size = self.create_smiley_dp()
        # open smiley detection pattern
        img2 = Image.open(f"{TEMP_DIR_PATH}/smiley.png")
        self.flip_image_horizontally(image)
        img3 = Image.open(f"{TEMP_DIR_PATH}/smiley-horizontal-mirror.png")
        self.flip_image_vertically(image)
        img4 = Image.open(f"{TEMP_DIR_PATH}/smiley-vertical-mirror.png")

        # resizing the images to be placed at detection patterns
        img2 = img2.resize(smiley_size)
        img3 = img3.resize(smiley_size)
        img4 = img4.resize(smiley_size)

        # pasting the modifed images at the detection patterns
        Image.Image.paste(img1, img2, (47, 47))
        Image.Image.paste(img1, img3, (self.size - 47 - smiley_size[0], 47))
        Image.Image.paste(img1, img4, (47, self.size - 47 - smiley_size[0]))

        # savinh the modified qr code
        fp = open('new-qr.png', 'wb')
        img1.save(fp)
        img_new = Image.open("new-qr.png").convert("L")

        img_new = ImageOps.colorize(img_new, black="black", white="white")

        return img_new

    def centre_image_resizing(self, img_new, centre_image, logo_image, resize_factor):
        centre_image_size = resize_factor
        logo_image_size = resize_factor

        my_img = Image.open(centre_image).convert('RGBA')
        logo_img = Image.open(logo_image).convert('RGBA')

        self.crop_to_circle(my_img)

        my_img = my_img.resize((resize_factor, resize_factor))
        logo_img = logo_img.resize((resize_factor, resize_factor))

        fp = open(f"{TEMP_DIR_PATH}/cropped.png", 'wb')
        my_img.save(fp)
        my_img = Image.open(f"{TEMP_DIR_PATH}/cropped.png")

        fp = open(f"{TEMP_DIR_PATH}/rippling_logo.png", 'wb')
        logo_img.save(fp)
        logo_img = Image.open(f"{TEMP_DIR_PATH}/rippling_logo.png")

        mask = Image.fromarray(np.uint8(255 * (np.random.rand(100, 100) > 0)))
        Image.Image.paste(img_new, logo_img,
                          (int(self.size / 2 - resize_factor / 2), int(self.size / 2 - 1.5 * resize_factor)), mask)
        Image.Image.paste(img_new, my_img,
                          (int(self.size / 2 - resize_factor / 2), int(self.size / 2 - resize_factor / 2)), mask)

        return centre_image_size


if __name__ == "__main__":
    text = input("Enter text to generate QR code: ")
    version = input("Enter desired version to generate QR code: ")
    version = int(version)
    logo_image = input("Enter file location of the logo image: ")
    centre_image = input("Enter file location of the image you want to place at centre of the url: ")
    my_qr = FancyQR(text, version)
    my_qr.generate_qr()
    img_new = my_qr.modify_qr()

    my_qr.centre_image_resizing(img_new, centre_image, logo_image, 100)

    img_new.show()
