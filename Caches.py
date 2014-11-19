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


class JsonCache(AbstractCache):

    fileExt = 'json'

    def encode(self, obj):
        return json.dumps(obj)

    def decode(self, text):
        return json.loads(text)
