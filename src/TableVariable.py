from llvmlite import ir
from src.configs import MAX_STR_SIZE
from src.NumbVariable import NumbVariable
from src.utils import generate_random_name


class TableVariable:
    def __init__(self, name: str, elements: tuple, n_cols: int, n_rows: int | ir.Constant, builder: ir.builder.IRBuilder) -> None:
        print("elems = ", elements)
        self.name = name
        self.builder = builder
        if isinstance(elements, ir.Constant):
            self.var = elements
            self.type = ir.ArrayType(ir.ArrayType(
                ir.IntType(8), MAX_STR_SIZE), n_rows * n_cols)
            self.raw_var = elements.constant
            print("hello")
            exit(1)
        else:
            cvars = [ir.Constant(ir.ArrayType(ir.IntType(8), MAX_STR_SIZE), bytearray(
                var, 'utf-8')) for var in elements]
            self.type = ir.ArrayType(ir.ArrayType(
                ir.IntType(8), MAX_STR_SIZE), n_rows * n_cols)
            self.var = ir.Constant(self.type, cvars)
            self.type = ir.IntType(8).as_pointer()
            self.builder.bitcast(self.var, self.type)
            self.raw_var = elements
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.compile_init()

    def compile_init(self):
        self.ptr = self.builder.alloca(self.type)
        self.builder.store(self.var, self.ptr)

    def set_value(self, value):
        self.n_cols = value.n_cols
        self.n_rows = value.n_rows
        self.type = value.type
        self.var = value.var
        self.compile_init()

    def get_element(self, index: int):
        val = self.builder.extract_value(self.table_ptr, index)
        return val

    def insert_element(self, value: int | str, index):
        return self.builder.insert_value(self.table_ptr, value, index)
