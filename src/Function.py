from typing import Any, Sequence, Union
from llvmlite import ir
from src.variables import *


class Function:
    def __init__(self, module: ir.Module, function_type: ir.FunctionType, name: str, return_var_type: Variable | Sequence[Variable]) -> None:
        self.arg_types = function_type.args
        self._return_type = return_var_type
        self.type = function_type
        self._function = ir.Function(
            module, 
            function_type,
            name
        )
        self._is_convert_func = "toDynamic" in name   # if function is used for dynamic converting -> return raw alloca inst

    def _save_function_result(self, func_res: ir.AllocaInstr, builder: ir.builder, result_size: int | tuple, first_arg_type: Variable) -> Variable | ir.AllocaInstr:
        if self._is_convert_func:
            return func_res
        if self._return_type == VoidVariable:
            return None
        elif self._return_type == StringVariable:
            return StringVariable(func_res, builder)
        elif self._return_type == TableVariable:
            return TableVariable(func_res, *result_size, builder)
        elif self._return_type == IterVariable:
            return IterVariable(func_res, result_size, builder)
        elif self._return_type == NumbVariable:
            return NumbVariable(func_res, builder)
        elif isinstance(self._return_type, list):
            if first_arg_type not in [RowVariable, ColumnVariable, TableVariable]:
                raise ValueError(f"Arg type - {first_arg_type}")
            if first_arg_type in [RowVariable, ColumnVariable]:
                return first_arg_type(func_res, result_size, builder)
            else:
                return first_arg_type(func_res, *result_size, builder)
        else:
            raise TypeError(f"Uknown return type - {self._return_type}")


    def __call__(self, builder: ir.builder, *args, **kwargs) -> Any:
        raw_args = [arg.get_value() for arg in args]
        function_result = builder.call(self._function, raw_args)
        return_type_opt = type(args[0]) if args else None
        return self._save_function_result(function_result, builder, kwargs.get("result_size"), return_type_opt)
