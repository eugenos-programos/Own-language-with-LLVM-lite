from typing import Any
from llvmlite import ir
from src.utils import generate_random_name


class NumbVariable:
    type = ir.DoubleType()

    def __init__(self, name: str, value: float | ir.Constant, builder: ir.builder.IRBuilder) -> None:
        value = float(value) if isinstance(value, int) else value
        if isinstance(value, float):
            self.var = ir.Constant(
                self.type,
                value
            )
            self.raw_var = value
        else:
            self.var = value
            self.raw_var = value.constant
        self.name = name
        self.builder = builder
        self.compile_numb_init()

    def compile_numb_init(self):
        self.ptr = self.builder.alloca(self.type)
        self.builder.store(self.var, self.ptr)

    def get_value(self):
        value = self.builder.load(self.ptr)
        return value

    def set_value(self, value: int):
        self.var = ir.Constant(self.type, value)
        self.builder.store(self.var, self.ptr)

    def __add__(self, other_var) -> int:
        return NumbVariable(
            self.type,
            self.builder.fadd(
                self.get_value(),
                other_var.get_value()
            ),
            self.builder
        )

    def __eq__(self, other):
        return NumbVariable(
            generate_random_name(),
            ir.Constant(
                self.type,
                self.raw_var == other.raw_var
            ),
            self.builder
        )

    def __ne__(self, other):
        return NumbVariable(
            generate_random_name(),
            ir.Constant(
                self.type,
                self.raw_var != other.raw_var
            ),
            self.builder
        )

    def __sub__(self, other_var):
        return NumbVariable(
            generate_random_name(),
            self.builder.fsub(
                self.get_value(),
                other_var.get_value()
            ),
            self.builder
        )

    def __truediv__(self, other_var):
        return NumbVariable(
            generate_random_name(),
            self.builder.fdiv(
                self.get_value(),
                other_var.get_value()
            ),
            self.builder
        )

    def __floordiv__(self, other_var):
        var1 = self.get_value(),
        var2 = other_var.get_value()
        return NumbVariable(
            generate_random_name(),
            self.builder.fsub(
                self.builder.fdiv(var1.get_value(), var2),
                self.builder.frem(var1, var2)
            ),
            self.builder
        )

    def __mul__(self, other_var):
        return NumbVariable(
            generate_random_name(),
            self.builder.fmul(
                self.get_value(),
                other_var.get_value()
            ),
            self.builder
        )
