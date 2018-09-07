import spidev
import time
import requests
import sys
import hashlib
from docopt import docopt
import RPi.GPIO as GPIO
import subprocess
from big_arrow import UP,DOWN,RIGHT,LEFT

from os import path
from docopt import docopt


ROOT_DIR = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))

HTS_VOICE_DIRECTORY = f'summer-intern-2018-blockchain-raspberry/data/hts-voice/'
HTS_VOICES = {
    'default': 'nitech_jp_atr503_m001.htsvoice',
}
MECAB_DIR = '/var/lib/mecab/dic/open-jtalk/naist-jdic'


class Jtalk:
    def __init__(self, voice_model='default'):
        self._open_jtalk = ['open_jtalk']
        self._mech = ['-x', MECAB_DIR]
        self._htsvoice = ['-m', HTS_VOICE_DIRECTORY + HTS_VOICES['default']]
        self._speed = ['-r', '1.0']
        self._outwav = ['-ow', 'out.wav']

        if voice_model in HTS_VOICES:
            self._htsvoice = ['-m', HTS_VOICE_DIRECTORY + HTS_VOICES[voice_model]]

    def talk(self, text):
        print(self._htsvoice)
        cmd = self._open_jtalk + self._mech + self._htsvoice + self._speed + self._outwav
        c = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        c.stdin.write(text.encode('utf-8'))
        c.stdin.close()
        c.wait()
        aplay = ['aplay', 'out.wav']
        subprocess.Popen(aplay)

    @property
    def htsvoice(self):
        return self._htsvoice

    @htsvoice.setter
    def htsvoice(self, voice_model):
        if voice_model in HTS_VOICES:
            self._htsvoice = ['-m', HTS_VOICE_DIRECTORY + HTS_VOICES[voice_model]]


#ノード建てている人のIPアドレス：翌日には変わるので要注意
HOST = '192.168.213.131'
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

    # ひたすら入力を待ち続ける
    while True:
        
        password = ""

        flag = False
        #コマンド入力は発生したかどうか
        commandInput = False
        #IDとパスワードを入力するかどうか
        registerFlag = False

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
                #新しいパスワードを入力してユーザ登録する時は最初に中心を押し込んだ後にコマンドを入力する
                if sw_level == 1:
                    if commandInput == False:
                        print("register")
                        registerFlag = True
                        time.sleep(delay * 2)
                        continue
                    print(password)
                    break

                #ジョイスティックの初期位置はコマンドとして認識させない 上下左右に押し込んだ時だけコマンド取得
                if 600 < x < 890 and 700 < y < 870 :
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
                        displayText = LEFT
                    else:
                        command = "up"
                        displayText = UP
                else:
                    if y - x < 0:  
                        command = "right"
                        displayText = RIGHT
                    else:
                        command = "down"
                        displayText = DOWN

                password += command
                print(displayText)
                commandInput = True
                time.sleep(delay)

        #ハッシュ化
        hashString = hashlib.md5(password.encode("utf-8")).hexdigest()

        #新規登録（POST：ID+Password）
        #postで送信

        if registerFlag == True:
            chaincode = 'kawaya'
            function_name = 'putUser'
            args = 'testID01,' + hashString
            requester = APIRequest()
            res = requester.invoke(chaincode, function_name, args)
            #予約した時に残高を減らす
            chaincode = 'kawaya'
            function_name = 'getUser'
            args = hashString
            requester = APIRequest()
            res = requester.query(chaincode, function_name, args)
            balance = res['user']['balance'] - 10
            #残高に反映
            function_name = 'updateBalance'
            args = hashString + ',' + str(balance)
            requester = APIRequest()
            res = requester.invoke(chaincode, function_name, args)
            #予約通知
            model = 'default'
            text = "よやくしました　ざんがくは" + str(res['user']['balance']) + "です"
            talker = Jtalk(model)
            talker.talk(text)
            #今回はコマンド入力上からの個室IDの差押えは未実装？
        else:
            #扉を開けるかどうかの判断を仰ぐ（GET：Password）＞ 
            #GEtで送信
            print("confirm")
            chaincode = 'kawaya'
            function_name = 'unlock'
            #ここはHash値にする
            args = hashString
            requester = APIRequest()
            res = requester.query(chaincode, function_name, args)

            print(res)
            
            #getUserしてきたユーザーのパスワードと一致して入れば解錠（今回は音を鳴らす）
            #print(res['user']['password'])
            #print(res['user']['balance'])

            if res['is_unlock'] == True:
                print("open")
                #トイレ解錠通知
                model = 'default'
                text = "といれがひらきました"

                talker = Jtalk(model)
                talker.talk(text)

            else:
                #トイレ施錠したまま
                print("open false")
                model = 'default'
                text = "コマンドがまちがっています"
                talker = Jtalk(model)
                talker.talk(text)
            
        print(res)
        #トイレ解錠の有無に関わらず次の入力に備えて待つ
        time.sleep(delay * 10)

    sys.exit(0)
