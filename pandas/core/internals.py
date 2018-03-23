

class Block:
    pass


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
