import llvmlite.ir as ir
import llvmlite.binding as llvm
from ctypes import CFUNCTYPE
from parser.LangParser import LangParser
from src.ColumnVariable import ColumnVariable
from src.NumbVariable import NumbVariable
from src.StringVariable import StringVariable
from src.RowVariable import RowVariable, MAX_STR_SIZE
from src.TableVariable import TableVariable
import time
import os
from llvmlite import binding


class ProgramCompiler:
    def __init__(self, listener) -> None:
        print("Program translation into IR code was started...")
        self.module = ir.Module()
        self.module.triple = "x86_64-pc-linux-gnu"
        self.listener = listener
        self.numb_type = ir.DoubleType()
        self.load_builtin_funcs()
        self.start_main_func()
        self.local_builders = []
        self.local_functions = []

    def load_builtin_funcs(self):
        self.__load_print_func()
        self.__load_length_func()
        self.__load_print_row_col_func()
        self.__load_read_str_func()

    def __load_print_func(self):
        self.__print_func_arg_types = [ir.IntType(8).as_pointer()]
        printf_ty = ir.FunctionType(ir.IntType(32), self.__print_func_arg_types, var_arg=True)
        self.__print_func = ir.Function(self.module, printf_ty, name="printf")

    def __load_length_func(self):
        self.__length_func_arg_types = []
        leng_ty = ir.FunctionType(ir.IntType(32), self.__length_func_arg_types)
        self.__length_func = ir.Function(self.module, leng_ty, name='length')

    def __load_print_row_col_func(self):
        self.__print_row_col_arg_types = [ir.ArrayType(ir.IntType(8), MAX_STR_SIZE).as_pointer(), ir.IntType(32), ir.IntType(32)]
        print_row_col_ty = ir.FunctionType(
            ir.VoidType(),
            self.__print_row_col_arg_types
            )
        self.__print_row_col_func = ir.Function(self.module, print_row_col_ty, name='print_row_or_column')

    def __load_read_str_func(self):
        self.__read_str_arg_types = []
        read_str_ty = ir.FunctionType(
            StringVariable.type,
            self.__read_str_arg_types
        )
        self.__read_str_func = ir.Function(self.module, read_str_ty, name='read_string')

    def process_numb_expr(self, ctx:LangParser.NumbExprContext):
        first_operand = float(str(ctx.numbExpr(0).returnType().basicType().children[0]))
        second_operand = float(str(ctx.numbExpr(1).returnType().basicType().children[0]))
        nexpr_res = self.main_builder.fadd(
            self.numb_type(first_operand),
            self.numb_type(second_operand)
        )
        return nexpr_res

    def call_print_func(self, variable):
        if isinstance(variable, NumbVariable):
            fmt = "%.3f\n\0"
            variable_arg = variable.get_value()
        elif isinstance(variable, StringVariable):
            fmt = "%s\n\0"
            variable_arg = variable.get_value()
        elif isinstance(variable, (ColumnVariable, RowVariable)):
            arg_2 = ir.Constant(ir.IntType(32), variable.size)
            arg_3 = ir.Constant(ir.IntType(32), int(isinstance(variable, ColumnVariable)))
            f_arg = self.main_builder.bitcast(variable.ptr, self.__print_row_col_arg_types[0])
            print("!!!", self.main_builder.call(self.__print_row_col_func, [f_arg, arg_2, arg_3]))
            return
        elif isinstance(variable, str):
            fmt = "%s\n\0"
            variable += '\0'
            const_val = ir.Constant(
                ir.ArrayType(ir.IntType(8), len(variable)),
                bytearray(variable.encode('utf8'))
            )
            variable_arg = self.main_builder.alloca(const_val.type)
            self.main_builder.store(const_val, variable_arg)
        elif isinstance(variable, float):
            fmt = "%.3f\n\0"
            variable_arg = ir.Constant(ir.DoubleType(), variable)

        c_fmt = ir.Constant(ir.ArrayType(ir.IntType(8), len(fmt)),
                                bytearray(fmt.encode("utf8")))
        ptr = self.main_builder.alloca(c_fmt.type)
        self.main_builder.store(c_fmt, ptr)

        fmt_arg = self.main_builder.bitcast(ptr, *self.__print_func_arg_types)
        self.main_builder.call(self.__print_func, [fmt_arg, variable_arg])

    def __generate_random_name(self):
        import random
        import string

        rand_name = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=5))
        return rand_name

    def call_create_row_col_func(self, vars, is_col=False):
        vars = [var + '\0' + ' ' * (MAX_STR_SIZE - 1 - len(var)) for var in vars]
        if is_col:
            variable = ColumnVariable(self.__generate_random_name(), vars, self.main_builder)
        else:
            variable = RowVariable(self.__generate_random_name(), vars, self.main_builder)
        return variable



    def compile_program(self, file_name='ir_program.ll'):
        self.end_main_func()
        with open(file_name, "w") as ir_file:
            ir_file.write(str(self.module))
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
        self.main_func = ir.Function(self.module, main_type, name='run_llvmlite_compiler')
        self.main_builder = ir.IRBuilder(self.main_func.append_basic_block(name='entry'))

    def end_main_func(self):
        self.main_builder.ret(ir.Constant(ir.IntType(32), 0))

    def convert_type(self, str_type):
        if str_type == 'numb':
            return ir.DoubleType()
        elif str_type == 'string':
            return ir.IntType(8).as_pointer()
        elif str_type == 'row':
            pass
        elif str_type == 'table':
            pass
        elif str_type == 'column':
            pass

        
    def start_local_func(self, func_name, return_type, arg_types):
        print(func_name, return_type, arg_types)
        type_ = self.convert_type(return_type)
        func_type = ir.FunctionType(type_, (self.convert_type(arg_type) for arg_type in arg_types))
        self.local_function = ir.Function(self.module, func_type, name=func_name)
        self.tmp_local_builder = ir.builder.IRBuilder(function.append_basic_block(name='entry'))
        self.local_builders.append(self.tmp_local_builder)
        self.local_functions.append(self.local_function)

    def end_local_func(self, return_const:ir.Constant):
        self.tmp_local_builder.ret(return_const)
        self.tmp_local_builder = None
        self.local_function = None

    def incr_var(self, var: NumbVariable):
        temp_val = self.main_builder.load(var.ptr)
        new_val = self.main_builder.fadd(temp_val, ir.Constant(ir.DoubleType(), 1.))
        self.main_builder.store(new_val, var.ptr)
        return var

    def decr_var(self, var: NumbVariable):
        temp_val = self.main_builder.load(var.ptr)
        new_val = self.main_builder.fsub(temp_val, ir.Constant(ir.DoubleType(), 1.))
        self.main_builder.store(new_val, var.ptr)
        return var

    def read_string(self) -> StringVariable:
        var = StringVariable(self.__generate_random_name(), ' ' * (MAX_STR_SIZE - 1), self.main_builder)
        self.main_builder.store(self.main_builder.call(self.__read_str_func, []), var.ptr)
        return var
