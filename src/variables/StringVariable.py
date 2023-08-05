from llvmlite import ir
from llvmlite.ir import CallInstr 
from src.configs import MAX_STR_SIZE
from ..basic_types import string
from .Variable import Variable


class StringVariable(Variable):

    basic_type: ir.Type = string
    convert_func: ir.Function

    def __init__(self, value: str | CallInstr, builder: ir.builder.IRBuilder) -> None:
        if isinstance(value, CallInstr):
            self.builder = builder
            self.ptr = self.builder.alloca(self.basic_type)
            self.builder.store(value, self.ptr)
            self.ptr = self.builder.load(self.ptr)
        else:
            if len(value) < MAX_STR_SIZE - 1:
                value += " " * (MAX_STR_SIZE - 1 - len(value))
            value += '\0'
            self.builder = builder
            self.var = ir.Constant(ir.ArrayType(ir.IntType(8), MAX_STR_SIZE), bytearray(value, 'utf-8'))
            self.ptr = self.builder.alloca(ir.ArrayType(ir.IntType(8), MAX_STR_SIZE))
            self.builder.store(self.var, self.ptr)
                
            result = self.convert_func(self.builder, self)
            self.ptr = self.builder.alloca(self.basic_type)
            self.builder.store(result, self.ptr)
            self.ptr = self.builder.load(self.ptr)

    def get_value(self):
        return self.ptr

    def set_value(self, value: str):
        value += '\0'
        self.type = ir.ArrayType(ir.IntType(8), len(value))
        self.var = ir.Constant(
            ir.ArrayType(ir.IntType(8), len(value)),
            bytearray(value.encode("utf8"))
        )
        self.compile_str_init()
