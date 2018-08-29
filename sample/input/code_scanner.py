import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
from time import sleep
from video_capture import VideoCapture
from docopt import docopt

__doc__ = """{f}
Usage:
    {f}
    {f} <filename>
    {f} [-h | --help]

Options:
    <filename>  ファイルから画像を読み込みたい場合に指定
    -h --help   ヘルプを表示して終了
""".format(f=__file__)

FIX_CONTRAST_GAMMA = 5


class CodeScanner:
    @staticmethod
    def fix_contrast(img):
        """
        コントラスト調整
        :param img:image cv2.imread retval
        :return: image
        """
        look_up_table = [np.uint8(255.0 / (1 + np.exp(-FIX_CONTRAST_GAMMA * (i - 128.) / 255.)))
                         for i in range(256)]

        result_image = np.array([look_up_table[value]
                                 for value in img.flat], dtype=np.uint8)
        result_image = result_image.reshape(img.shape)

        return result_image

    def decode(self, img):
        """
        QRコード/バーコードを読み込んで情報を返却
        :param img:image cv2.imread retval
        :return: list
        """
        # グレースケール変換
        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # コントラスト調整
        fixed_image = self.fix_contrast(gray_image)

        decoded_objects = pyzbar.decode(fixed_image)
        return decoded_objects

    def scan(self):
        """
        カメラからQRコード/バーコードを読み込んで情報を返却
        :return: list|None
        """
        with VideoCapture() as cap:
            ret, img = cap.read()

            # 読み込めない場合はカメラが起動中の可能性があるので少し待って再取得
            if ret is not True:
                sleep(2)
                ret, img = cap.read()

            # それでもダメならメッセージを出力してNone返却
            if ret is not True:
                print('capture device is not available')
                return None

            # QRコード/バーコードが画像に含まれてるか確認したいときに利用
            # cv2.imwrite('./test.jpg', img)

            data = self.decode(img)

            return data


if __name__ == '__main__':
    opt = docopt(__doc__)

    scanner = CodeScanner()

    if opt.get('<filename>') is not None:
        image = cv2.imread(opt.get('<filename>'))
        code_data = scanner.decode(image)
    else:
        code_data = scanner.scan()

    print(code_data)
