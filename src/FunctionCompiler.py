from llvmlite.ir import Module
from llvmlite import ir
from src.basic_types import *
from src.configs import MAX_STR_SIZE
from src.Function import Function
from src.ColumnVariable import ColumnVariable
from src.NumbVariable import NumbVariable
from src.StringVariable import StringVariable
from src.RowVariable import RowVariable
from src.TableVariable import TableVariable


class FunctionCompiler:

    def __init__(self, module) -> None:
        self.module = module
        self._functions = {}
        self._load_builtin_functions()
        self._call_function_map = {
            "print": self.call_print_func
        }

    def _load_builtin_functions(self):
        function_parameters = [
            [i32, [i8.as_pointer()], "printf", True],
            [i32, [], "length", False],
            [void, [iter, i32, i32], "print_row_or_column", False],
            [string, [], "read_string", False],
            [void, [iter, i32, i32], "print_table", False],
            [iter, [iter, i32, i32, iter, i32, i32], "mul_tables", False]
        ]
        for func_params in function_parameters:
            self._save_func_to_dict(*func_params)

    def _save_func_to_dict(self, return_type: ir.Type, arg_types: list, name: str, var_arg: bool = False):
        function = Function(self.module,
            ir.FunctionType(
                return_type,
                arg_types,
                var_arg=var_arg
            ),
            name
        )
        self._functions[name] = function

    def call_function(self, name: str, args: list, builder: ir.builder.IRBuilder):
        call_function = self._call_function_map[name]
        return call_function(*args, builder)

    def call_mult_tables_function(self, first_table: TableVariable, second_table: TableVariable, builder: ir.builder.IRBuilder):
        if first_table.n_rows != second_table.n_rows:
            raise ValueError("N rows is not equal")
        args = (
            first_table,
            NumbVariable(first_table.n_rows, builder),
            NumbVariable(second_table.n_cols, builder),
            second_table,
            NumbVariable(second_table.n_rows, builder),
            NumbVariable(second_table.n_cols, builder)
        )

    def call_print_func(self, variable: RowVariable | NumbVariable | TableVariable | ColumnVariable | StringVariable, builder: ir.builder.IRBuilder):
        if isinstance(variable, NumbVariable):
            format_string = "%.3f\n\0"
        elif isinstance(variable, StringVariable):
            format_string = "%s\n\0"
            self._functions["printf"](builder, variable)
        elif isinstance(variable, (ColumnVariable, RowVariable)):
            pass  # call __print_row_col_func
        elif isinstance(variable, TableVariable):
            pass # call __print_table_func
        c_fmt = StringVariable(format_string, builder)

        self._functions

    def call_custom_func(self, name, args):
        return_var = ...
        # call custom function
        return return_var
        
    def call_reshape_func(self, arg1: TableVariable, arg2: NumbVariable, arg3: NumbVariable):
        if not isinstance(arg1, TableVariable) and not isinstance(arg2, NumbVariable) and not isinstance(arg3, NumbVariable):
            raise ValueError(
                "Invalid arg types combination - {}, {}, {}".format(type(arg1), type(arg2), type(arg3)))
        return TableVariable(arg1.var, arg2, arg3, self.main_builder)

    def read_string(self) -> StringVariable:
        # call __read_str_func
        result = ...
        return result
    