import llvmlite.ir as ir
from parser.LangParser import LangParser
from src.variables import *
from src.FunctionCompiler import FunctionCompiler
from src.ExpressionCompiler import ExpressionCompiler
from src.configs import MAX_STR_SIZE
from src.basic_types import *
import time
import os


class LLVMCompiler:
    def __init__(self) -> None:
        print("Program compilation into IR code is starting...")
        self._module = ir.Module()
        self._module.triple = "x86_64-pc-linux-gnu"
        self._builtin_funcs = {}
        self.function_compiler = FunctionCompiler(self._module)
        self.expression_compiler = ExpressionCompiler()
        self.local_function = None
        self._main_func = None

    def finish_compiling(self, file_name='ir_program.ll'):
        self.finish_main_func()
        print(str(self._module))
        with open(file_name, "w") as ir_file:
            ir_file.write(str(self._module))
        print("Program translation into IR code is finished. IR file - {}".format(file_name))
        time.sleep(1)
        print("Program is converting from IR into executable file")
        os.system(f"llvm-as {file_name} -o mylang.bc")
        os.system(f"clang -c -emit-llvm src/main.c -o main.bc")
        os.system(f"clang -c -emit-llvm src/func_utilities.c -o func_utilities.bc")
        os.system(f"clang mylang.bc main.bc func_utilities.bc -o executable")
        os.system(f"rm main.bc mylang.bc func_utilities.bc")

    def start_main_func(self):
        main_type = ir.FunctionType(ir.IntType(32), [])
        self._main_func = ir.Function(
            self._module, main_type, name='run_llvmlite_compiler')
        self._builder = ir.IRBuilder(
            self._main_func.append_basic_block(name='entry'))
    
    def is_main_function_started(self):
        return self._main_func is not None

    def finish_main_func(self):
        if self._builder is not None:
            self._builder.ret(ir.Constant(ir.IntType(32), 0))

    def start_local_function(self, func_name, return_type, arg_types):
        if self.local_function is not None:
            return
        type_ = self.convert_type(return_type)
        converted_types = [self.convert_type(
            arg_type) for arg_type in arg_types]
        func_type = ir.FunctionType(
            type_, converted_types)
        self.local_function = ir.Function(
            self.module, func_type, name=func_name)
        self._builder = ir.builder.IRBuilder(
            self.local_function.append_basic_block(name='entry'))
        self.builtin_funcs[func_name] = (
            self.local_function, return_type, arg_types)
        self.local_func_args = [self.create_var_by_type(
            arg_type) for arg_type in arg_types]

    def finish_local_function(self, return_const: ir.Constant = None):
        self._builder.ret(return_const.var)
        self.local_function = None
        self._builder = None

    def _load_builtin_func(self):
        self.function_compiler.load_builtin_functions()

    def process_numb_expr(self, ctx: LangParser.NumbExprContext):
        first_operand = float(
            str(ctx.numbExpr(0).returnType().basicType().children[0]))
        second_operand = float(
            str(ctx.numbExpr(1).returnType().basicType().children[0]))
        nexpr_res = self._builder.fadd(
            self.numb_type(first_operand),
            self.numb_type(second_operand)
        )
        return nexpr_res
    
    def call_function(self, name: str, args: list = []):
        return self.function_compiler.call_function(name, args, self._builder)

    def create_empty_var_by_type(self, type: ir.Type):
        if type == 'numb':
            return NumbVariable(1, self._builder)
        elif type == 'string':
            return StringVariable("", self._builder)
        elif type == 'row':
            return RowVariable([], self._builder)
        elif type == 'column':
            return ColumnVariable([], self._builder)
        elif type == 'table':
            return TableVariable([], self._builder)
        else:
            raise ValueError("Unkown type - {}".format(type))

    def create_table(self, vars, n_col, n_row):
        vars = [var + '\0' + ' ' * (MAX_STR_SIZE - 1 - len(var))
                for var in vars]
        if n_col * n_row != vars:
            while len(vars) != n_col * n_row:
                vars.append(" " * (MAX_STR_SIZE - 1) + '\0')
        return TableVariable(vars, n_col, n_row, self._builder)
        
    def convert_type(self, type: str) -> ir.Type:
        result_type = None
        match type:
            case "numb":
                result_type = number
            case "string":
                result_type = string
            case "iter"|"row"|"table"|"column":
                result_type = iter
            case "void":
                result_type = number
            case "int":
                result_type = i8
            case _:
                raise ValueError("Unknown type - {}".format(type))
        return result_type
