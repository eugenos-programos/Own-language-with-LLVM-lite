from src.NumbVariable import NumbVariable
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
