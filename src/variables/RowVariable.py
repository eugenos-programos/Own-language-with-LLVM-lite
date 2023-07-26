from llvmlite import ir
from .IterVariable import IterVariable


class RowVariable(IterVariable):
    def __init__(self, elements: list = None, builder: ir.builder.IRBuilder = None, ptr=None, func:ir.Function=None) -> None:
        super().__init__(elements, len(elements), builder, ptr, func)

    def set_value(self, value):
        self.size = value.size
        self.type = value.type
        self.var = value.var
        self.compile_init()

    def get_element(self, index: int):
        return self.ptr

    def insert_element(self, value: int | str, index):
        return self.builder.insert_value(self.ptr, value, index)
