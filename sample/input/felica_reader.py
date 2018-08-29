# -*- coding: utf-8 -*-
import nfc
import binascii

SUICA_TAG_SYS = "0000030000"
EMPLOYEE_CARD_TAG_SYS = "0080720000"

class FeliCaReader:
    """
    nfc.ContactlessFrontendのopen,closeをwith構文で行えるようにするためのラッパークラス
    Example:
        with FeliCaReader() as fr:
            idm = fr.read()
    """
    def __init__(self):
        self._reader = nfc.ContactlessFrontend('usb')
        self.TIME_interval = 0.2
        self.TIME_cycle = 1.0
        # 認識カードのデフォルトは社員証(入室カード)
        self.tag_sys = EMPLOYEE_CARD_TAG_SYS


    def __enter__(self):
        """
        :rtype: <nfc object>
        """
        return self

    def __exit__(self, exc_type=None, exc_val=None, exc_tb=None):

        if self._reader is not None:
            self._reader.close()

        # 例外未発生(=正常終了)ならreturn
        if exc_type is None:
            return

        # 例外発生時は原因を出力
        print(exc_type)
        print(exc_val)
        print(exc_tb)

    def set_mode(self, mode):
        # 8072(社員証), 0003(Suica)
        if mode == "suica":
            self.tag_sys = SUICA_TAG_SYS
        elif mode == "employee_card":
            self.tag_sys = EMPLOYEE_CARD_TAG_SYS


    def read(self):
        # NFC接続リクエストのための準備
        # 212F(FeliCa)で設定
        target_req_felica = nfc.clf.RemoteTarget("212F")
        target_req_felica.sensf_req = bytearray.fromhex(self.tag_sys)
        while True:
            # カードの待ち受け開始
            target_res = self._reader.sense(target_req_felica, iterations=int(self.TIME_cycle // self.TIME_interval) + 1,
                                            interval=self.TIME_interval)

            if target_res != None:
                tag = nfc.tag.activate_tt3(self._reader, target_res)
                tag.sys = 3

                # IDmを取り出す
                idm = binascii.hexlify(tag.idm)

                return idm


if __name__ == '__main__':
    with FeliCaReader() as fr:
        idm = fr.read()
        print 'FeliCa detected. idm = ' + idm
