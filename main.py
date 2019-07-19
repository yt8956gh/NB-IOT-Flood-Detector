import RPi.GPIO as GPIO
import sys
from time import sleep
from camera import Camera
from nbiot import NBiot
pin_input = [17,27,22]


def main():

    GPIO.setmode(GPIO.BCM)

    for pin in pin_input:
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    cm = Camera()
    nbiot = NBiot()

    print(sys.argv)
    period = 900

    if len(sys.argv)==2:

        if sys.argv[1]=="init":
            nbiot.setting_init()
        elif sys.argv[1].isdigit():
            period = int(sys.argv[1])

    print("Period: %d" % period)

    level = 0
    count = 0

    while True:

        level=0    
        count+=10

        for i in range(len(pin_input)):
            if GPIO.input(pin_input[i]):
                level = i+1
        print("Count: %d" % count)

        nbiot.send_data("front_door", count, 0)
        cm.capturePhoto()

        sleep(period)


if __name__ == "__main__":
    main()
