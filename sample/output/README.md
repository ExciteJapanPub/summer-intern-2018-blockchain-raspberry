# GPIO

ピンにモジュールを接続するタイプの出力サンプル

### 必要パッケージのinstall

```
sudo apt-get install python3-rpi.gpio
```

## simple_LED.py

LEDを点灯させるサンプル

### 回路

参考:  
https://physical-computing-lab.net/raspberry-pi-b/3-2-raspberry-pi-b-%E3%82%A4%E3%83%B3%E3%82%BF%E3%83%A9%E3%82%AF%E3%83%86%E3%82%A3%E3%83%96%E3%83%A2%E3%83%BC%E3%83%89%E3%81%A7l%E3%83%81%E3%82%AB.html

## buzzer.py

圧電スピーカーでブザー音を鳴らすサンプル。  
周波数で音階を変えられるが、出せる音の範囲は狭い

### 回路

参考:  
https://physical-computing-lab.net/raspberry-pi-b/3-2-raspberry-pi-b-%E3%82%A4%E3%83%B3%E3%82%BF%E3%83%A9%E3%82%AF%E3%83%86%E3%82%A3%E3%83%96%E3%83%A2%E3%83%BC%E3%83%89%E3%81%A7l%E3%83%81%E3%82%AB.html  
のLEDを圧電スピーカに置き換え


## servomoter.py

サーボモーターを指定角度で動かすサンプル

### 回路

./image/servomoter_配線.jpgを参照

## 4dig_7segment_led.py

4桁7セグメントLED(数字を表示できる)を点灯させるサンプル  

### 回路
サンプルで利用したブレッドボードをそのままの状態で用意してあるので、  
ジャンパワイヤを定数に対応するGPIOピンに刺してください  
(ごちゃごちゃしているのであまり参考にならないかもしれませんが  
./image/4dig_7segment_led_配線.jpgに配線の画像を上げています)


# USB

USBポートにデバイスを接続するタイプの出力サンプル

## speaker.py

USBに接続したスピーカーから指定した日本語音声を再生するサンプル

### 必要パッケージのinstall

```
sudo apt install open-jtalk open-jtalk-mecab-naist-jdic hts-voice-nitech-jp-atr503-m001libatlas-base-dev libjasper-dev
```

### voice_model

* http://sourceforge.jp/projects/sfnet_open-jtalk/releases/
* http://www.mmdagent.jp/

などから.htsvoice形式のボイスモデルファイルをダウンロードし、  
/data/hts-voice下に置いておく  