from typing import Any
from llvmlite import ir


class Function:
    def __init__(self, module: ir.Module, function_type: ir.FunctionType, name: str) -> None:
        self.arg_types = function_type.args
        print(self.arg_types)
        self._function = ir.Function(
            module, 
            function_type,
            name
        )

    def __call__(self, *args) -> Any:
        pass
