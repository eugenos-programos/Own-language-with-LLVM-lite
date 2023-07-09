import llvmlite.ir as ir
from parser.LangParser import LangParser
from src.ColumnVariable import ColumnVariable
from src.NumbVariable import NumbVariable
from src.StringVariable import StringVariable
from src.RowVariable import RowVariable
from src.TableVariable import TableVariable
from src.configs import MAX_STR_SIZE
import time
import os


class ProgramCompiler:
    def __init__(self, listener) -> None:
        print("Program translation into IR code started...")
        self.module = ir.Module()
        self.module.triple = "x86_64-pc-linux-gnu"
        self.listener = listener
        self.numb_type = ir.DoubleType()
        self.builtin_funcs = {}

        self.load_builtin_funcs()
        self.local_builders = []
        self.local_function = None
        self.main_func = None
        TableVariable.builtin_functions = self.builtin_funcs

    def call_mult_tables(self, table_1, table_2):
        if table_1.n_rows != table_2.n_rows:
            raise ValueError("N ROWS error")
        self.cast_iter_to_ptr(table_2)
        args = [
            table_1.ptr,
            ir.Constant(ir.IntType(8), table_1.n_rows),
            ir.Constant(ir.IntType(8), table_1.n_cols),
            table_2.ptr,
            ir.Constant(ir.IntType(8), table_2.n_rows),
            ir.Constant(ir.IntType(8), table_2.n_cols)
        ]
        func, return_type, args_types = self.builtin_funcs.get("mul_tables")

        ptr_res = self.main_builder.alloca(return_type)
        res = self.main_builder.call(func, args)
        self.main_builder.store(
            res,
            ptr_res
        )
        return TableVariable(n_cols=table_1.n_cols + table_2.n_cols, n_rows=table_1.n_rows, builder=self.main_builder, ptr=ptr_res)

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
            variable = ColumnVariable(vars, self.main_builder)
        else:
            variable = RowVariable(vars, self.main_builder)
        return variable

    def call_custom_func(self, name, args):
        func, return_type, arg_types = self.builtin_funcs.get(name)

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
        return TableVariable(vars, n_col, n_row, self.main_builder)

    def call_reshape_func(self, arg1: TableVariable, arg2: NumbVariable, arg3: NumbVariable):
        if not isinstance(arg1, TableVariable) and not isinstance(arg2, NumbVariable) and not isinstance(arg3, NumbVariable):
            raise ValueError(
                "Invalid arg types combination - {}, {}, {}".format(type(arg1), type(arg2), type(arg3)))
        return TableVariable(arg1.var, arg2, arg3, self.main_builder)


    def read_string(self) -> StringVariable:
        var = StringVariable(' ' *
                             (MAX_STR_SIZE - 1), self.main_builder)
        self.main_builder.store(self.main_builder.call(
            self.__read_str_func, []), var.ptr)
        return var

