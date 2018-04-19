from pandas.core.indexes.numeric import Int64Index

class RangeIndex(Int64Index):
    def __new__(cls, start=None, stop=None, step=None,
                dtype=None, copy=False, name=None, fastpath=False):
        pass
    pass