from llvmlite.ir import Module
from llvmlite import ir
from src.basic_types import *
from src.configs import MAX_STR_SIZE, MAX_ARR_SIZE
from src.Function import Function
from src.variables import *


class FunctionCompiler:

    def __init__(self, module) -> None:
        self.module = module
        self._functions = {}
        self._load_builtin_functions()
        self._call_function_map = {
            "print": self.call_print_func,
            "length": self.call_length_func,
        }

    def _load_builtin_functions(self):
        function_parameters = [
            [VoidVariable, [string], "printf", True],
            [NumbVariable, [], "length", False],
            [VoidVariable, [iter, number, number], "print_row_or_column", False],
            [StringVariable, [], "read_string", False],
            [VoidVariable, [iter, number, number], "print_table", False],
            [TableVariable, [iter, number, number, iter, number, number], "mul_tables", False],
            [None, [number, ir.ArrayType(ir.ArrayType(i8, MAX_STR_SIZE), MAX_ARR_SIZE)], "toDynamic2", False]
        ]
        for func_params in function_parameters:
            self._save_func_to_dict(*func_params)

    def _save_func_to_dict(self, return_type: ir.Type, arg_types: list, name: str, var_arg: bool = False):
        function = Function(self.module,
            ir.FunctionType(
                return_type.basic_type if not return_type is None else ir.ArrayType(ir.ArrayType(i8, MAX_STR_SIZE), MAX_ARR_SIZE),
                arg_types,
                var_arg=var_arg
            ),
            name,
            return_type
        )
        self._functions[name] = function

    def get_function_by_name(self, name: str) -> ir.Function:
        return self._functions.get(name)

    def call_function(self, name: str, args: list, builder: ir.builder.IRBuilder):
        call_function_var = self._call_function_map[name] if self._call_function_map.get(name) is not None \
                                                          else self._functions[name]
        return call_function_var(builder, *args)

    def call_mult_tables_function(self, builder: ir.builder.IRBuilder, first_table: TableVariable, second_table: TableVariable):
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

    def call_print_func(self, builder: ir.builder.IRBuilder, variable: RowVariable | NumbVariable | TableVariable | ColumnVariable | StringVariable) -> VoidVariable:
        if isinstance(variable, NumbVariable):
            format_string = StringVariable("%.3f\n\0", builder)
            return self._functions["printf"](builder, format_string, variable)
        elif isinstance(variable, StringVariable):
            format_string = StringVariable("%s\n\0", builder)
            return self._functions["printf"](builder, format_string, variable)
        elif isinstance(variable, (ColumnVariable, RowVariable)):
            is_column = NumbVariable(1, builder) if isinstance(variable, ColumnVariable) else NumbVariable(0, builder)
            return self._functions["print_row_or_column"](builder, variable, variable.size, is_column)
        elif isinstance(variable, TableVariable):
            return self._functions["print_table"](builder, variable, variable.n_rows, variable.n_cols)

    def call_length_func(self, builder: ir.builder.IRBuilder, variable: IterVariable) -> NumbVariable:
        return variable.size
        
    def call_reshape_func(self, arg1: TableVariable, arg2: NumbVariable, arg3: NumbVariable):
        if not isinstance(arg1, TableVariable) and not isinstance(arg2, NumbVariable) and not isinstance(arg3, NumbVariable):
            raise ValueError("Invalid arg types combination - {}, {}, {}".format(type(arg1), type(arg2), type(arg3)))
        return TableVariable(arg1.var, arg2, arg3, self.main_builder)
    