from src.NumbVariable import NumbVariable
from llvmlite import ir
from parser.LangParser import LangParser


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
    
    def process_numb_expr(self, first_var, operation_sign, second_var):
        first_operand = float(
            str(ctx.numbExpr(0).returnType().basicType().children[0]))
        second_operand = float(
            str(ctx.numbExpr(1).returnType().basicType().children[0]))
        nexpr_res = self.main_builder.fadd(
            self.numb_type(first_operand),
            self.numb_type(second_operand)
        )
        return nexpr_res
