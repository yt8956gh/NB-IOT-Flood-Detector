import RPi.GPIO as GPIO
import sys, sched, time, threading
from time import sleep
from camera import Camera
from nbiot import NBiot
from requests import post
from pyzbar.pyzbar import decode
from PIL import Image
from Crypto.Cipher import AES
from base64 import b64encode, b64decode
import cv2 as cv

key = b"Winnie the pooh "

pin_input = [17,27,22]
level = [20,40,60]
period = 15   # second

cm = Camera()
nbiot = NBiot()
AES_obj = AES.new(key, AES.MODE_ECB)


def main():

    global period

    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(2,GPIO.OUT) # for camera IR LED

        for pin in pin_input:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        
        print(sys.argv)

        if len(sys.argv)>1:

            if sys.argv[1]=="init":
                nbiot.nbiot_init()
            
            if sys.argv[-1].isdigit():
                period = int(sys.argv[-1])

        print("Period: %d" % period)

        sensor()

    finally:
            GPIO.cleanup()

def QR_AES(imgPath):


    img = cv.imread(imgPath, cv.CV_8UC1)

    th = cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY,11,2)

    qrArray = decode(img)

    cv.imwrite("./threshold.jpg", th)
    
    if len(qrArray) == 0:
        return -1

    heights = []


    for i, qr in enumerate(qrArray):
        try:
            print("[data-%d] " % i, AES_obj.decrypt(b64decode(qr.data)))
            height = int(AES_obj.decrypt(b64decode(qr.data)))
            heights.append(height)
        except ValueError:
            print("ValueError in \"%s\"" % qr.data)

    return min(heights)
    

def sensor():

    global level,cm,nbiot,pin_input

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(2,GPIO.OUT) # for camera IR LED
    GPIO.setup(3,GPIO.OUT) # for camera IR LED
    GPIO.setup(4,GPIO.OUT) # for camera IR LED

    imgPath = 'sensor-V2.jpg'
    QR_ImgPath = 'imgQR.jpg'

    threading.Timer(period, sensor).start()
    
    GPIO.output(2, 1)
    GPIO.output(3, 1)
    GPIO.output(4, 1)
    cm.capturePhoto(imgPath)
    GPIO.output(2, 0)
    GPIO.output(3, 0)
    GPIO.output(4, 0)

    level_count = QR_AES(QR_ImgPath)

    print("level_count: %d" % level_count)

    nbiot.send_data("sensor-V2", level[level_count], 100)

    #for i in range(10):
    #    print("<<< ./sensor-V2_%d.jpg >>>" % (i+1))
    #    nbiot.send_file("./sensor-V2_%d.jpg" % (i+1))

   
    # nbiot.send_file("./sensor-V2.jpg")
    # transfer_file_wifi()



def transfer_file_wifi(filePath='./front_door.jpg'):
    url = 'http://ccrc.twnict.com/function/upload_img.php'
    img = {'img':open(filePath, 'rb')}
    r = post(url,files=img)
    print("Post Response: %s" % str(r.content).replace("<br/>","\n"))



if __name__ == "__main__":
    main()
