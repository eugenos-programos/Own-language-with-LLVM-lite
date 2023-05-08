import llvmlite.ir as ir
import llvmlite.binding as llvm
from ctypes import CFUNCTYPE
from parser.LangParser import LangParser
import time
import os


class ProgramCompiler:
    def __init__(self, listener) -> None:
        print("Program translation into IR code is started...")
        self.module = ir.Module()
        self.module.triple = "x86_64-pc-linux-gnu"
        self.listener = listener
        self.numb_type = ir.DoubleType()
        self.start_main_func()

    def process_numb_expr(self, ctx:LangParser.NumbExprContext):
        first_operand = float(str(ctx.numbExpr(0).returnType().basicType().children[0]))
        second_operand = float(str(ctx.numbExpr(1).returnType().basicType().children[0]))
        nexpr_res = self.main_builder.fadd(
            self.numb_type(first_operand),
            self.numb_type(second_operand)
        )
        return nexpr_res

    def process_print_func(self, ctx:LangParser.PrintStmtContext):

        voidptr_ty = ir.IntType(8).as_pointer()

        fmt = "%f\n\0"
        c_fmt = ir.Constant(ir.ArrayType(ir.IntType(8), len(fmt)),
                            bytearray(fmt.encode("utf8")))
        global_fmt = ir.GlobalVariable(self.module, c_fmt.type, name="fstr")
        global_fmt.linkage = 'internal'
        global_fmt.global_constant = True
        global_fmt.initializer = c_fmt


        printf_ty = ir.FunctionType(ir.IntType(32), [voidptr_ty], var_arg=True)
        printf = ir.Function(self.module, printf_ty, name="printf")


        # this val can come from anywhere
        numb_expr_res = self.process_numb_expr(ctx.numbExpr(0))

        fmt_arg = self.main_builder.bitcast(global_fmt, voidptr_ty)
        self.main_builder.call(printf, [fmt_arg, numb_expr_res])


    def compile_program(self, file_name='ir_program.ll'):
        self.end_main_func()
        with open(file_name, "w") as ir_file:
            ir_file.write(str(self.module))
        print("Program translation into IR code is finished. IR file - {}".format(file_name))
        time.sleep(1)
        print("Program is converting from IR into executable file")
        os.system(f"llvm-as {file_name} -o llvmlite.bc")
        os.system(f"clang -c -emit-llvm src/main.c -o main.bc")
        os.system(f"clang llvmlite.bc main.bc -o executable")
        os.system(f"rm main.bc llvmlite.bc")



    def start_main_func(self):
        main_type = ir.FunctionType(ir.IntType(32), [])
        self.main_func = ir.Function(self.module, main_type, name='run_llvmlite_compiler')
        self.main_builder = ir.IRBuilder(self.main_func.append_basic_block(name='entry'))

    def end_main_func(self):
        self.main_builder.ret(ir.Constant(ir.IntType(32), 0))
        
