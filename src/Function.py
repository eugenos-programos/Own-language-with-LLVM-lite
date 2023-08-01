from typing import Any
from llvmlite import ir
from src.variables import *


class Function:
    def __init__(self, module: ir.Module, function_type: ir.FunctionType, name: str, return_var_type: Variable) -> None:
        self.arg_types = function_type.args
        self._return_type = return_var_type
        self.type = function_type
        self._function = ir.Function(
            module, 
            function_type,
            name
        )
        print(name)
        self._is_convert_func = "toDynamic" in name

    def _save_function_result(self, func_res: ir.AllocaInstr, builder: ir.builder, result_size: int) -> Variable | ir.AllocaInstr:
        if self._is_convert_func:
            return func_res
        if self._return_type == VoidVariable:
            return None
        elif self._return_type == StringVariable:
            return StringVariable(func_res, builder)
        elif self._return_type == TableVariable:
            return TableVariable(func_res)
        elif self._return_type == IterVariable:
            return IterVariable(func_res, result_size, builder)

    def __call__(self, builder: ir.builder, *args, **kwargs) -> Any:
        args = [arg.get_value() for arg in args]
        function_result = builder.call(self._function, args)
        return self._save_function_result(function_result, builder, kwargs.get("result_size"))
