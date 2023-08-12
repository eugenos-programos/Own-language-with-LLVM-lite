from llvmlite import ir
from .IterVariable import IterVariable
from .NumbVariable import NumbVariable


class RowVariable(IterVariable):
    def __init__(self, elements: list, size: NumbVariable, builder: ir.builder.IRBuilder) -> None:
        super().__init__(elements, size, builder)

    def set_value(self, value: IterVariable):
        self.size = value.size
        self.var = value.var
        self.ptr = value.ptr

    def copy_variable(self, builder):
        return RowVariable(self, self.size, builder)
