from pandas.core.internals import BlockManager


class NDFrame:
    def __init__(self, data,fastpath=False):
        if not isinstance(data, BlockManager):
            raise TypeError('data must be of type BlockManager')
        self._data = data
