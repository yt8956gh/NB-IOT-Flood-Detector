import RPi.GPIO as GPIO
from time import sleep

def main():

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(2,GPIO.OUT) # for camera IR LED
    GPIO.setup(3,GPIO.OUT) # for camera IR LED
    GPIO.setup(4,GPIO.OUT) # for camera IR LED
    

    while 1:

        GPIO.output(2, 1)
        GPIO.output(3, 1)
        GPIO.output(4, 1)

        sleep(1)

        GPIO.output(2, 0)
        GPIO.output(3, 0)
        GPIO.output(4, 0)

        sleep(1)


if __name__ == "__main__":
    main()
