import llvmlite.ir as ir
import llvmlite.binding as llvm
from ctypes import CFUNCTYPE
from parser.LangParser import LangParser
from src.ColumnVariable import ColumnVariable
from src.NumbVariable import NumbVariable
from src.StringVariable import StringVariable
from src.RowVariable import RowVariable
from src.TableVariable import TableVariable
import time
import os


class ProgramCompiler:
    def __init__(self, listener) -> None:
        print("Program translation into IR code is started...")
        self.module = ir.Module()
        self.module.triple = "x86_64-pc-linux-gnu"
        self.listener = listener
        self.numb_type = ir.DoubleType()
        self.load_builtin_funcs()
        self.start_main_func()

    def load_builtin_funcs(self):
        self.__load_print_func()

    def __load_print_func(self):
        self.__print_func_arg_types = [ir.IntType(8).as_pointer()]
        printf_ty = ir.FunctionType(ir.IntType(32), self.__print_func_arg_types, var_arg=True)
        self.__print_func = ir.Function(self.module, printf_ty, name="printf")

    def process_numb_expr(self, ctx:LangParser.NumbExprContext):
        first_operand = float(str(ctx.numbExpr(0).returnType().basicType().children[0]))
        second_operand = float(str(ctx.numbExpr(1).returnType().basicType().children[0]))
        nexpr_res = self.main_builder.fadd(
            self.numb_type(first_operand),
            self.numb_type(second_operand)
        )
        return nexpr_res

    def call_print_func(self, value):
        if isinstance(value, NumbVariable):
            fmt = "%.3f\n\0"
            value_arg = self.main_builder.load(value.ptr)

        c_fmt = ir.Constant(ir.ArrayType(ir.IntType(8), len(fmt)),
                                bytearray(fmt.encode("utf8")))
        ptr = self.main_builder.alloca(c_fmt.type)
        self.main_builder.store(c_fmt, ptr)
        print(self.main_builder.load(ptr))

        fmt_arg = self.main_builder.bitcast(ptr, *self.__print_func_arg_types)
        self.main_builder.call(self.__print_func, [fmt_arg, value_arg])


    def compile_program(self, file_name='ir_program.ll'):
        self.end_main_func()
        with open(file_name, "w") as ir_file:
            ir_file.write(str(self.module))
        print("Program translation into IR code is finished. IR file - {}".format(file_name))
        time.sleep(1)
        print("Program is converting from IR into executable file")
        os.system(f"llvm-as {file_name} -o mylang.bc")
        os.system(f"clang -c -emit-llvm src/main.c -o main.bc")
        os.system(f"clang mylang.bc main.bc -o executable")
        os.system(f"rm main.bc mylang.bc")



    def start_main_func(self):
        main_type = ir.FunctionType(ir.IntType(32), [])
        self.main_func = ir.Function(self.module, main_type, name='run_llvmlite_compiler')
        self.main_builder = ir.IRBuilder(self.main_func.append_basic_block(name='entry'))

    def end_main_func(self):
        self.main_builder.ret(ir.Constant(ir.IntType(32), 0))
        
