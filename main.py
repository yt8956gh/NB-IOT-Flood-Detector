import RPi.GPIO as GPIO
import sys, sched, time, threading
from time import sleep
from camera import Camera
from nbiot import NBiot
from requests import post

pin_input = [17,27,22]
level = [20,40,60]
period = 900   # second

cm = Camera()
nbiot = NBiot()


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




def sensor():

    global level,cm,nbiot,pin_input

    threading.Timer(period, sensor).start()

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(2,GPIO.OUT) # for camera IR LED

    for pin in pin_input:
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    
    for i in range(len(pin_input)):
        if GPIO.input(pin_input[i]):
            level = i

    print("Level: " + str(level))

    nbiot.send_data("test", level[i], 100)
    
    GPIO.output(2, 1)
    cm.capturePhoto()
    GPIO.output(2, 0)

    for i in range(10):
        print("<<< ./test_%d.jpg >>>" % (i+1))
        nbiot.send_file("./test_%d.jpg" % (i+1))
    
    # transfer_file_wifi()



def transfer_file_wifi(filePath='./front_door.jpg'):
    url = 'http://ccrc.twnict.com/function/upload_img.php'
    img = {'img':open(filePath, 'rb')}
    r = post(url,files=img)
    print("Post Response: %s" % str(r.content).replace("<br/>","\n"))



if __name__ == "__main__":
    main()
