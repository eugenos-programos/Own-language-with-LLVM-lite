import llvmlite.ir as ir
from parser.LangParser import LangParser
from src.ColumnVariable import ColumnVariable
from src.NumbVariable import NumbVariable
from src.StringVariable import StringVariable
from src.RowVariable import RowVariable
from src.TableVariable import TableVariable
from src.FunctionCompiler import FunctionCompiler
from src.configs import MAX_STR_SIZE
import time
import os


class LLVMCompiler:
    def __init__(self, function_compiler: FunctionCompiler) -> None:
        print("Program compilation into IR code is starting...")
        self._module = ir.Module()
        self._module.triple = "x86_64-pc-linux-gnu"
        self._builtin_funcs = {}
        self.function_compiler = function_compiler

        self._load_builtin_funcs()

    def _load_builtin_func(self):
        self.function_compiler



