from llvmlite import ir
from src.configs import MAX_STR_SIZE


i8 = ir.IntType(8)
i32 = ir.IntType(32)
array = ir.ArrayType

void = ir.VoidType()
string = i8.as_pointer()
iter = i8.as_pointer().as_pointer()
number = ir.DoubleType()
