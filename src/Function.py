from typing import Any
from llvmlite import ir


class Function:
    def __init__(self, module: ir.Module, function_type: ir.FunctionType, name: str) -> None:
        self._function = ir.Function(
            module, 
            function_type,
            name
        )

    def __call__(self, *args) -> Any:
        pass
