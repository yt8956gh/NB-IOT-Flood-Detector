import RPi.GPIO as GPIO
import sys
from time import sleep
from camera import Camera
from nbiot import NBiot
from requests import post

pin_input = [17,27,22]


def main():

    GPIO.setmode(GPIO.BCM)

    for pin in pin_input:
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    cm = Camera()
    nbiot = NBiot()

    print(sys.argv)
    period = 900

    if len(sys.argv)>1:

        if sys.argv[1]=="init":
            nbiot.nbiot_init()
        
        if sys.argv[-1].isdigit():
            period = int(sys.argv[-1])

    print("Period: %d" % period)

    level = 0
    # count = 0

    while True:

        level=0    
        # count+=10

        for i in range(len(pin_input)):
            if GPIO.input(pin_input[i]):
                level = i+1
        print("Level: %d" % level)

        nbiot.send_data("front_door", level*20, 0)
        cm.capturePhoto()
        nbiot.send_file()
        # transfer_file_wifi()

        sleep(period)


def transfer_file_wifi(filePath='./front_door.jpg'):
    url = 'http://ccrc.twnict.com/function/upload_img.php'
    img = {'img':open(filePath, 'rb')}
    r = post(url,files=img)
    print("Post Response: %s" % str(r.content).replace("<br/>","\n"))



if __name__ == "__main__":
    main()
