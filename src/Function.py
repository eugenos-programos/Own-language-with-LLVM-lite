from typing import Any
from llvmlite import ir
from src.variables import *


class Function:
    def __init__(self, module: ir.Module, function_type: ir.FunctionType, name: str, return_var_type) -> None:
        self.arg_types = function_type.args
        self._return_type = return_var_type
        self._function = ir.Function(
            module, 
            function_type,
            name
        )

    def _save_function_result(self, func_res: ir.AllocaInstr, builder: ir.builder):
        if self._return_type == VoidVariable:
            return None
        elif self._return_type == StringVariable:
            var = StringVariable(func_res, builder)
            return var
        return self._return_type(func_res, builder)

    def __call__(self, builder: ir.builder, *args) -> Any:
        args = [arg.get_value() for arg in args]
        function_result = builder.call(self._function, args)
        return self._save_function_result(function_result, builder)
