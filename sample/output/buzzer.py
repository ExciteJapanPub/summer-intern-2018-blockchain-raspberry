import RPi.GPIO as GPIO
import time

GPIO_POS = 5

SCALE_2_HERTZ = {
    'C_low': 220.0,
    'D': 246.9,
    'E': 277.2,
    'F': 293.7,
    'G': 329.6,
    'A': 370.0,
    'B': 415.3,
    'C_high': 440.0
}


class Buzzer:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(GPIO_POS, GPIO.OUT)
        self.pwm = GPIO.PWM(GPIO_POS, 1000)

    def __del__(self):
        GPIO.cleanup()

    def change_frequency(self, freq):
        self.pwm.ChangeFrequency(freq)

    def change_scale(self, scale='C_low'):
        if scale not in SCALE_2_HERTZ:
            return

        freq = SCALE_2_HERTZ[scale]
        self.pwm.ChangeFrequency(freq)

    def play(self, duty):
        self.pwm.start(duty)

    def stop(self):
        self.pwm.stop()


if __name__ == '__main__':

    buz = Buzzer()
    chocho = ['G', 'E', 'E', 'F', 'D', 'D', 'C', 'D', 'E', 'F', 'G', 'G', 'G']

    for scale in chocho:
        buz.change_scale(scale)

        buz.play(50)
        time.sleep(1)

        buz.stop()
        time.sleep(0.25)
