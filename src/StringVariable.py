from llvmlite import ir


class StringVariable:

    def __init__(self, name:str, value:str, builder:ir.builder.IRBuilder) -> None:
        self.name = name
        self.type = ir.ArrayType(ir.IntType(8), len(value))
        self.var = ir.Constant(
            self.type,
            len(str),
            bytearray(value.encode("utf8"))
        )
        self.builder = builder
        self.compile_numb_init()

    def compile_numb_init(self):
        self.ptr = self.builder.alloca(self.type, name=self.name)
        self.builder.store(self.var, self.ptr)

    def get_value(self):
        return self.var.constant
    
    def set_value(self):
        value = self.builder.load(self.ptr, name=self.name)
        return value
    
