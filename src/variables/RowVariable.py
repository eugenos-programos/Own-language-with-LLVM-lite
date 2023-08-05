from llvmlite import ir
from .IterVariable import IterVariable
from .NumbVariable import NumbVariable


class RowVariable(IterVariable):
    def __init__(self, elements: list, size: NumbVariable, builder: ir.builder.IRBuilder, ptr=None) -> None:
        super().__init__(elements, size, builder, ptr)

    def set_value(self, value: IterVariable):
        self.size = value.size
        self.var = value.var
        self.ptr = value.ptr

    def get_element(self, index: int):
        return self.ptr

    def insert_element(self, value: int | str, index):
        return self.builder.insert_value(self.ptr, value, index)
