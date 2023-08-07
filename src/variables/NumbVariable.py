from llvmlite import ir
from .Variable import Variable


class NumbVariable(Variable):
    basic_type = ir.DoubleType()

    def __init__(self, value: float | Variable | ir.instructions.Instruction, builder: ir.builder.IRBuilder) -> None:
        self.builder = builder
        value = float(value) if isinstance(value, int) else value
        if isinstance(value, float):
            self.var = ir.Constant(
                self.basic_type,
                value
            )
        elif isinstance(value, ir.instructions.Instruction):
            self.var = value
        else:
            self.var = self.builder.load(value.ptr)
        self.ptr = self.builder.alloca(self.basic_type)
        self.builder.store(self.var, self.ptr)

    def get_value(self):
        return self.builder.load(self.ptr)

    def copy_variable(self, builder: ir.builder.IRBuilder):
        return NumbVariable(self, builder) 

    def set_value(self, other_variable):
        self.var = ir.Constant(self.type, value)
        self.builder.store(self.var, self.ptr)

    def __add__(self, other_var) -> int:
        return NumbVariable(
            self.builder.fadd(
                self.get_value(),
                other_var.get_value()
            ),
            self.builder
        )

    def __eq__(self, other):
        return NumbVariable(
            ir.Constant(
                self.basic_type,
                self.raw_var == other.raw_var
            ),
            self.builder
        )

    def __ne__(self, other):
        return NumbVariable(
            ir.Constant(
                self.basic_type,
                self.raw_var != other.raw_var
            ),
            self.builder
        )

    def __sub__(self, other_var):
        return NumbVariable(
            self.builder.fsub(
                self.get_value(),
                other_var.get_value()
            ),
            self.builder
        )

    def __truediv__(self, other_var):
        return NumbVariable(
            self.builder.fdiv(
                self.get_value(),
                other_var.get_value()
            ),
            self.builder
        )

    def __floordiv__(self, other_var):
        var1 = self.get_value()
        var2 = other_var.get_value()
        return NumbVariable(
            self.builder.frem(
                var1,
                var2
            ),
            self.builder
        )

    def __mul__(self, other_var):
        return NumbVariable(
            self.builder.fmul(
                self.get_value(),
                other_var.get_value()
            ),
            self.builder
        )
