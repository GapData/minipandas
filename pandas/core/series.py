import numpy
import pandas.core


class Series(pandas.core.generic.NDFrame):
    pass


pandas.core.ops.add_special_arithmetic_methods(Series)


def _sanitize_array(data, index, dtype=None, copy=False,
                    raise_cast_failure=False):
    if not isinstance(data, list):
        raise NotImplementedError('Only data as a list is supported')
    subarr = numpy.array(data, copy=False)
    subarr = numpy.array(subarr, dtype=dtype, copy=copy)
    return subarr
