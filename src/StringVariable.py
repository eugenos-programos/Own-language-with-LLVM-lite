from llvmlite import ir
from src.configs import MAX_STR_SIZE


class StringVariable:

    type = ir.ArrayType(ir.IntType(8), MAX_STR_SIZE)

    def __init__(self, name:str, value:str, builder:ir.builder.IRBuilder) -> None:
        self.name = name
        if len(value) != MAX_STR_SIZE - 1:
            raise ValueError("Incorrect string - {}".format(value))
        value += '\0'
        self.var = ir.Constant(
            self.type,
            bytearray(value.encode("utf8"))
        )
        self.builder = builder
        self.compile_str_init()

    def compile_str_init(self):
        self.ptr = self.builder.alloca(self.type, name=self.name)
        self.builder.store(self.var, self.ptr)

    def get_value(self):
        return self.ptr
    
    def set_value(self, value:str):
        value += '\0'
        self.type = ir.ArrayType(ir.IntType(8), len(value))
        self.var = ir.Constant(
            ir.ArrayType(ir.IntType(8), len(value)),
            bytearray(value.encode("utf8"))
        )
        self.compile_str_init()
    
