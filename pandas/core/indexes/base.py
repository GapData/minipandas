

class Index:
    def __init__(self,values):
        self._data = values
        pass

    def __getitem__(self, key):
        return self._data[key]

    def __len__(self):
        return len(self._data)

    pass


def _ensure_index(index_like, copy=False):
    return index_like