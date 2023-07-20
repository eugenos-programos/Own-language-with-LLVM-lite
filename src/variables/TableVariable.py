from llvmlite import ir
from src.configs import MAX_STR_SIZE
from .IterVariable import IterVariable
from .NumbVariable import NumbVariable


class TableVariable(IterVariable):

    def __init__(self, elements: tuple = None, n_cols: int = None, n_rows: int = None, builder: ir.builder.IRBuilder = None, ptr=None) -> None:
        super().__init__(elements, n_cols * n_rows, builder, ptr)

        self.n_rows = NumbVariable(n_rows, builder)
        self.n_cols = NumbVariable(n_cols, builder)

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
