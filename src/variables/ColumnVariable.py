from llvmlite import ir
from .IterVariable import IterVariable
from .NumbVariable import NumbVariable


class ColumnVariable(IterVariable):

    def __init__(self, elements: tuple, size: NumbVariable, builder: ir.builder.IRBuilder, ptr=None) -> None:
        super().__init__(elements, size, builder, ptr)
        
    def copy_variable(self, builder):
        return ColumnVariable(self, self.size, builder)
