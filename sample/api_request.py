import requests
import sys
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

HOST = 'localhost'
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


if __name__ == '__main__':
    opt = docopt(__doc__)

    chaincode = opt.get('-c')
    function_name = opt.get('-m')
    args = opt.get('-v')

    requester = APIRequest()

    if opt.get('invoke') is not False:
        res = requester.invoke(chaincode, function_name, args)
        print(res)
        sys.exit(0)

    res = requester.query(chaincode, function_name, args)
    print(res)