import RPi.GPIO as GPIO
import time

GPIO_POS = 5


class Motor:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(GPIO_POS, GPIO.OUT)
        self.servo = GPIO.PWM(GPIO_POS, 50)

    def __del__(self):
        GPIO.cleanup()

    def rotate(self, angle):
        """
        モーターを回転させる。dutyの計算については以下を参考

        動作パルス：20ms–＞周波数50Hz
        ０度：1.0m–＞デユーティ5%
        ９０度：1.5ms–＞デユーティ7．5%
        １８０度：2.0ms–＞デユーティ10.0%
        :param angle: numbers
        :return:
        """
        duty = (angle / 180.0) * 10
        self.servo.start(duty)


if __name__ == '__main__':

    motor = Motor()
    angles = [90, 180, 0]

    for ang in angles:
        print(f'angle: {ang}')
        motor.rotate(ang)
        time.sleep(3)
