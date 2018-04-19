import collections
import itertools
import numpy
from pandas.core.dtypes.generic import ABCSeries

class Block:
    def __init__(self, values, placement, ndim=None):
        self.ndim = self._check_ndim(values, ndim)
        self.mgr_locs = placement
        self.values = values

    def _check_ndim(self, values, ndim):
        return ndim or values.ndim


class IntBlock(Block):
    pass


class FloatBlock(Block):
    pass


class BlockManager:
    def __init__(self, blocks, axes):
        if not isinstance(blocks, tuple):
            raise TypeError('blocks must be of type tuple')
        if not all(isinstance(block, Block) for block in blocks):
            raise TypeError('blocks must be a tuple of Block elements')
        self.blocks = blocks

    def _consolidate_inplace(self):
        pass


class SingleBlockManager(BlockManager):
    pass


def get_block_type(values, dtype=None):
    """
    Return block class for the speficied data type.
    """
    vtype = (dtype or values.dtype).type
    if issubclass(vtype, numpy.integer):
        return IntBlock
    if issubclass(vtype, numpy.floating):
        return FloatBlock
    else:
        raise NotImplementedError('Only int and float blocks are supported')


def _stack_arrays(tuples, dtype):
    def _asarray_compat(x):
        if isinstance(x, ABCSeries):
            return x._values
        else:
            return numpy.asarray(x)

    def _shape_compat(x):
        if isinstance(x, ABCSeries):
            return len(x),
        else:
            return x.shape

    placement, names, arrays = zip(*tuples)

    first = arrays[0]
    shape = (len(arrays),) + _shape_compat(first)

    stacked = numpy.empty(shape, dtype=dtype)
    for i, arr in enumerate(arrays):
        stacked[i] = _asarray_compat(arr)

    return stacked, placement


def make_block(values, placement, klass=None, ndim=None, dtype=None):
    """
    Return an instance of Block of the appropriate type.
    """
    if klass is None:
        dtype = dtype or values.dtype
        klass = get_block_type(values, dtype)
    return klass(values, ndim=ndim, placement=placement)


def _multi_blockify(tuples, dtype=None):
    """
    Return a list of blocks from multiple columns of the same type.
    """
    grouper = itertools.groupby(tuples, lambda x: x[2].dtype)
    new_blocks = []
    for dtype, tup_block in grouper:
        values, placement = _stack_arrays(list(tup_block), dtype)
        block = make_block(values, placement=placement)
        new_blocks.append(block)
    return new_blocks


def form_blocks(arrays, names, axes):
    """
    Return a list of blocks from a list of arrays.

    This function groups the columns by type, and each block is of a specific
    dtype.
    """
    blocks_dict = collections.defaultdict(list)
    for i in range(len(names)):
        name = names[i]
        column = arrays[i]
        block_type = get_block_type(column)
        blocks_dict[block_type.__name__].append((i, name, column))

    blocks = []
    if len(blocks_dict['IntBlock']):
        int_blocks = _multi_blockify(blocks_dict['IntBlock'])
        blocks.extend(int_blocks)
    if len(blocks_dict['FloatBlock']):
        float_blocks = _multi_blockify(blocks_dict['FloatBlock'])
        blocks.extend(float_blocks)
    return blocks


def create_block_manager_from_arrays(arrays, names, axes):
    """
    Create a BlockManager object from a list of arrays.
    """
    blocks = tuple(form_blocks(arrays, names, axes))
    mgr = BlockManager(blocks, axes)
    mgr._consolidate_inplace()
    return mgr
