from llvmlite.ir import Module
from src.variables import Variable

class AssignExpressionCompiler:
    def __init__(self, module: Module) -> None:
        self._module = module

    def compile_assign_expr(self, variable: Variable, assign_sign: str, value: Variable) -> None:
        if assign_sign == '=':
            variable.set_value(value)
        elif assign_sign == '+=':
            variable.set_value(variable + value)
        elif assign_sign == '-=':
            variable.set_value(variable - value)
        elif assign_sign == '/=':
            variable.set_value(variable / value)
        elif assign_sign == '*=':
            variable.set_value(variable * value)
        else:
            raise ValueError(f"Unknown assign sign - {assign_sign}")