import cv2


class VideoCapture:
    """
    cv2.video_captureのopen,releaseをwith構文で行えるようにするためのラッパークラス
    Attributes:
        device: int or string
            VideoCapture::VideoCaptureに引数として与えられるデバイスのindexもしくはファイルネーム
    Example:
        with VideoCapture(device) as capture:
            capture.read()
    """
    def __init__(self, device=None):
        """
        :param device: int or string
        """
        self._device = device or 0
        self._capture = cv2.VideoCapture(self._device)

    def __enter__(self):
        """
        :rtype: <VideoCapture object>
        """
        return self._capture

    def __exit__(self, exc_type=None, exc_val=None, exc_tb=None):

        if self._capture is not None:
            self._capture.release()

        # 例外未発生(=正常終了)ならreturn
        if exc_type is None:
            return

        # 例外発生時は原因を出力
        print(exc_type)
        print(exc_val)
        print(exc_tb)


if __name__ == '__main__':
    with VideoCapture() as cap:
        r, img = cap.read()
        cv2.imwrite('./test.jpg', img)
