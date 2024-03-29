from llvmlite import ir
from src.IterVariable import IterVariable
from basic_types import iter


class RowVariable(IterVariable):

    def __init__(self, elements: tuple = None, builder: ir.builder.IRBuilder = None, ptr=None) -> None:
        super().__init__(elements, len(elements), builder, ptr)

    def set_value(self, value):
        self.size = value.size
        self.type = value.type
        self.var = value.var
        self.compile_init()

    def get_value(self):
        return self.ptr

    def get_element(self, index: int):
        return self.ptr

    def insert_element(self, value: int | str, index):
        return self.builder.insert_value(self.ptr, value, index)
