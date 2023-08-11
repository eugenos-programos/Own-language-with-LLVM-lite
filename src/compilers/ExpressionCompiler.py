from src.variables import NumbVariable, Variable
from llvmlite import ir


class ExpressionCompiler:

    def __init__(self) -> None:
        pass

    def increment_variable(self, var: NumbVariable, builder: ir.builder.IRBuilder):
        temp_val = builder.load(var.ptr)
        new_val = builder.fadd(temp_val, ir.Constant(ir.DoubleType(), 1.))
        builder.store(new_val, var.ptr)
        return var

    def decrement_variable(self, var: NumbVariable, builder: ir.builder.IRBuilder):
        temp_val = builder.load(var.ptr)
        new_val = builder.fsub(temp_val, ir.Constant(ir.DoubleType(), 1.))
        builder.store(new_val, var.ptr)
        return var
    
    def process_numb_expr(self, first_var: Variable, operation_sign: str, second_var: Variable):
        if isinstance(first_var, NumbVariable) and isinstance(second_var, NumbVariable):
            if operation_sign == '+':
                return first_var + second_var
            elif operation_sign == '-':
                return first_var - second_var
            elif operation_sign == '/':
                return first_var / second_var
            elif operation_sign == '//':
                return first_var // second_var
            elif operation_sign == '*':
                return first_var * second_var
            elif operation_sign == '==':
                return first_var == second_var
            elif operation_sign == '!=':
                return first_var != second_var

        raise ValueError(f"Uknown operation operands and sign - {first_var}, {operation_sign}, {second_var}")
