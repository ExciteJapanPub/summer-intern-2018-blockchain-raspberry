# GPIO

ピンにモジュールを接続するタイプの入力サンプル

### 必要パッケージのinstall

```
sudo apt-get install python3-rpi.gpio
```

## 3pin_sensor.py

ピンが3つあるタイプのセンサの利用サンプル

### 回路

「S」と書かれているピンにVCC(電源),「-」と書かれているピンに入力を受け取るGPIOピン、残りの一つをGNDにつなぐ。  
配線例は./image/3pin_sensor_配線.jpgを参照

## analog_sensor.py

CdSセルやアナログ温度センサのようなADコンバータを通す必要のあるタイプの利用サンプル

### 必要パッケージのinstall

```
pip install spidev
```

SPIが有効になっているか確認
```
$ lsmod | grep spi
>spi_bcm2835        16384  0
```
※なっていない場合はraspi-configで設定を変更
```
$ sudo raspi-config
```
5 INterfacing Option > P4 SPI  
の順に選択してEnabledに設定を変更する

### 回路
配線例は./image/analog_sensor0X.jpgを参照
使用したいアナログセンサは配線例のブレッドボードのf-j側に配置（わかりやすくするため）
基本的には、アナログ出力値をADコンバータのピンに繋ぎ、プログラム側で該当のチャネルを指定してデータを取り出す。

ADコンバータとRaspberryPiのピンの対応は、コンバータの型番に差異はあるがこちらのサイトが参考になる
https://sites.google.com/site/memorandumjavaandalgorithm/raspberry-pi-jiang-zuo12-adkonbata-mcp3208

# USB

USBポートにデバイスを接続するタイプの入力サンプル

## video_capture.py

USBに接続したWEBカメラから画像を取得するサンプル

### 必要パッケージのinstall

```
sudo apt install libopencv-dev libgstreamer1.0-0 libqt4-test  libjasper-dev libqtgui4
```

## motion_detect.py

USBに接続したWEBカメラから一定間隔で画像を取得して、動体を検知するサンプル  
閾値はカメラ設定位置に応じて要調整

## code_scanner.py

USBに接続したカメラから画像を撮影して、認識したQRコード/バーコードの情報を表示するサンプル

### 必要なパッケージのinstall

```
sudo apt-get install libzbar-dev libzbar0
pip install pyzbar
```

## felica_reader.py

USBに接続したFeliCaリーダーからICカードのIdmを読み込むサンプル
※使用するPythonパッケージの都合上、Python2.x系用になっています。

nfcpyではICカードに書き込みもできますが、今回は使用しないでください

### 必要なパッケージのinstall

```
sudo pip install nfcpy
```

### Sudo権限なしで動かす場合
lsusbコマンドでRC-S380のIDを調べる
```
$ lsusb
> Bus 001 Device 007: ID XXXX:YYYY Sony Corp.
```
このIDに対して以下のコマンドを実行
```
$ sudo sh -c 'echo SUBSYSTEM==\"usb\", ACTION==\"add\", ATTRS{idVendor}==\"XXXX\", ATTRS{idProduct}==\"YYYY\", GROUP=\"plugdev\" >> /etc/udev/rules.d/nfcdev.rules'
```
command input
