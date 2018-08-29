import RPi.GPIO as GPIO
import time


class ThreePinSensor:
    SENSOR_PIN = 5

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.SENSOR_PIN, GPIO.IN)

    def __del__(self):
        GPIO.cleanup()

    def is_sensed(self):
        return GPIO.input(self.SENSOR_PIN)


# テストとしてセンサの検知状態に応じてLEDを点灯させる
if __name__ == '__main__':
    LED_PIN = 6

    print('Program is running...')
    print('Please press Ctrl+C to end the program...')

    sensor = ThreePinSensor()
    # センサに応じて点灯するLEDのセットアップ
    GPIO.setup(LED_PIN, GPIO.OUT, initial=GPIO.HIGH)

    while True:
        if sensor.is_sensed():
            GPIO.output(LED_PIN, GPIO.LOW)
            time.sleep(0.5)
            GPIO.output(LED_PIN, GPIO.HIGH)
            time.sleep(0.5)
            # print('Sensor input is ON')
        else:
            GPIO.output(LED_PIN, GPIO.HIGH)
            # print('Sensor input is OFF')
            time.sleep(1)
