import llvmlite.ir as ir
from parser.LangParser import LangParser
from src.ColumnVariable import ColumnVariable
from src.NumbVariable import NumbVariable
from src.StringVariable import StringVariable
from src.RowVariable import RowVariable, MAX_STR_SIZE
from src.TableVariable import TableVariable
import time
import os
from src.utils import generate_random_name


class ProgramCompiler:
    def __init__(self, listener) -> None:
        print("Program translation into IR code was started...")
        self.module = ir.Module()
        self.module.triple = "x86_64-pc-linux-gnu"
        self.listener = listener
        self.numb_type = ir.DoubleType()
        self.load_builtin_funcs()
        self.local_builders = []
        self.local_functions = []
        self.loc_funcs = {}
        self.local_function = None
        self.main_func = None

    def load_builtin_funcs(self):
        self.__load_print_func()
        self.__load_length_func()
        self.__load_print_row_col_func()
        self.__load_read_str_func()
        self.__load_print_tabl_func()

    def __load_print_func(self):
        self.__print_func_arg_types = [ir.IntType(8).as_pointer()]
        printf_ty = ir.FunctionType(ir.IntType(
            32), self.__print_func_arg_types, var_arg=True)
        self.__print_func = ir.Function(self.module, printf_ty, name="printf")

    def __load_length_func(self):
        self.__length_func_arg_types = []
        leng_ty = ir.FunctionType(ir.IntType(32), self.__length_func_arg_types)
        self.__length_func = ir.Function(self.module, leng_ty, name='length')

    def __load_print_row_col_func(self):
        self.__print_row_col_arg_types = [ir.ArrayType(ir.IntType(
            8), MAX_STR_SIZE).as_pointer(), ir.IntType(32), ir.IntType(32)]
        print_row_col_ty = ir.FunctionType(
            ir.VoidType(),
            self.__print_row_col_arg_types
        )
        self.__print_row_col_func = ir.Function(
            self.module, print_row_col_ty, name='print_row_or_column')

    def __load_read_str_func(self):
        self.__read_str_arg_types = []
        read_str_ty = ir.FunctionType(
            StringVariable.type,
            self.__read_str_arg_types
        )
        self.__read_str_func = ir.Function(
            self.module, read_str_ty, name='read_string')

    def __load_print_tabl_func(self):
        self.__print_tabl_arg_types = [
            ir.ArrayType(ir.IntType(8), MAX_STR_SIZE).as_pointer(),
            ir.IntType(32),
            ir.IntType(32)
        ]
        print_row_col_ty = ir.FunctionType(
            ir.VoidType(),
            self.__print_row_col_arg_types
        )
        self.__print_table_func = ir.Function(
            self.module, print_row_col_ty, name='print_table')

    def process_numb_expr(self, ctx: LangParser.NumbExprContext):
        first_operand = float(
            str(ctx.numbExpr(0).returnType().basicType().children[0]))
        second_operand = float(
            str(ctx.numbExpr(1).returnType().basicType().children[0]))
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
            arg_3 = ir.Constant(ir.IntType(32), int(
                isinstance(variable, ColumnVariable)))
            f_arg = self.main_builder.bitcast(
                variable.ptr, self.__print_row_col_arg_types[0])
            self.main_builder.call(self.__print_row_col_func, [
                                   f_arg, arg_2, arg_3])
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
        elif isinstance(variable, TableVariable):
            n_r = ir.Constant(ir.IntType(32), variable.n_rows)
            n_c = ir.Constant(ir.IntType(32), variable.n_cols)
            tabl = self.main_builder.bitcast(
                variable.ptr, self.__print_tabl_arg_types[0])
            self.main_builder.call(self.__print_table_func, [tabl, n_r, n_c])
            return
        c_fmt = ir.Constant(ir.ArrayType(ir.IntType(8), len(fmt)),
                            bytearray(fmt.encode("utf8")))
        ptr = self.main_builder.alloca(c_fmt.type)
        self.main_builder.store(c_fmt, ptr)

        fmt_arg = self.main_builder.bitcast(ptr, *self.__print_func_arg_types)
        self.main_builder.call(self.__print_func, [fmt_arg, variable_arg])

    def call_create_row_col_func(self, vars, is_col=False):
        vars = [var + '\0' + ' ' * (MAX_STR_SIZE - 1 - len(var))
                for var in vars]
        if is_col:
            variable = ColumnVariable(
                generate_random_name(), vars, self.main_builder)
        else:
            variable = RowVariable(
                generate_random_name(), vars, self.main_builder)
        return variable

    def create_var_by_type(self, type):
        name = generate_random_name()
        if type == 'numb':
            return NumbVariable(name, 1, self.main_builder)
        elif type == 'string':
            return StringVariable(name, "", self.main_builder)
        elif type == 'row':
            return RowVariable(name, [], self.main_builder)
        elif type == 'column':
            return ColumnVariable(name, [], self.main_builder)
        elif type == 'table':
            return TableVariable(name, [], self.main_builder)
        else:
            raise ValueError("Unkown type - {}".format(type))

    def call_custom_func(self, name, args):
        func, return_type, arg_types = self.loc_funcs.get(name)

        return_var = self.create_var_by_type(return_type)
        self.main_builder.bitcast(return_var.ptr, func.type)

        args = [self.main_builder.bitcast(
            arg.ptr, self.convert_type(arg_types[arg_idx])) for arg_idx, arg in enumerate(args)]

        func_res = self.main_builder.call(func, args)
        self.main_builder.store(func_res, return_var.ptr)
        return return_var

    def create_table(self, vars, n_col, n_row):
        vars = [var + '\0' + ' ' * (MAX_STR_SIZE - 1 - len(var))
                for var in vars]
        if n_col * n_row != vars:
            while len(vars) != n_col * n_row:
                vars.append(" " * (MAX_STR_SIZE - 1) + '\0')
        return TableVariable(generate_random_name(), vars, n_col, n_row, self.main_builder)

    def call_reshape_func(self, arg1: TableVariable, arg2: NumbVariable, arg3: NumbVariable):
        if not isinstance(arg1, TableVariable) and not isinstance(arg2, NumbVariable) and not isinstance(arg3, NumbVariable):
            raise ValueError(
                "Invalid arg types combination - {}, {}, {}".format(type(arg1), type(arg2), type(arg3)))
        return TableVariable(generate_random_name(), arg1.var, arg2, arg3, self.main_builder)

    def compile_program(self, file_name='ir_program.ll'):
        self.end_main_func()
        print(str(self.module))
        with open(file_name, "w") as ir_file:
            ir_file.write(str(self.module))
        print(
            "Program translation into IR code is finished. IR file - {}".format(file_name))
        time.sleep(1)
        print("Program is converting from IR into executable file")
        os.system(f"llvm-as {file_name} -o mylang.bc")
        os.system(f"clang -c -emit-llvm src/main.c -o main.bc")
        os.system(f"clang -c -emit-llvm src/func_utilities.c -o func_utilities.bc")
        os.system(f"clang mylang.bc main.bc func_utilities.bc -o executable")
        os.system(f"rm main.bc mylang.bc func_utilities.bc")

    def start_main_func(self):
        main_type = ir.FunctionType(ir.IntType(32), [])
        self.main_func = ir.Function(
            self.module, main_type, name='run_llvmlite_compiler')
        self.main_builder = ir.IRBuilder(
            self.main_func.append_basic_block(name='entry'))

    def end_main_func(self):
        if self.main_builder is not None:
            self.main_builder.ret(ir.Constant(ir.IntType(32), 0))

    def convert_type(self, str_type):
        if str_type == 'numb':
            return ir.DoubleType()
        elif str_type == 'string':
            return ir.IntType(8).as_pointer()
        elif str_type == 'row':
            return ir.ArrayType(ir.IntType(8), MAX_STR_SIZE).as_pointer()
        elif str_type == 'table':
            return ir.ArrayType(ir.IntType(8), MAX_STR_SIZE).as_pointer()
        elif str_type == 'column':
            return ir.ArrayType(ir.IntType(8), MAX_STR_SIZE).as_pointer()
        elif str_type == 'void':
            return ir.DoubleType()

    def start_local_func(self, func_name, return_type, arg_types):
        if self.local_function is not None:
            return
        type_ = self.convert_type(return_type)
        converted_types = [self.convert_type(
            arg_type) for arg_type in arg_types]
        func_type = ir.FunctionType(
            type_, converted_types)
        self.local_function = ir.Function(
            self.module, func_type, name=func_name)
        self.main_builder = ir.builder.IRBuilder(
            self.local_function.append_basic_block(name='entry'))
        self.loc_funcs[func_name] = (
            self.local_function, return_type, arg_types)
        self.local_func_args = [self.create_var_by_type(
            arg_type) for arg_type in arg_types]

    def end_local_func(self, return_const: ir.Constant = None):
        print(self.main_builder)
        print(self.local_function)
        if return_const is None:
            self.main_builder.ret(ir.Constant(ir.DoubleType(), 0.0))
        else:
            self.main_builder.ret(return_const.var)
        self.local_function = None
        self.main_builder = None

    def incr_var(self, var: NumbVariable):
        temp_val = self.main_builder.load(var.ptr)
        new_val = self.main_builder.fadd(
            temp_val, ir.Constant(ir.DoubleType(), 1.))
        self.main_builder.store(new_val, var.ptr)
        return var

    def decr_var(self, var: NumbVariable):
        temp_val = self.main_builder.load(var.ptr)
        new_val = self.main_builder.fsub(
            temp_val, ir.Constant(ir.DoubleType(), 1.))
        self.main_builder.store(new_val, var.ptr)
        return var

    def read_string(self) -> StringVariable:
        var = StringVariable(generate_random_name(), ' ' *
                             (MAX_STR_SIZE - 1), self.main_builder)
        self.main_builder.store(self.main_builder.call(
            self.__read_str_func, []), var.ptr)
        return var

    def del_el(self, obj_: RowVariable | ColumnVariable, el: str):
        if isinstance(el, int):
            el = str(el)
