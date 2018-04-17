import pandas.core

from pandas.core.indexes.base import _ensure_index

def extract_index(data):
    """Extract the index from the data, or return a default index.

    Currently it always return the default index, because the only supported
    data is a dict of lists, which does not have index information.
    """
    column_length = None
    for column in data:
        if not isinstance(column, list):
            raise NotImplementedError('DataFrame constructor only supports '
                                      'data as a dict of list')
        if column_length is None:
            column_length = len(column)
        elif len(column) != column_length:
            raise ValueError('All columns must have the same size')

    return pandas.core.indexes.RangeIndex(0, column_length, name=None)


def _homogenize(data, index, dtype=None):
    homogenized = []
    for column in data:
        column = pandas.core.series._sanitize_array(column, index,
                                                    dtype=dtype, copy=False,
                                                    raise_cast_failure=False)
        homogenized.append(column)
    return homogenized


def _arrays_to_mgr(arrays, arr_names, index, columns, dtype=None):
    if index is None:
        index = extract_index(arrays)

    arrays = _homogenize(arrays, index, dtype)
    axes = [_ensure_index(columns), _ensure_index(index)]
    return pandas.core.internals.create_block_manager_from_arrays(arrays,
                                                                  arr_names,
                                                                  axes)


class DataFrame(pandas.core.generic.NDFrame):
    def __init__(self, data=None, index=None, columns=None, dtype=None,
                 copy=False):
        if isinstance(data, dict):
            mgr = self._init_dict(data, index, columns, dtype=dtype)
        else:
            raise NotImplementedError('DataFrame constructor only supports '
                                      'data as a dict')
        pandas.core.generic.NDFrame.__init__(self, mgr, fastpath=True)

    def _init_dict(self, data, index, columns, dtype=None):
        keys = pandas.core.common._dict_keys_to_ordered_list(data)
        columns = data_names = pandas.core.indexes.Index(keys)
        arrays = [data[k] for k in keys]
        return _arrays_to_mgr(arrays, data_names, index, columns, dtype=dtype)
