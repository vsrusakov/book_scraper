import json

class FileSink:
    def __init__(self, path):
        self._file = open(path, 'w', encoding='utf-8')

    def write(self, item):
        self._file.write(json.dumps(item, ensure_ascii=False) + '\n')

    def __del__(self):
        self._file.close()


class Item:
    def __init__(self, url, tries=0):
        self.url = url
        self.start = None
        self.tries = tries
