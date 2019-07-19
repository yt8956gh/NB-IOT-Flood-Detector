from picamera import PiCamera
from time import sleep
from datetime import datetime
from requests import post

def capturePhoto():
    cm = PiCamera()
    cm.resolution = (720,480)
    cm.rotation = 180
    

    while True:
        # filename = '/home/pi/Photo_'+datetime.now().strftime('%Y-%m-%d_%H-%M-%S')+'.jpg'
        filename = 'front_door.jpg'
        cm.capture(filename)
        #sleep(3)
        print("save in " + filename)
        sleep(1)
        url = 'http://ccrc.twnict.com/function/upload_img.php'
        img = {'img':open('./front_door.jpg','rb')}
        r = post(url,files=img)

        print("Post Response: %s" % r.content)
        sleep(900) # a image per half of hour

def main():
    capturePhoto()

if __name__ == "__main__":
    main()
