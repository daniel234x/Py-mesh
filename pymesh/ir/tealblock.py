from abc import ABC, abstractmethod
from typing import Optional, List, Tuple, Iterator, cast, TYPE_CHECKING

from .tealop import TealOp, Op
if TYPE_CHECKING:
    from ..ast import Expr
    from .tealsimpleblock import TealSimpleBlock

class TealBlock(ABC):
    """Represents a basic block of TealComponents in a graph."""

    def __init__(self, ops: List[TealOp]) -> None:
        self.ops = ops
        self.incoming: List[TealBlock] = []
    
    @abstractmethod
    def getOutgoing(self) -> List['TealBlock']:
        """Get this block's children blocks, if any."""
        pass

    @abstractmethod
    def replaceOutgoing(self, oldBlock: 'TealBlock', newBlock: 'TealBlock') -> None:
        """Replace one of this block's child blocks."""
        pass
    
    def isTerminal(self) -> bool:
        """Check if this block ends the program."""
        for op in self.ops:
            if op.getOp() in (Op.return_, Op.err):
                return True
        return len(self.getOutgoing()) == 0
    
    def validate(self, parent: 'TealBlock' = None) -> None:
        """Check that this block and its children have valid parent pointers.

        Args:
            parent (optional): The parent block to this one, if it has one. Defaults to None.
        """
        if parent is not None:
            count = 0
            for block in self.incoming:
                if parent is block:
                    count += 1
            assert count == 1
        
        for block in self.getOutgoing():
            block.validate(self)
    
    def addIncoming(self, block: 'TealBlock' = None) -> None:
        """Calculate the parent blocks for this block and its children.

        Args:
            block (optional): The parent block to this one, if it has one. Defaults to None.
        """
        if block is not None and all(block is not b for b in self.incoming):
            self.incoming.append(block)
        
        for block in self.getOutgoing():
            block.addIncoming(self)
    
    @abstractmethod
    def __repr__(self) -> str:
        pass

    @abstractmethod
    def __eq__(self, other: object) -> bool:
        pass

    @classmethod
    def FromOp(cls, op: TealOp, *args: 'Expr') -> Tuple['TealBlock', 'TealSimpleBlock']:
        """Create a path of blocks from a TealOp and its arguments.

        Returns:
            The starting and ending block of the path that encodes the given TealOp and arguments.
        """
        from .tealsimpleblock import TealSimpleBlock
        opBlock = TealSimpleBlock([op])

        if len(args) == 0:
            return opBlock, opBlock

        start = None
        prevArgEnd = None
        for i, arg in enumerate(args):
            argStart, argEnd = arg.__teal__()
            if i == 0:
                start = argStart
            else:
                cast(TealSimpleBlock, prevArgEnd).setNextBlock(argStart)
            prevArgEnd = argEnd

        cast(TealSimpleBlock, prevArgEnd).setNextBlock(opBlock)

        return cast(TealBlock, start), opBlock
    
    @classmethod
    def Iterate(cls, start: 'TealBlock') -> Iterator['TealBlock']:
        """Perform a depth-first search of the graph of blocks starting with start."""
        queue = [start]
        visited = list(queue)

        def is_in_visited(block):
            for v in visited:
                if block is v:
                    return True
            return False

        while len(queue) != 0:
            w = queue.pop(0)
            nextBlocks = w.getOutgoing()
            yield w
            for nextBlock in nextBlocks:
                if not is_in_visited(nextBlock):
                    visited.append(nextBlock)
                    queue.append(nextBlock)
    
    @classmethod
    def NormalizeBlocks(cls, start: 'TealBlock') -> 'TealBlock':
        """Minimize the number of blocks in the graph of blocks starting with start by combining
        sequential blocks. This operation does not alter the operations of the graph or the
        functionality of its underlying program, however it does mutate the input graph.

        Returns:
            The new starting point of the altered graph. May be the same or differant than start.
        """
        for block in TealBlock.Iterate(start):
            if len(block.incoming) == 1:
                prev = block.incoming[0]
                prevOutgoing = prev.getOutgoing()
                if len(prevOutgoing) == 1 and prevOutgoing[0] is block:
                    # combine blocks
                    block.ops = prev.ops + block.ops
                    block.incoming = prev.incoming
                    for incoming in prev.incoming:
                        incoming.replaceOutgoing(prev, block)
                    if prev is start:
                        start = block
        
        return start

TealBlock.__module__ = "pyteal"
