import json
import os


class AbstractCache(object):

    filePath = None
    fileExt = None

    def __init__(self, name):
        self.filePath = '{}.{}'.format(name, self.fileExt)

    def exists(self):
        return os.path.exists(self.filePath)

    def read(self):
        with open(self.filePath, 'r') as f:
            text = f.read()
            obj = self.decode(text)
            return obj

    def write(self, obj):
        with open(self.filePath, 'w') as f:
            text = self.encode(obj)
            f.write(text)

    def encode(self, obj):
        raise NotImplementedError('Must override with encoding standard.')

    def decode(self, text):
        raise NotImplementedError('Must override with decoding standard.')

    # If the cache exists, return the contents. If not, return the result of
    # sourceFunction and cache it
    def retrieve(self, sourceFunction):
        if self.exists():
            return self.read()
        else:
            result = sourceFunction()
            self.write(result)
            return result


class JsonCache(AbstractCache):

    fileExt = 'json'

    def encode(self, obj):
        return json.dumps(obj)

    def decode(self, text):
        return json.loads(text)
