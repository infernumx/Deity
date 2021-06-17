from .types import Env
import requests




def to_string(x):
    if type(x) == bool:
        return str(x).lower()
    elif x is None:
        return 'null'
    return str(x)

class stdlib:
    @staticmethod
    def put(*args, **kwargs):
        args = [to_string(x)
                for x in args]
        print(*args, **kwargs)
    
    @staticmethod
    def urlreq(url):
        _r = requests.get(url)
        return _r


_stdlib = {
    'put': stdlib.put,
    'urlreq': {
        'get': stdlib.urlreq
    }
}

std = Env()
std.update(_stdlib)
