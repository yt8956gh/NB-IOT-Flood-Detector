import RPi.GPIO as GPIO
import sys
from time import sleep
import nbiot
pin_input = [17,27,22]


def main():

    GPIO.setmode(GPIO.BCM)

    for pin in pin_input:
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    print(sys.argv)

    nbiot.serial_connect()

    if len(sys.argv)>1 and sys.argv[1]=="init":
       nbiot.serial_init()

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

        sleep(5)


if __name__ == "__main__":
    main()
