from picamera import PiCamera
from time import sleep
from PIL import Image, ImageDraw, ImageFont
import os


class Camera:

    def __init__(self):

        self.cm = PiCamera()
        self.cm.resolution = (720,480)
        # self.cm.rotation = 180
        

    def capturePhoto(self, filename = 'front_door.jpg', quality=70):
     
        # take a picture
        self.cm.capture(filename)
        sleep(1)
        print("save in " + filename)

        im = Image.open(filename)

        before_size = os.path.getsize(filename)
        print("Before Size: ", before_size)

        im.save(filename, optimize=True, quality=quality)

        after_size = os.path.getsize(filename)
        print("After Size: ", after_size)

        print("Compression ratio: %.2f" % (before_size/after_size))
        print("space saving: %.2f" % (1-(after_size/before_size)))

        im.close()
        

if __name__ == "__main__":
    c = Camera()

    while True:
        str = input("Please key Enter ")
        c.capturePhoto()

