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
    def conditional_input(prompt: str = '', condition: callable=None):
        '''Retries until a valid input is received'''
        try:
            user_input = input(prompt)
            if condition:
                if condition(user_input):
                    return user_input
                return stdlib.conditional_input(prompt, condition)
            return user_input
        except Exception as e:
            return stdlib.conditional_input(prompt, condition)

    @staticmethod
    def to_int(value):
        return int(value)

    @staticmethod
    def to_float(value):
        return float(value)

    @staticmethod
    def to_str(value):
        return str(value)

    @staticmethod
    def to_bool(value):
        return bool(value)

    @staticmethod
    def memaddr(v):
        return hex(id(v))


_stdlib = {
    'put': stdlib.put,
    'input': stdlib.conditional_input,
    'converter': {
        'to_integer': stdlib.to_int,
        'to_float': stdlib.to_float,
        'to_string': stdlib.to_str,
        'to_boolean': stdlib.to_bool
    },
    'memaddr': stdlib.memaddr
}

std = Env()
std.update(_stdlib)
