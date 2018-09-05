import spidev
import time
import requests
import sys
import hashlib
from docopt import docopt


__doc__ = """{f}
Usage:
    {f} (query|invoke) -c <chaincode_name> -m <function_name> -v <arguments>
    {f} [-h | --help]

Options:
    query,invoke        実行するAPIのモード
    -c <chaincode_name> チェーンコード名
    -m <function_name>  関数名
    -v <arguments>      引数をカンマ区切りで指定
    -h --help           ヘルプを表示して終了
""".format(f=__file__)

#ノード建てている人のIPアドレス：翌日には変わるので要注意
HOST = '192.168.213.132'
PORT = 3000


class APIRequest:
    def __init__(self):
        self.base_url = f'http://{HOST}:{PORT}'

    def query(self, chaincode, function_name, args):
        url = self.base_url + '/query'
        params = {
            'chaincode': chaincode,
            'function': function_name,
            'args': args,
        }
        r = requests.get(url, params=params)

        return r.json()

    def invoke(self, chaincode, function_name, args):
        url = self.base_url + '/invoke'
        params = {
            'chaincode': chaincode,
            'function': function_name,
            'args': args,
        }
        r = requests.post(url, json=params)

        return r.json()

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


if __name__ == "__main__":
    # Define sensor channels
    x_channel = 0
    y_channel = 1
    sw_channel = 2

    # Define delay between readings
    delay = 0.3

    max_count = 5000

    password = ""
    flag = False

    with AnalogSensorReader() as asr:
        while True:
            # Read the module sensor data
            x_level = asr.read_row_data_for_channel(x_channel)
            y_level = asr.read_row_data_for_channel(y_channel)
            sw_level = asr.read_row_data_for_channel(sw_channel)
            x_volts = asr.convert_volts(x_level, 2)
            y_volts = asr.convert_volts(y_level, 2)
            sw_volts = asr.convert_volts(sw_level, 2)

            x = x_level
            y = y_level

            #入力終了は中心を押しこむ
            if sw_level == 1:
                print(password)
                break

            #ジョイスティックの初期位置はコマンドとして認識させない 上下左右に押し込んだ時だけコマンド取得
            if 800 < x < 850 and 750 < y < 800 :
                time.sleep(delay)
                continue

            lineSeg1 = -1025

            #上左 or 下右のどれか
            if y + x + lineSeg1 < 0:
                flag = False

            if y + x + lineSeg1 >= 0:
                flag = True

            #上or左　又は　下or右
            if flag == False:
                if y - x >= 0:
                    command = "left"
                else:
                    command = "up"
            else:
                if y - x < 0:  
                    command = "right"
                else:
                    command = "down"


            password += command
            print(command)

            time.sleep(delay)

    #ハッシュ化
    hashString = hashlib.md5(password.encode("utf-8")).hexdigest()
    #postで送信
    chaincode = 'kawaya'
    function_name = 'putUser'
    args = 'ID01,' + hashString

    requester = APIRequest()

    res = requester.invoke(chaincode, function_name, args)
    print(res)
    sys.exit(0)
