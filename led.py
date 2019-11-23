import RPi.GPIO as GPIO
from time import sleep

def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(2,GPIO.OUT) # for camera IR LED
    GPIO.setup(3,GPIO.OUT) # for camera IR LED

    GPIO.output(2, 1)
    GPIO.output(3, 1)

    for i in range(100):
        print(i)
        sleep(1)

    GPIO.output(2, 0)


if __name__ == "__main__":
    main()
