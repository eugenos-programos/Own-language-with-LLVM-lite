from llvmlite import ir     


class ColumnVariable:

    def __init__(self, name:str, value:tuple, el_type:str, builder:ir.builder.IRBuilder) -> None:
        self.name = name
        bas_type = ir.DoubleType() if el_type == 'numb' else ir.IntType(8)
        self.type = ir.ArrayType(bas_type, len(value))
        self.var = ir.Constant(self.type, self.value)
        self.builder = builder
        self.compile_column_init()

    def compile_column_init(self):
        self.ptr = self.builder.alloca(self.type)
        self.builder.store(self.var, self.ptr)

    def get_element(self, index:int):
        val = self.builder.extract_value(self.ptr, index)
        return val
        
    def insert_element(self, value:int|str, index):
        return self.builder.insert_value(self.ptr, value, index)
    
