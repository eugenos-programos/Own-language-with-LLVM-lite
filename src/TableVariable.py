from llvmlite import ir


class TableVariable:
    def __init__(self, name:str, elements:tuple, el_type:str, builder:ir.builder.IRBuilder) -> None:
        self.elements = elements
        self.name = name
        els_type = ir.DoubleType() if el_type == 'numb' else ir.IntType(8)
        self.type = ir.ArrayType(els_type)
        self.builder = builder

    def compile_row_init(self):
        self.array_type = ir.ArrayType(self.type, len(self.elements))
        self.table_var = ir.Constant(self.array_type, self.elements)
        self.table_ptr = self.builder.alloca(self.array_type)
        self.builder.store(self.table_var, self.table_ptr)

    def get_element(self, index:int):
        val = self.builder.extract_value(self.table_ptr, index)
        return val

    def insert_element(self, value:int|str, index):
        return self.builder.insert_value(self.table_ptr, value, index)
    