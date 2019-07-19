from picamera import PiCamera
from time import sleep
from datetime import datetime
from requests import post


class Camera:

    def __init__(self):

        self.cm = PiCamera()
        self.cm.resolution = (720,480)
        # self.cm.rotation = 180
        

    def capturePhoto(self, filename = 'front_door.jpg'):
     
        # take a picture
        self.cm.capture(filename)
        print("save in " + filename)
        sleep(3)
        
        # send image to server

        url = 'http://ccrc.twnict.com/function/upload_img.php'
        img = {'img':open('./front_door.jpg','rb')}
        r = post(url,files=img)

        print("Post Response: %s" % str(r.content).replace("<br/>","\n"))
        # sleep(900) # a image per half of hour

def main():
    capturePhoto()

if __name__ == "__main__":
    main()
