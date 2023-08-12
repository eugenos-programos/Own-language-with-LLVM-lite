from llvmlite import ir
from src.configs import MAX_STR_SIZE
from .IterVariable import IterVariable
from .NumbVariable import NumbVariable


class TableVariable(IterVariable):

    def __init__(self, elements: tuple, n_rows: NumbVariable, n_cols: NumbVariable, builder: ir.builder.IRBuilder) -> None:
        super().__init__(elements, n_cols * n_rows, builder)

        self.n_rows = n_rows
        self.n_cols = n_cols

    def set_value(self, value):
        self.n_cols = value.n_cols
        self.n_rows = value.n_rows
        self.type = value.type
        self.var = value.var
        self.compile_init()

    def copy_variable(self, builder):
        return TableVariable(self, self.n_rows, self.n_cols, builder)
