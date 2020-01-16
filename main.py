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
    GPIO.setup(3,GPIO.OUT) # for camera IR LED
    GPIO.setup(4,GPIO.OUT) # for camera IR LED

    for pin in pin_input:
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    
    level_count = -1
    send_level = -1

    for i in range(len(pin_input)):
        if GPIO.input(pin_input[i]):
            level_count = i
            send_level = i




    print("Level: " + str(level))

    nbiot.send_data("sensor-V2", 0 if level_count==-1 else level[level_count], 100)
    
    GPIO.output(2, 1)
    GPIO.output(3, 1)
    GPIO.output(4, 1)
    cm.capturePhoto('sensor-V2.jpg')
    GPIO.output(2, 0)
    GPIO.output(3, 0)
    GPIO.output(4, 0)

    for i in range(10):
        print("<<< ./sensor-V2_%d.jpg >>>" % (i+1))
        nbiot.send_file("./sensor-V2_%d.jpg" % (i+1))
  
        level_count = -1

        for i in range(len(pin_input)):
            if GPIO.input(pin_input[i]):
                level_count = i
            
        if level_count != send_level:
            print("Current Level: " + str(level[level_count]))
            nbiot.send_data("sensor-V2", 0 if level_count==-1 else level[level_count], 100)
 
   
    # nbiot.send_file("./sensor-V2.jpg")
    # transfer_file_wifi()



def transfer_file_wifi(filePath='./front_door.jpg'):
    url = 'http://ccrc.twnict.com/function/upload_img.php'
    img = {'img':open(filePath, 'rb')}
    r = post(url,files=img)
    print("Post Response: %s" % str(r.content).replace("<br/>","\n"))



if __name__ == "__main__":
    main()
