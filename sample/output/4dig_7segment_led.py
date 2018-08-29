import RPi.GPIO as GPIO
import time

LIGHT_INTERVAL = 0.001
GPIO.setmode(GPIO.BCM)


class SegmentGPIOPin:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.LOW)

    def on(self):
        GPIO.output(self.pin, GPIO.HIGH)

    def off(self):
        GPIO.output(self.pin, GPIO.LOW)


# こちらはLOWがon,HIGHがoff
class DigitGPIOPin:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.HIGH)

    def on(self):
        GPIO.output(self.pin, GPIO.LOW)

    def off(self):
        GPIO.output(self.pin, GPIO.HIGH)


class SegmentsPattern:
    TOP = SegmentGPIOPin(11)
    CENTER = SegmentGPIOPin(18)
    BOTTOM = SegmentGPIOPin(8)
    LEFT_UPPER = SegmentGPIOPin(10)
    LEFT_LOWER = SegmentGPIOPin(7)
    RIGHT_UPPER = SegmentGPIOPin(4)
    RIGHT_LOWER = SegmentGPIOPin(23)
    DOT = SegmentGPIOPin(25)

    LIGHT_ON = 1
    LIGHT_OFF = 0
    SEGMENT_2_GPIO_PIN = (
        TOP, RIGHT_UPPER, RIGHT_LOWER, BOTTOM,
        LEFT_LOWER, LEFT_UPPER, CENTER, DOT
    )

    def __init__(self, *pattern):
        self.pattern = pattern

    def light(self):
        for pin, seg in zip(self.SEGMENT_2_GPIO_PIN, self.pattern):
            if seg is self.LIGHT_ON:
                pin.on()
            else:
                pin.off()


class FourDigitSevenSegmentLED:
    DIGIT_2_GPIO_PIN = (
        DigitGPIOPin(22),
        DigitGPIOPin(27),
        DigitGPIOPin(17),
        DigitGPIOPin(24),
    )
    CHAR_2_SEGMENTS = {
        ' ': SegmentsPattern(0, 0, 0, 0, 0, 0, 0, 0),
        '0': SegmentsPattern(1, 1, 1, 1, 1, 1, 0, 0),
        '1': SegmentsPattern(0, 1, 1, 0, 0, 0, 0, 0),
        '2': SegmentsPattern(1, 1, 0, 1, 1, 0, 1, 0),
        '3': SegmentsPattern(1, 1, 1, 1, 0, 0, 1, 0),
        '4': SegmentsPattern(0, 1, 1, 0, 0, 1, 1, 0),
        '5': SegmentsPattern(1, 0, 1, 1, 0, 1, 1, 0),
        '6': SegmentsPattern(1, 0, 1, 1, 1, 1, 1, 0),
        '7': SegmentsPattern(1, 1, 1, 0, 0, 0, 0, 0),
        '8': SegmentsPattern(1, 1, 1, 1, 1, 1, 1, 0),
        '9': SegmentsPattern(1, 1, 1, 1, 0, 1, 1, 0),
    }

    def light(self, digit, char):
        """
        指定桁に指定の文字を点灯
        :param digit: int 桁数(1~4)
        :param char: string 表示する数字や文字
        :return: None
        """
        # 表示する文字のチェック
        if char not in self.CHAR_2_SEGMENTS:
            return

        # セグメントLED点灯
        self.CHAR_2_SEGMENTS[char].light()

        # 同時に点灯できるのは一桁だけなので一度全ての桁をoff
        for dig in self.DIGIT_2_GPIO_PIN:
            dig.off()

        # 今回点灯対象の桁点灯
        self.DIGIT_2_GPIO_PIN[digit - 1].on()


# テストとして動かしているマシンの現在時刻を表示
if __name__ == '__main__':
    segLED = FourDigitSevenSegmentLED()
    try:
        while True:
            # 現在時刻を取得
            time.sleep(LIGHT_INTERVAL)
            now = time.strftime('%H%M')
            time_dig_list = list(now)

            for i, number in enumerate(time_dig_list):
                digit = i + 1
                segLED.light(digit, number)
                time.sleep(LIGHT_INTERVAL)
    finally:
        GPIO.cleanup()
