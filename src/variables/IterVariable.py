from llvmlite import ir
from src.configs import MAX_STR_SIZE, MAX_ARR_SIZE
from ..basic_types import iter, i8
from .NumbVariable import NumbVariable


class IterVariable:

    basic_type = iter

    def __init__(self, elements: tuple, size: int, builder: ir.builder.IRBuilder, ptr=None, func = None) -> None:
        self.builder = builder
        self.size = NumbVariable(size, builder)

        elements += ["" * MAX_STR_SIZE] * (MAX_ARR_SIZE - len(elements))

        if ptr is not None:
            self.ptr = ptr
            self.var = self.builder.load(self.ptr)
        else:
            cvars = [ir.Constant(ir.ArrayType(ir.IntType(8), MAX_STR_SIZE), bytearray(
                var + ' ' * (MAX_STR_SIZE - len(var)), 'utf-8')) for var in elements]
            self.type = ir.ArrayType(ir.ArrayType(ir.IntType(8), MAX_STR_SIZE), len(elements))
            self.var = ir.Constant(self.type, cvars)


            result = func(self.builder, self.size, self)

            self.var = ir.Constant(iter, result)



    def get_value(self):
        return self.var
