import RPi.GPIO as GPIO
from time import sleep
pin_input = [17,27,22]


def main():

    GPIO.setmode(GPIO.BCM)

    for pin in pin_input:
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    while True:
        for i in range(len(pin_input)):
            print(GPIO.input(pin_input[i]))

        print()

        sleep(1)

if __name__ == "__main__":
    main()
