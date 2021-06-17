class Env(dict):
    def __init__(self, params=(), args=(), outer=None):
        self.update(zip(params, args))
        self.outer = outer

    def find(self, name):
        if name in self:
            return self[name]
        elif self.outer is not None:
            return self.outer.find(name)

        raise UnboundLocalError("{} is undefined".format(name))

class Function(object):
    def __init__(self, process, params, body, env):
        self.process, self.params, self.body, self.env = process, params, body, env
        self.type = 'function'

    def __call__(self, *args):
        params = []
        for i in range(len(self.params)):
            if type(args[i]) != self.process.types[self.params[i][1]]:
                raise TypeError("Expected type '{}' for param '{}', received '{}'.".format(self.params[i][1], self.params[i][0], self.process.rtypes[type(args[i])]))
            params.append(self.params[i][0])
        return self.process.run((self.body,), Env(params, args, self.env))

class Value(object):
    def __init__(self, value, val_type):
        self.value = value
        self.type = val_type

    def __len__(self):
        try:
            return len(self.value)
        except:
            return 1

    def __str__(self):
        return "{}: {}".format(self.value, self.type)

    def get(self):
        return self.value