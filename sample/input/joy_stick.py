import spidev
import time
import os

class AnalogSensorReader:
    def __init__(self):
        self._spi = spidev.SpiDev()
        self._spi.open(0, 0)
        self._spi.max_speed_hz = 1000000

    def __enter__(self):
        return self

    def __exit__(self, exc_type=None, exc_val=None, exc_tb=None):
        if self._spi is not None:
            self._spi.close()

        # 例外未発生(=正常終了)ならreturn
        if exc_type is None:
            return

        # 例外発生時は原因を出力
        print(exc_type)
        print(exc_val)
        print(exc_tb)

    def read_row_data_for_channel(self, channel):
        adc = self._spi.xfer2([1, (8 + channel) << 4, 0])
        data = ((adc[1] & 3) << 8) + adc[2]
        return data

    def convert_volts(self, data, places):
        volts = (data * 3.3) / float(1023)
        volts = round(volts, places)
        return volts



def convert_temp(data, places):
    # ADC Value
    # (approx)  Temp  Volts
    #    0      -50    0.00
    #   78      -25    0.25
    #  155        0    0.50
    #  233       25    0.75
    #  310       50    1.00
    #  465      100    1.50
    #  775      200    2.50
    # 1023      280    3.30

    temp = ((data * 330) / float(1023)) - 50
    temp = round(temp, places)
    return temp



if __name__ == "__main__":

    # Define sensor channels
    x_channel = 0
    y_channel = 1
    sw_channel = 2

    # Define delay between readings
    delay = 1

    max_count = 50

    with AnalogSensorReader() as asr:
        for i in range(max_count):
            # Read the module sensor data
            x_level = asr.read_row_data_for_channel(x_channel)
            y_level = asr.read_row_data_for_channel(y_channel)
            sw_level = asr.read_row_data_for_channel(sw_channel)
            x_volts = asr.convert_volts(x_level, 2)
            y_volts = asr.convert_volts(y_level, 2)
            sw_volts = asr.convert_volts(sw_level, 2)

            # Read the temperature sensor data
            #temp_level = asr.read_row_data_for_channel(temp_channel)
            #temp_volts = asr.convert_volts(temp_level, 2)
            #temp = convert_temp(temp_level, 2)

            print(f"-------------------- loop: {i} ------------------------")
            print(f"x: {x_level} ({x_volts}V)")
            print(f"y: {y_level} ({y_volts}V)")
            print(f"SW: {sw_level} ({sw_volts}V)")


            time.sleep(delay)




