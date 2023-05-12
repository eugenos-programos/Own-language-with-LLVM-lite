from llvmlite import ir     
from src.configs import MAX_STR_SIZE


class ColumnVariable:

    def __init__(self, name:str, value:tuple, builder:ir.builder.IRBuilder) -> None:
        self.name = name
        cvars = [ir.Constant(ir.ArrayType(ir.IntType(8), MAX_STR_SIZE), bytearray(var, 'utf-8')) for var in value]
        self.size = len(value)
        self.type = ir.ArrayType(ir.ArrayType(ir.IntType(8), MAX_STR_SIZE), self.size)
        self.var = ir.Constant(self.type, cvars)
        self.builder = builder
        self.compile_column_init()

    def compile_column_init(self):
        self.ptr = self.builder.alloca(self.type)
        self.builder.store(self.var, self.ptr)

    def get_value(self):
        return self.ptr

    def get_element(self, index:int):
        return self.ptr
        
    def insert_element(self, value:int|str, index):
        return self.builder.insert_value(self.ptr, value, index)
    
