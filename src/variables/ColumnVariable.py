from llvmlite import ir
from .IterVariable import IterVariable
from .NumbVariable import NumbVariable


class ColumnVariable(IterVariable):

    def __init__(self, elements: tuple, size: NumbVariable, builder: ir.builder.IRBuilder, ptr=None) -> None:
        super().__init__(elements, size, builder, ptr)

    def set_value(self, value):
        self.size = value.size
        self.type = value.type
        self.var = value.var
        self.compile_init()

    def get_value(self):
        return self.ptr

    def copy_variable(self, builder):
        return ColumnVariable(self, self.n_rows, self.n_cols, builder)
