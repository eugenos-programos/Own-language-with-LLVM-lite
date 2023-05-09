from llvmlite import ir     


class ColumnVariable:
    def __init__(self, name:str, elements:tuple, el_type:str, builder:ir.builder.IRBuilder) -> None:
        self.elements = elements
        self.name = name
        self.type = ir.DoubleType() if el_type == 'numb' else ir.IntType(8)
        self.builder = builder

    def compile_column_init(self):
        self.array_type = ir.ArrayType(self.type, len(self.elements))
        self.column_var = ir.Constant(self.array_type, self.elements)
        self.column_ptr = self.builder.alloca(self.array_type)
        self.builder.store(self.column_var, self.column_ptr)

    def get_element(self, index:int):
        val = self.builder.extract_value(self.column_ptr, index)
        return val
    
    def insert_element(self, value:int|str, index):
        return self.builder.insert_value(self.column_ptr, value, index)
    
    
