import RPi.GPIO as GPIO
import time

GPIO_POS = 5


class SimpleLED:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(GPIO_POS, GPIO.OUT)

    def __del__(self):
        GPIO.cleanup()

    @staticmethod
    def on():
        GPIO.output(GPIO_POS, GPIO.HIGH)

    @staticmethod
    def off():
        GPIO.output(GPIO_POS, GPIO.LOW)


if __name__ == '__main__':

    sLED = SimpleLED()
    loop_count = 1
    loop_max = 3

    while loop_count <= loop_max:
        print(f'Loop: {loop_count} / {loop_max} ')
        sLED.on()
        time.sleep(1)
        sLED.off()
        time.sleep(1)
        loop_count += 1
