from .stdlib import *
from .parser import Parser
from .types import *
import pprint
from typing import *

class Processor:
    def __init__(self, tree, debug=False, lexer=None, env={}):
        if not isinstance(env, Env):
            _env = env
            env = Env(outer=std)
            env.update(_env)
        self.tree = tree
        self.env = Env(outer=env)
        self.should_return = False
        self.depth = 0
        self.debug = debug
        self.lexer = lexer
        self.types  = { 'int': int, 'float': float, 'str': str, 'obj': object, 'NullType': NullType, 'null': LiteralNull, 'bool': bool}
        self.rtypes = { int: 'int', float: 'float', str: 'str', object: 'obj', NullType: 'NullType', LiteralNull: 'null', bool: 'bool'}

    def run(self, tree=None, env={}):
        current_env = self.env
        result = None
        if env != {}:
            self.env = env
        if tree is None:
            for line in self.tree:
                if self.debug:
                    print('[DEBUG] Tree ->', ' '.join(str(line).split()))
                result = self.evaluate(line)
                if self.depth == 0:
                    self.should_return = False
                if self.should_return:
                    self.should_return = False
                    return result
        else:
            for line in tree:
                if self.debug:
                    print('[DEBUG] Tree ->', ' '.join(str(line).split()))
                result = self.evaluate(line)
                if self.depth == 0:
                    self.should_return = False
                if self.should_return:
                    self.should_return = False
                    return result
        self.env = current_env
        return result

    def evaluate(self, parsed):
        if not isinstance(parsed, tuple):
            return parsed

        action = parsed[0]

        if action in '+-*/%':
            return self.handle_math_op(action, parsed)
        elif action in ('or', 'and', 'equal', 'inequal', 'lthan', 'gthan'):
            return self.handle_comparison(action, parsed)
        elif action == '!':
            return not self.evaluate(parsed[1])
        elif action == '.':
            if type(parsed[1]) == tuple:
                var = self.evaluate(parsed[1])
            else:
                var = self.env.find(parsed[1])
            if isinstance(var, Value):
                try:
                    res = self.evaluate(var.value[parsed[2]])
                except TypeError:
                    res = self.evaluate(getattr(var.value, parsed[2]))
            else:
                try:
                    res = self.evaluate(var[parsed[2]])
                except TypeError:
                    res = self.evaluate(getattr(var, parsed[2]))
            return res
        elif action == 'pipe':
            if isinstance(parsed[1], list):
                args = [self.evaluate(arg) for arg in parsed[1]]
            else:
                args = [self.evaluate(parsed[1])]
            fn = self.env.find(parsed[2])
            if not isinstance(fn, Function):
                if type(fn) == type(lambda x: x):
                    return fn(*args)
            else:
                return fn(*args)
            return None
        elif action == 'return':
            expr = self.evaluate(parsed[1])
            self.should_return = True
            return expr
        elif action == 'var_assign':
            name = parsed[1]
            _type = parsed[2]
            _range = parsed[3][1]
            self.env.update({name: Value(None, _type)})
            self.evaluate(parsed[3])
        elif action == 'for':
            _range = range(*parsed[2][1])
            for i in _range:
                self.env.update({parsed[1]: Value(i, type(i))})
                self.run((parsed[3],))
            self.env.pop(parsed[1])
        elif action == 'while':
            expr = parsed[1]
            while self.evaluate(expr):
                self.run((parsed[2],))
        elif action == 'var_define':
            # Var definition
            name = parsed[1]
            value = self.evaluate(parsed[2])
            _type = self.rtypes[parsed[3]]
            eval_type = type(value).__name__
            if _type != 'obj' and eval_type != _type:
                raise TypeError(f"Expected type '{_type}' for variable '{name}', received '{eval_type}'")
                return None
            self.env.update({name: Value(value, _type)})
        elif action == 'var_define_no_expr':
            # Var definition without an expression
            name = parsed[1]
            _type = parsed[2]
            self.env.update({name: Value(None, _type)})
        elif action == 'var_redefine':
            # Var redefinition
            name = parsed[1]
            if not self.env.find(name):
                return None
            value = parsed[2]
            self.env.update({name: self.evaluate(value)})
        elif action == 'call':
            # Function call
            if isinstance(parsed[1], tuple):
                func = self.evaluate(parsed[1])
            else:
                func = self.env.find(parsed[1])
            if isinstance(func, Value):
                func = func.get()

            if not isinstance(func, Function):
                if type(func) == type(lambda x: x):
                    args = [self.evaluate(arg) for arg in parsed[2][1]]
                    self.depth += 1
                    res = func(*args)
                    self.depth -= 1
                    return res
                else:
                    raise ValueError('\'%s\' not a function' % parsed[1])

            args = [self.evaluate(arg) for arg in parsed[2][1]]
            self.depth += 1
            res = func(*args)
            self.depth -= 1
            return res
        elif action == 'if':
            # If statement
            cond = self.evaluate(parsed[1])
            if cond:
                return self.evaluate(parsed[2])
            if parsed[3] is not None:
                return self.evaluate(parsed[3])
        elif action == 'fn':
            # Function definition
            params = parsed[2]
            body = parsed[3]
            self.env.update({parsed[1]: Function(
                self, params[1], body, self.env, name=parsed[1])})
            return None
        elif action == 'id':
            # Retrieves identifier from environment
            var = self.env.find(parsed[1])
            if var is None:
                raise NameError(f'Identifier \'{parsed[1]}\' not found.')
            if not isinstance(var, Value):
                return var
            return var.get()
        elif action == 'condition':
            return self.evaluate(parsed[1])
        elif action == 'block':
            return self.run(parsed[1])

    def handle_comparison(self, op, parsed):
        evaluate_args = lambda args: [self.evaluate(arg)
                                      for arg in args]
        if op == 'or':
            a, b = evaluate_args(parsed[1:3])
            return a or b
        elif op == 'and':
            a, b = evaluate_args(parsed[1:3])
            return a and b
        elif op == 'equal':
            a, b = evaluate_args(parsed[1:3])
            _op = parsed[3]
            if _op == '===':
                return a is b
            return a == b
        elif op == 'inequal':
            a, b = evaluate_args(parsed[1:3])
            _op = parsed[3]
            if _op == '!==':
                return a is not b
            return a != b
        elif op == 'gthan':
            op = parsed[1]
            a, b = evaluate_args(parsed[2:4])
            if op == '>':
                return a > b
            elif op == '>=':
                return a >= b
        elif op == 'lthan':
            op = parsed[1]
            a, b = evaluate_args(parsed[2:4])
            if op == '<':
                return a < b
            elif op == '<=':
                return a <= b

    def handle_math_op(self, op, parsed):
        evaluate_args = lambda args: [self.evaluate(arg)
                                      for arg in args]
        if op == '+':
            a, b = evaluate_args(parsed[1:3])
            # Implicit str/int conversion
            types = {(str, int): lambda x, y: x + str(y),
                     (int, str): lambda x, y: str(x) + y}
            if callback := types.get((type(a), type(b))):
                return callback(a, b)
            return a + b
        elif op == '-':
            a, b = evaluate_args(parsed[1:3])
            return a - b
        elif op == '*':
            a, b = evaluate_args(parsed[1:3])
            return a * b
        elif op == '/':
            a, b = evaluate_args(parsed[1:3])
            return a / b
        elif op == '%':
            a, b = evaluate_args(parsed[1:3])
            return a % b

