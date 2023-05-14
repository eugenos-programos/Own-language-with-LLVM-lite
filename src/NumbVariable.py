from llvmlite import ir


class NumbVariable:
    type = ir.DoubleType()

    def __init__(self, name:str, value:float|ir.Constant, builder:ir.builder.IRBuilder) -> None:
        if isinstance(value, ir.Constant):
            self.var = value
        else:
            self.var = ir.Constant(
            self.type,
            value
        )
        self.name = name
        self.builder = builder
        self.compile_numb_init()

    def compile_numb_init(self):
        self.ptr = self.builder.alloca(self.type, name=self.name)
        self.builder.store(self.var, self.ptr)

    def get_value(self):
        value = self.builder.load(self.ptr, name=self.name)
        return value
    
    def set_value(self, value:int):
        self.var = ir.Constant(self.type, value)
        self.builder.store(self.var, self.ptr)
        
