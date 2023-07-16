from typing import Any
from llvmlite import ir


class Function:
    def __init__(self, module: ir.Module, function_type: ir.FunctionType, name: str) -> None:
        self.arg_types = function_type.args
        self.return_type = function_type.return_type
        self._function = ir.Function(
            module, 
            function_type,
            name
        )

    def __call__(self, builder: ir.builder, *args) -> Any:
        args = (arg.get_value() for arg in args)
        function_result = builder.call(self._function, args)
        builder.store()
