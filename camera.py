# -- coding:utf-8 --

from picamera import PiCamera
from time import sleep
from PIL import Image
import os


class Camera:

    def __init__(self):

        self.cm = PiCamera()
        self.cm.resolution = (720,480)
        # self.cm.rotation = 180
        

    def capturePhoto(self, file_path = './test.jpg', quality=70):
     
        # take a picture
        self.cm.capture(file_path)
        sleep(1)

        print("┎------------Image------------")
        print("| save in " + file_path)

        im = Image.open(file_path)

        before_size = os.path.getsize(file_path)
        # print("| Before Size: ", before_size)

        im.save(file_path, optimize=True, quality=quality)

        after_size = os.path.getsize(file_path)
        print("| Size: ", after_size)

        print("| Compression ratio: %.2f" % (before_size/after_size))
        print("| Space saving: %.2f" % (1-(after_size/before_size)))
        self.cut_image(file_path)
        print("┖-----------------------------")
        im.close()

    def cut_image(self, file_path , cut_number = 10):
        img = Image.open(file_path)
        print("| Image shape: ", img.size)
        w, h = img.size
        x0, y0 = 0, 0
        x1, y1 = w, 0
        new_height = h/cut_number

        for i in range(cut_number):
            y0 = y1
            y1 = (i+1) * new_height
            # print((y0, x0, y1, x1))
            tmp = img.crop((x0, y0, x1, y1))
            new_filename = 'test_%d.jpg' % (i+1)
            tmp.save(new_filename)
            print("| Saving in : ", new_filename)


if __name__ == "__main__":

    import RPi.GPIO as GPIO
    
    try:
        c = Camera()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(2,GPIO.OUT) # for camera IR LED

        while True:
            str = input("Please key Enter ")
            if len(str) != 0 and str == "q":
                break

            GPIO.output(2,1) 
            sleep(1)
            c.capturePhoto()
            GPIO.output(2,0)
            sleep(1)

    finally:
        GPIO.cleanup()
