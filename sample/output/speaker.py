import subprocess
from os import path
from docopt import docopt

__doc__ = """{f}
Usage:
    {f} [-m <voice_model>] <text>
    {f} [-h | --help]
Options:
    -m <voice_filename>  voice_modelの名前
    <text>               読み上げるテキスト(日本語)
    -h --help            ヘルプを表示して終了
""".format(f=__file__)

ROOT_DIR = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))

HTS_VOICE_DIRECTORY = f'{ROOT_DIR}/data/hts-voice/'
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


if __name__ == '__main__':
    opt = docopt(__doc__)

    model = 'default'
    if opt.get('-m') is not False:
        model = opt.get('-m')

    text = opt.get('<text>')

    talker = Jtalk(model)
    talker.talk(text)
