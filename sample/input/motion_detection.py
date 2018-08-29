import cv2
from time import sleep
from video_capture import VideoCapture


DEFAULT_MASK_THRESHOLD = 10
DEFAULT_MOTION_DETECTION_THRESHOLD = 5000


class MotionDetect:
    def __init__(self, mask_th=DEFAULT_MASK_THRESHOLD, motion_th=DEFAULT_MOTION_DETECTION_THRESHOLD):
        """
        :param mask_th: int 差分計算時の閾値(どのくらいの輝度変化があればピクセルに変化があったとみなすか)
        :param motion_th: int 動体判定時の閾値(どのくらい広い範囲のピクセル(=ピクセルの数)に変化があれば動体を検知したとみなすか)
        """
        self.mask_threshold = mask_th
        self.motion_threshold = motion_th
        self.imgQueue = [None] * 3

    def push(self, img):
        """
        差分判定用の画像をセット
        :param img: numpy.ndarray
        :return:
        """
        self.imgQueue[2] = self.imgQueue[1]
        self.imgQueue[1] = self.imgQueue[0]
        self.imgQueue[0] = img

    def frame_sub(self, img1=None, img2=None, img3=None):
        """
        フレーム間差分を計算
        参考:https://algorithm.joho.info/image-processing/frame-difference-method/

        :param img1: numpy.ndarray
        :param img2: numpy.ndarray
        :param img3: numpy.ndarray
        :rtype: numpy.ndarray|None
        """
        img1 = img1 or self.imgQueue[0]
        img2 = img2 or self.imgQueue[1]
        img3 = img3 or self.imgQueue[2]

        # ndarrayのリストに対してはallがうまく働かないのでis Noneで比較
        if img1 is None or img2 is None or img3 is None:
            print('差分検出のための画像が足りません')
            return None

        self.imgQueue = [img1, img2, img3]

        # フレームの絶対差分
        diff1 = cv2.absdiff(img1, img2)
        diff2 = cv2.absdiff(img2, img3)

        # 2つの差分画像の論理積
        diff = cv2.bitwise_and(diff1, diff2)

        # 二値化処理
        diff[diff < self.mask_threshold] = 0
        diff[diff >= self.mask_threshold] = 255

        # メディアンフィルタ処理（ゴマ塩ノイズ除去）
        mask = cv2.medianBlur(diff, 5)

        return mask

    def is_detect(self, img1=None, img2=None, img3=None):
        """
        動体があるか判定する
        :param img1: numpy.ndarray
        :param img2: numpy.ndarray
        :param img3: numpy.ndarray
        :rtype: bool
        """
        mask = self.frame_sub(img1, img2, img3)
        white_pixel = cv2.countNonZero(mask)

        return white_pixel > self.motion_threshold


if __name__ == '__main__':
    with VideoCapture() as cap:
        # カメラが起動するのに若干時間がかかるので初回にWAITを入れる
        sleep(2)
        detector = MotionDetect()

        # 動体検出の差分判定用にフレームを2枚取得してグレースケール変換しpushしておく
        detector.push(cv2.cvtColor(cap.read()[1], cv2.COLOR_RGB2GRAY))
        detector.push(cv2.cvtColor(cap.read()[1], cv2.COLOR_RGB2GRAY))

        take_count = 100

        print('動体検知開始')

        while take_count > 0:
            detector.push(cv2.cvtColor(cap.read()[1], cv2.COLOR_RGB2GRAY))

            if detector.is_detect():
                print('動体を検知しました')
                break

            take_count -= 1
            print(f'試行回数 残り{take_count}')
            sleep(1)
        else:
            print('ループないで動体を検知できませんでした')
