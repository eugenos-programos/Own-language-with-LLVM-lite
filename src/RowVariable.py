from llvmlite import ir


class RowVariable:
    def __init__(self, name:str, elements:tuple, el_type:str, builder:ir.builder.IRBuilder) -> None:
        self.elements = elements
        self.name = name
        self.type = ir.DoubleType() if el_type == 'numb' else ir.IntType(8)
        self.builder = builder

    def compile_row_init(self):
        self.array_type = ir.ArrayType(self.type, len(self.elements))
        self.row_var = ir.Constant(self.array_type, self.elements)
        self.row_ptr = self.builder.alloca(self.array_type)
        self.builder.store(self.row_var, self.row_ptr)

    def get_element(self, index:int):
        val = self.builder.extract_value(self.row_ptr, index)
        return val

    def insert_element(self, value:int|str, index):
        return self.builder.insert_value(self.row_ptr, value, index)
