from llvmlite.ir import Module
from llvmlite import ir
from src.basic_types import *
from src.configs import MAX_STR_SIZE
from src.Function import Function


class FunctionCompiler:

    def __init__(self, module) -> None:
        self.module = module
        self._functions = {}

    def load_builtin_functions(self):
        function_parameters = [
            [i32, [i8.as_pointer()], "printf", True],
            [i32, [], "length", False],
            [void, [array(i8, MAX_STR_SIZE).as_pointer(), i32, i32], "print_row_or_column", ]
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

