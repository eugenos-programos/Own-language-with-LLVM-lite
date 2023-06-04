from llvmlite import ir
from src.configs import MAX_STR_SIZE


class IterVariable:
    def __init__(self, elements: tuple = None, size: int = None, builder: ir.builder.IRBuilder = None, ptr=None) -> None:
        self.builder = builder
        self.size = size

        if ptr is not None:
            self.ptr = ptr
            self.var = self.builder.load(self.ptr)
        else:
            cvars = [ir.Constant(ir.ArrayType(ir.IntType(8), MAX_STR_SIZE), bytearray(
                var, 'utf-8')) for var in elements]
            self.type = ir.ArrayType(ir.ArrayType(
                ir.IntType(8), MAX_STR_SIZE), size)
            self.var = ir.Constant(self.type, cvars)
            self.ptr = self.builder.alloca(self.type)
            self.builder.store(self.var, self.ptr)
            self.ptr = self.builder.bitcast(self.ptr, ir.PointerType(
                ir.PointerType(ir.IntType(8))))

    def compile_init(self):
        self.ptr = self.builder.alloca(self.type)
        self.builder.store(self.var, self.ptr)
