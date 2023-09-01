import llvmlite.ir as ir
from parser.LangParser import LangParser
from src.variables import *
from .FunctionCompiler import FunctionCompiler
from .ExpressionCompiler import ExpressionCompiler
from .AssignExpressionCompiler import AssignExpressionCompiler
from src.configs import MAX_STR_SIZE
from src.basic_types import *
import time
import os


class ProgramCompiler:
    def __init__(self) -> None:
        print("Program compilation into IR code is starting...")
        self._module = ir.Module()
        self._module.triple = "x86_64-pc-linux-gnu"
        self._builtin_funcs = {}
        self.function_compiler = FunctionCompiler(self._module)
        self.expression_compiler = ExpressionCompiler()
        self.assign_expression_compiler = AssignExpressionCompiler(self._module)
        self.local_function = None
        self._main_func = None
        self._llvm_type_to_var_type_map = {
            number: NumbVariable,
            iter: IterVariable,
            string: StringVariable
        }

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
        self._main_func = ir.Function(self._module, main_type, name='run_llvmlite_compiler')
        self._builder = ir.IRBuilder(self._main_func.append_basic_block(name='entry'))
    
    def is_main_function_started(self):
        return self._main_func is not None

    def finish_main_func(self):
        if self._builder is not None:
            self._builder.ret(ir.Constant(ir.IntType(32), 0))

    def create_var_by_type(self, type: str, value):
        if type == 'numb':
            return NumbVariable(value, self._builder)
        elif type == 'string':
            return StringVariable(value, self._builder)
        elif type == 'row':
            return RowVariable(value, 3, self._builder)
        elif type == 'column':
            return ColumnVariable(value, 3, self._builder)
        elif type == 'table':
            return TableVariable(value, 3, self._builder)
        else:
            raise ValueError("Unkown type - {}".format(type))

    def start_local_function(self, func_name: str, return_type: str, arg_types: list):
        if self.local_function is not None:
            return
        
        return_type = self.convert_type(return_type)
        converted_arg_types = tuple(map(self.convert_type, arg_types))
        
        self.function_compiler.add_function(
            self._llvm_type_to_var_type_map[return_type],
            converted_arg_types,
            func_name
        )

        self.local_function = self.function_compiler.get_function_by_name(func_name)
        self._builder = ir.builder.IRBuilder(self.local_function.get_row_function_var().append_basic_block(name='entry'))
        self.local_func_args = [self.create_var_by_type(arg_type, self.local_function.get_row_function_var().args[idx]) for idx, arg_type in enumerate(arg_types)]

    def finish_local_function(self, return_const: ir.Constant = None):
        self._builder.ret(return_const.var)
        self.local_function = None
        self._builder = None

    def _load_builtin_func(self):
        self.function_compiler.load_builtin_functions()

    def find_expression_result(self, first_variable, operation_sign: str, second_variable):
        return self.expression_compiler.process_numb_expr(first_variable, operation_sign, second_variable)
    
    def call_function(self, name: str, args: list = [], **kwargs):
        return self.function_compiler.call_function(name, args, self._builder, **kwargs)

    def create_table(self, elements, n_col, n_row):
        return TableVariable(elements, NumbVariable(n_row, self._builder), NumbVariable(n_col, self._builder), self._builder)
    
    def create_row(self, elements: list[str]):
        return RowVariable(elements, NumbVariable(len(elements), self._builder), self._builder)
    
    def create_column(self, elements: list[str]):
        return ColumnVariable(elements, NumbVariable(len(elements), self._builder), self._builder)
        
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
    
    def assign_value(self, variable: Variable, assign_sign: str, value: Variable) -> None:
        if type(variable) != type(value):
            raise TypeError("Different type of assign value")
        self.assign_expression_compiler.compile_assign_expr(variable, assign_sign, value)
