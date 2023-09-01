from llvmlite import ir
from src.configs import MAX_STR_SIZE, MAX_ARR_SIZE
from ..basic_types import iter, i8
from .NumbVariable import NumbVariable
from .Variable import Variable


class IterVariable(Variable):

    basic_type = iter
    convert_func: ir.Function

    def __init__(self, elements: tuple | object | ir.instructions.Instruction, size: NumbVariable, builder: ir.builder.IRBuilder, ptr=None) -> None:
        self.builder = builder
        self.size = NumbVariable(size, builder) if not isinstance(size, NumbVariable) else size

        if isinstance(elements, (ir.instructions.Instruction, ir.Argument)):
            self.var = elements
            self.ptr = self.builder.alloca(self.basic_type)
            self.builder.store(self.var, self.ptr)
            self.ptr = self.builder.load(self.ptr)
            return
        
        elif not isinstance(elements, (tuple, list)):
            self.var = elements.var
            self.ptr = self.builder.alloca(self.basic_type)
            self.builder.store(self.var, self.ptr)
            self.ptr = self.builder.load(self.ptr)
            return

        elements = [element + " " * (MAX_STR_SIZE - len(element) - 1) for element in elements]

        elements += [" " * (MAX_STR_SIZE - 1)] * (MAX_ARR_SIZE - len(elements))

        if ptr is not None:
            self.ptr = ptr
            self.var = self.builder.load(self.ptr)
        else:
            cvars = [ir.Constant(ir.ArrayType(ir.IntType(8), MAX_STR_SIZE), bytearray(
                var + ' ' * (MAX_STR_SIZE - len(var) - 1) + '\0', 'utf-8')) for var in elements]
            type_ = ir.ArrayType(ir.ArrayType(ir.IntType(8), MAX_STR_SIZE), len(elements))
            self.var = ir.Constant(type_, cvars)
            self.ptr = self.builder.alloca(type_)
            self.builder.store(self.var, self.ptr)

            result = self.convert_func(self.builder, self.size, self)
            self.ptr = self.builder.alloca(self.basic_type)
            self.builder.store(result, self.ptr)
            self.ptr = self.builder.load(self.ptr)

    def set_value(self, value):
        self.var = value.var
        self.size = value.size
        self.ptr = value.ptr

    def get_value(self):
        return self.ptr

    