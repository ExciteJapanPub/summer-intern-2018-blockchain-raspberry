import spidev
import time
import os

POWER_SUPPLY = 3.3

class AnalogSensorReader:
    def __init__(self, max_speed_hz=1000000):
        self._spi = spidev.SpiDev()
        self._spi.open(0, 0)
        self._spi.max_speed_hz = max_speed_hz

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
        volts = (data * POWER_SUPPLY) / float(1023)
        volts = round(volts, places)
        return volts



def convert_temperature(data, decimal_places):
    # ADC Value
    # レベル値   温度    電圧
    #    0      -50    0.00
    #   78      -25    0.25
    #  155        0    0.50
    #  233       25    0.75
    #  310       50    1.00
    #  465      100    1.50
    #  775      200    2.50
    # 1023      280    3.30

    temp = ((data * 330) / float(1023)) - 50
    temp = round(temp, decimal_places)
    return temp



if __name__ == "__main__":

    # 各センサのチャネル
    sensor_module_channel = 0
    temp_channel = 1

    # ループ間の遅延時間
    delay = 5

    max_count = 50

    with AnalogSensorReader() as asr:
        for i in range(max_count):
            # センサモジュールのデータの読み取り
            sensor_module_level = asr.read_row_data_for_channel(sensor_module_channel)
            sensor_module_volts = asr.convert_volts(sensor_module_level, 2)

            # アナログ温度センサのデータの読み取り
            temp_level = asr.read_row_data_for_channel(temp_channel)
            temp_volts = asr.convert_volts(temp_level, 2)
            temp = convert_temperature(temp_level, 2)

            print(f"-------------------- loop: {i} ------------------------")
            print(f"Sensor Module: {sensor_module_level} ({sensor_module_volts}V)")
            print(f"Temp         : {temp_level} ({temp_volts}V) {temp} deg C")

            time.sleep(delay)




