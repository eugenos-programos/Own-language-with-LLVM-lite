# Generated from LangParser.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .LangParser import LangParser
else:
    from LangParser import LangParser
from src.llvm_compile import *


class SemanticAnalyzerException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


def get_dict(params : list, out_type : str, func_local_vars : list = None):
    if func_local_vars is None:
        return {"params": params, "return_type": out_type}
    return {"params": params, "return_type": out_type, "local_vars": func_local_vars}

# This class defines a complete listener for a parse tree produced by LangParser.
class LangParserListener(ParseTreeListener):

    global_vars = {}
    function_vars = {
        # built-in functions 
        # output is a number == it depends on {number} param 
        "print": get_dict(["table/row/column/string/numb"], "void"),
        "length": get_dict(["table/row/column/string"], "numb"),
        "reshape": get_dict(["table", "numb", "numb"], "table"),
        "del_col": get_dict(["table", "numb"], "table"),
        "del_row": get_dict(["table", "numb"], "table"),
        "del": get_dict(["row/column", "numb"], "0"),
        "insert": get_dict(["column/row", "string/numb", "numb"], "0"), 
        "max": get_dict(["table/row/column"], "numb"),
        "min": get_dict(["table/row/column"], "numb"),
        "maxlen": get_dict(["table/row/column"], "string"),
        "minlen": get_dict(["table/row/column"], "string"),
        "find": get_dict(["table/row/column", "string/numb"], "numb"),
        "create_row": get_dict(["numb", "list"], "row"),
        "create_table": get_dict(["numb", "list"], "table"),
        "create_column": get_dict(["numb", "numb", "list"], "column"),
        "read_string": get_dict([], "string"),
        "copy": get_dict(["table/row/column/string/numb"], "0")
    }

    available_operands = {
        # bool operators
        "==": ("numb", "string", "column", "row", "table"),
        "!=": ("numb", "string", "column", "row", "table"),
        "<=": ("numb", "string", "column", "row"),
        ">=": ("numb", "string", "column", "row"),
        "<": ("numb", "string", "column", "row"),
        ">": ("numb", "string", "column", "row"),
        "&": ("numb"),
        "|": ("numb"),
        "!": ("numb"),
        # number operators
        "+": ("numb", "string", "column", "row", "table"),
        "-": ("numb"),
        "/": ("numb", "column", "row", "table"),
        "//": ("numb", "table"),
        "*": ("numb", "table")
    }

    # Enter a parse tree produced by LangParser#program.
    def enterProgram(self, ctx:LangParser.ProgramContext):
        # function vars 
        self.is_func_init = False
        self.local_func_vars = {}
        self.local_func_params = {}
        self.local_func_name = None
        # for vars 
        self.all_for_vars = {}
        self.for_stat_init = False
        # while vars
        self.local_while_vars = {}
        # until vars
        self.local_until_vars = {}
        # if else vars
        self.local_ifels_vars = {}

        # init program compiler
        self.program_compiler = ProgramCompiler(self)


    # Exit a parse tree produced by LangParser#program.
    def exitProgram(self, ctx:LangParser.ProgramContext):
        #print(self.function_vars)
        #print(self.global_vars)
        self.program_compiler.compile_program()


    # Enter a parse tree produced by LangParser#func.
    def enterFunc(self, ctx:LangParser.FuncContext):
        self.is_func_return_smth = False

    def clear_func_cache(self):
        if self.is_func_init:
            self.function_vars.pop(self.local_func_name)
        for key in self.local_func_vars:
            self.global_vars.pop(key)

    # Exit a parse tree produced by LangParser#func.
    def exitFunc(self, ctx:LangParser.FuncContext):
        if not self.is_func_init:
            self.checkAndInitUserFunc(ctx)
        if not self.is_func_return_smth and self.local_func_params.get('return_type') != 'void':
            raise SemanticAnalyzerException(f"Function doesn't return {self.local_func_params.get('return_type')} value.")
        if self.is_func_return_smth and self.local_func_params.get('return_type') == 'void':
            raise SemanticAnalyzerException(f"Void function returns value")
        for func_param in self.local_func_vars:
            self.global_vars.pop(func_param)
        self.is_func_init = False

    def checkAndInitUserFunc(self, ctx:LangParser.FuncContext):
        func_type = str(ctx.children[0].children[0]) if str(ctx.children[0]) != 'void' else 'void'
        func_name = str(ctx.ID(0))
        self.local_func_name = func_name

        func_params = list(map(str, ctx.ID()[1:]))
        func_params_types = list(map(lambda ctx: str(ctx.children[0]), ctx.basicTypeName()[int(func_type != 'void'):]))

        if self.function_vars.get(func_name) is not None and self.function_vars.get(func_name).get("params") == func_params_types and\
            func_type == self.function_vars.get(func_name).get("return_type"): 
            raise SemanticAnalyzerException(f"Function {func_name} with such params is already defined")

        if len(func_params) != len(func_params_types):
            raise SemanticAnalyzerException("Check params number and number of their types")
        
        for func_index, func_param in enumerate(func_params):
            if self.local_func_vars.get(func_param) is not None:
                raise SemanticAnalyzerException(f"Function parameter {func_param} is already defined")
            self.local_func_vars[func_param] = func_params_types[func_index]
            self.addNewVariable(func_param, func_params_types[func_index], False)

        self.function_vars[func_name] = self.local_func_params = get_dict(func_params_types, func_type, func_params)
        self.is_func_init = True

    # Enter a parse tree produced by LangParser#stat.
    def enterStat(self, ctx:LangParser.StatContext):
        pass

    # Exit a parse tree produced by LangParser#stat.
    def exitStat(self, ctx:LangParser.StatContext):
        pass


    # Enter a parse tree produced by LangParser#funcStat.
    def enterFuncStat(self, ctx:LangParser.FuncStatContext):
        if isinstance(ctx.parentCtx, LangParser.ForStatContext):
            self.initUserForLocSpace(ctx.parentCtx)
        if not self.is_func_init and isinstance(ctx.parentCtx, LangParser.FuncContext):
            self.checkAndInitUserFunc(ctx.parentCtx)

    def initUserForLocSpace(self, ctx:LangParser.ForStatContext):
        if ctx.assignExpr() and ctx.assignExpr().basicTypeName():
            ass_ctxt = ctx.assignExpr()
            type_ = str(ass_ctxt.basicTypeName().children[0])
            vars_ = list(map(str, ass_ctxt.ID()))

            for_vars = self.all_for_vars.get("for_local")
            if for_vars:
                while for_vars.get("for_local"):
                    for_vars = for_vars.get("for_local")
            else:
                for_vars = self.all_for_vars
            for var in vars_:
                for_vars[var] = [type_, False]


    # Exit a parse tree produced by LangParser#funcStat.
    def exitFuncStat(self, ctx:LangParser.FuncStatContext):
        if ctx.returnStmt() and not self.is_func_init:
            raise SemanticAnalyzerException("Cannot return value outside function space")
        elif ctx.returnStmt():
            self.is_func_return_smth = True
            return_type = self.findExpressionOutType(ctx.returnStmt().numbExpr())
            if return_type != self.local_func_params.get('return_type'):
                raise SemanticAnalyzerException(f"{self.local_func_params.get('return_type')} function returns {return_type} object")
        elif ctx.stat() and ((ctx.stat().assignExpr() and ctx.stat().assignExpr().basicTypeName()) or ctx.stat().varDeclStmt() is not None):
            ass_ctxt = ctx.stat().assignExpr() if ctx.stat().assignExpr() else ctx.stat().varDeclStmt()
            if ass_ctxt.basicTypeName() is None:
                return
            _type = str(ass_ctxt.basicTypeName().children[0])
            if isinstance(ctx.parentCtx, LangParser.FuncContext):
                for id in ass_ctxt.ID():
                    self.local_func_vars[str(id)] = (_type, False)
            elif isinstance(ctx.parentCtx, LangParser.ForStatContext):
                for_vars = self.all_for_vars.get("for_local")
                if for_vars:
                    while for_vars:
                        for_vars = for_vars.get("for_local")
                else:   for_vars = self.all_for_vars
                for id in ass_ctxt.ID():
                    for_vars[str(id)] = (_type, False)
            elif isinstance(ctx.parentCtx, LangParser.UntilStmtContext):
                until_vars = self.local_until_vars.get("until_local")
                while until_vars:
                    until_vars = until_vars.get("until_local")
                for id in ass_ctxt.ID():
                    until_vars[str(id)] = (_type, False)
            elif isinstance(ctx.parentCtx, LangParser.WhileStmtContext):
                while_vars = self.local_while_vars.get("while_local")
                while while_vars:
                    while_vars = while_vars.get("while_local")
                for id in ass_ctxt.ID():
                    while_vars[str(id)] = (_type, False)
            elif isinstance(ctx.parentCtx, LangParser.IfElseStmtContext):
                ifels_vars = self.local_ifels_vars.get("ifels_local")
                while ifels_vars:
                    ifels_vars = ifels_vars.get("ifels_local")
                for id in ass_ctxt.ID():
                    ifels_vars[str(id)] = (_type, False)


    # Enter a parse tree produced by LangParser#forStat.
    def enterForStat(self, ctx:LangParser.ForStatContext):
        if isinstance(ctx.parentCtx.parentCtx, LangParser.FuncStatContext):
            self.all_for_vars = {}
        elif isinstance(ctx.parentCtx.parentCtx, LangParser.ProgramContext):
            self.all_for_vars["for_local"] = {}

    # Exit a parse tree produced by LangParser#forStat.
    def exitForStat(self, ctx:LangParser.ForStatContext):
        for_vars_space = self.all_for_vars.get("for_local")
        if for_vars_space:
            while for_vars_space.get("for_local"):
                for_vars_space = for_vars_space.get("for_local")
        else:
            for_vars_space = self.all_for_vars
        for local_var in for_vars_space:
            self.global_vars.pop(local_var)
        
        ### delete 
        if not self.all_for_vars.get("for_local"):
            self.all_for_vars = {}
        else:
            tmp = self.all_for_vars
            while tmp.get("for_local").get("for_local"):
                tmp = tmp.get("for_local")
            tmp.pop("for_local")


    # Enter a parse tree produced by LangParser#assignExpr.
    def enterAssignExpr(self, ctx:LangParser.AssignExprContext):
        pass


    def findVarType(self, ctx:LangParser.BasicTypeContext|LangParser.IterBasicTypeContext|str) -> str:
        if isinstance(ctx, str) or ctx.ID():
            str_id = str(ctx.ID()) if not isinstance(ctx, str) else ctx
            if self.global_vars.get(str_id) is None:
                raise SemanticAnalyzerException("Variable {} is not defined".format(str_id))
            var_obj = self.global_vars.get(str_id)
            if isinstance(var_obj, NumbVariable):
                var_type = 'numb'
            elif isinstance(var_obj, StringVariable):
                var_type = 'string'
            elif isinstance(var_obj, ColumnVariable):
                var_type = 'column'
            elif isinstance(var_obj, RowVariable):
                var_type = 'row'
            elif isinstance(var_obj, TableVariable):
                var_type = 'table'
            else:
                raise TypeError("Bro here is unknown object ((((")
            return var_type, False
        elif isinstance(ctx, LangParser.BasicTypeContext) and ctx.NUMBER():
            return 'numb', False
        elif isinstance(ctx, LangParser.BasicTypeContext) and ctx.STRING():
            return 'string', False
        else:
            raise SemanticAnalyzerException("Incorrect expression construction - {}".format(str(ctx.children[0])))

    def findBuiltinFunctionType(self, ctx:LangParser.BuiltinFuncStmtContext) -> tuple[str, str]:
        function_ctxt = ctx.children[0]
        func_return_type, func_name = None, None
        func_name = str(function_ctxt.children[0])
        if isinstance(function_ctxt, LangParser.CustFuncCallContext):
            find_name = self.function_vars.get(func_name)
            if find_name is None:
                raise SemanticAnalyzerException(f"Function {func_name} is not found")
            func_return_type = find_name.get("return_type")
        elif isinstance(function_ctxt, LangParser.InsertStmtContext):
            first_param = function_ctxt.numbExpr(0)
            func_return_type = self.findExpressionOutType(first_param)
        elif isinstance(function_ctxt, LangParser.CopyStmtContext):
            func_return_type = self.findVarType(str(function_ctxt.ID()))[0]
        elif (isinstance(function_ctxt, LangParser.DelFuncStmtContext) and function_ctxt.delFunc().DEL() is not None):
            first_param = function_ctxt.numbExpr(0)
            func_return_type = self.findExpressionOutType(first_param)
        elif isinstance(function_ctxt, LangParser.MinMaxFuncStmtContext):
            func_name = str(function_ctxt.minMaxFunc().children[0])
            func_return_type = self.function_vars.get(func_name).get("return_type")
        elif isinstance(function_ctxt, LangParser.DelFuncStmtContext):
            func_name = str(function_ctxt.delFunc().children[0])
            func_return_type = self.function_vars.get(func_name).get("return_type")
        else:
            func_return_type = self.function_vars.get(func_name).get("return_type")
        if isinstance(function_ctxt, LangParser.DelFuncStmtContext):
            func_name = str(function_ctxt.delFunc().children[0])
        
        return func_return_type, func_name
    

    def findIndexStmtType(self, ctx:LangParser.IndexStmtContext) -> str:
        if not isinstance(ctx, LangParser.IndexStmtContext):
            raise TypeError(f"Incorrect context type {type(ctx)}")
        if ctx.iterBasicType():
            iter_var = ctx.iterBasicType()
            if iter_var.ID():
                var_type, _ = self.findVarType(iter_var)
                if var_type not in ('column', 'row', 'table'):
                    raise SemanticAnalyzerException(f"{var_type} object is not subscriptable")
                return var_type
        elif ctx.builtinFuncStmt():
            var_type = self.findBuiltinFunctionType(ctx.builtinFuncStmt())[0]
            if var_type not in ('column', 'row', 'table'):
                raise SemanticAnalyzerException(f"Function {str(ctx.builtinFuncStmt().ID(0))} returns not iterable object")
            return var_type
        
    def findExprTypeWithTwoOperands(self, first_operand_ctxt: LangParser.NumbExprContext, 
                                   sign_ctxt: LangParser.BoolNumbSignContext,
                                   second_operand_ctxt: LangParser.NumbExprContext
                                   ) -> str:
        first_operand_type = self.findExpressionOutType(first_operand_ctxt)
        second_operand_type = self.findExpressionOutType(second_operand_ctxt)
        sign = str(sign_ctxt.boolSign().children[0]) if sign_ctxt.boolSign() else str(sign_ctxt.numbSign().children[0])
        if first_operand_type not in self.available_operands.get(sign) or\
            second_operand_type not in self.available_operands.get(sign):
            raise SemanticAnalyzerException(f"Incorrect operands types ({first_operand_type},{second_operand_type}) for {sign} sign")
        if first_operand_type == second_operand_type:
            if sign_ctxt.boolSign():
                return 'numb'
            elif sign_ctxt.numbSign():
                if sign in ["/", "//"] and first_operand_type != 'numb':
                    raise SemanticAnalyzerException(f"Incorrect operands types ({first_operand_type},{second_operand_type}) for {sign} sign")
                return first_operand_type
        else:
                if sign in ["==", "!=", "<=", ">=", ">", "<", "!", "&", "|", "-", "*"]:
                    raise SemanticAnalyzerException(f"Operands types for {sign} sign should be equal")
                elif sign == '+':
                    types_set = set((first_operand_type, second_operand_type))
                    if not(types_set == {'row', 'table'} or types_set == {'column', 'table'}):
                        raise SemanticAnalyzerException(f"Incorrect operands types ({first_operand_type},{second_operand_type}) for {sign} sign")
                    return 'table'
                elif sign == '/':
                    if not(second_operand_type == 'numb' and first_operand_type in ['column', 'row', 'table']):
                        raise SemanticAnalyzerException(f"Incorrect operands types ({first_operand_type},{second_operand_type}) for {sign} sign")
                    return first_operand_type
                elif sign == '//':
                    if not (first_operand_type == 'table' and second_operand_type == 'numb'):
                        raise SemanticAnalyzerException(f"Operator // can be used for table and number types")
                    return 'table'                



    def findExpressionOutType(self, expr_context: LangParser.NumbExprContext) -> str:
        if expr_context.returnType():
            if expr_context.returnType().basicType():
                var_type, _ = self.findVarType(expr_context.returnType().basicType())
                return var_type
            elif expr_context.returnType().builtinFuncStmt():
                func_type, func_name = self.findBuiltinFunctionType(expr_context.returnType().builtinFuncStmt())
                return func_type
            elif expr_context.returnType().indexStmt():
                index_stmt_type = self.findIndexStmtType(expr_context.returnType().indexStmt())
                return index_stmt_type
        elif expr_context.boolNumbSign():
            return self.findExprTypeWithTwoOperands(
                expr_context.numbExpr(0),
                expr_context.boolNumbSign(),
                expr_context.numbExpr(1)
            )

    # Exit a parse tree produced by LangParser#assignExpr.
    def exitAssignExpr(self, ctx:LangParser.AssignExprContext):
        if ctx.ID() and ctx.indexStmt():
            raise SemanticAnalyzerException("Cannot initialize variables and index statements in one assign expression")
        if ctx.indexStmt():
            if ctx.basicTypeName():
                raise SemanticAnalyzerException(f"Cannot initialize index stmt with specified type - {str(ctx.basicTypeName().children[0])}")
            for idx_stmt in ctx.indexStmt():
                if idx_stmt.builtinFuncStmt():
                    raise SemanticAnalyzerException(f"Function {str(idx_stmt.builtinFuncStmt().children[0].children[0])} only returns values")
                self.findIndexStmtType(idx_stmt)

        elif ctx.ID():
            if ctx.basicTypeName():
                var_type = str(ctx.basicTypeName().children[0])
            else:
                var_type, is_const = self.findVarType(str(ctx.ID(0)))
                if is_const:
                    raise SemanticAnalyzerException(f"Variable {str(ctx.ID())} is constant")
            var_names = []
            for var_name in ctx.ID():
                var_names.append(str(var_name))
            if len(var_names) != len(set(var_names)):
                raise SemanticAnalyzerException(f"Attempt to define variables with similar name")
            assign_exprs_n = 0
            for numb_expr in ctx.numbExpr():
                if numb_expr.returnType() is not None:
                    return_type = numb_expr.returnType()
                    if return_type.basicType():
                        bas_type_ctx = return_type.basicType()
                        assign_var_type, _ = self.findVarType(bas_type_ctx)
                        if var_type != assign_var_type:
                            raise SemanticAnalyzerException(f"Variable {str(bas_type_ctx.children[0])} type ({assign_var_type}) is incompatible with '{var_type}' type")
                        assign_exprs_n += 1
                    elif return_type.builtinFuncStmt():
                        func_type, func_name = self.findBuiltinFunctionType(return_type.builtinFuncStmt())
                        if func_type == 'void':
                            raise SemanticAnalyzerException(f"Function {func_name} returns nothing")
                        if var_type != func_type:
                            raise SemanticAnalyzerException(f"Function '{func_name}' return type ({func_type}) is incompatible with '{var_type}' type")
                        assign_exprs_n += 1
                    elif return_type.indexStmt():
                        iter_obj_ctxt = return_type.indexStmt().children[0]
                        if isinstance(iter_obj_ctxt, LangParser.BuiltinFuncStmtContext):
                            func_type, func_name = self.findBuiltinFunctionType(iter_obj_ctxt)
                            if var_type != func_type:
                                raise SemanticAnalyzerException(f"Function '{func_name}' return type ({func_type}) is incompatible with '{var_type}' type")
                            assign_exprs_n += 1
                        if isinstance(iter_obj_ctxt, LangParser.IterBasicTypeContext):
                            obj_type = str(iter_obj_ctxt.children[0])
                            if iter_obj_ctxt.ID():
                                obj_type, _ = self.findVarType(str(iter_obj_ctxt.ID()))
                            else:
                                raise SemanticAnalyzerException(f"Incorrect subscritable variable")
                            if var_type != obj_type:
                                #raise SemanticAnalyzerException(f"Iterable object output doesn't match to variable type")
                                pass
                            assign_exprs_n += 1
                elif numb_expr.boolNumbSign() is not None:
                    sign_ctxt = numb_expr.boolNumbSign()
                    return_type = self.findExprTypeWithTwoOperands(numb_expr.numbExpr(0),
                                                                    sign_ctxt,
                                                                    numb_expr.numbExpr(1) 
                                                                    )
                    if var_type != return_type:
                        raise SemanticAnalyzerException("Expression returned type is {} instead of {} type".format(
                                return_type, var_type
                            ))
                    assign_exprs_n += 1

            if len(var_names) != assign_exprs_n:
                raise SemanticAnalyzerException("Variables number doesn't match to expressions number") 
            assign_results = []   
            for numbExprCtxt in ctx.numbExpr():
                assign_results.append(self.findNumbExprResult(numbExprCtxt))
            if ctx.basicTypeName():  
                for idx, var_name in enumerate(var_names):
                    self.addNewVariable(var_name, var_type, assign_results[idx])

        
    def addNewVariable(self, str_name : str, var_type : str, value: list|str|int, constant: bool = False):
        if self.function_vars.get(str_name):
                raise SemanticAnalyzerException(f"Function with name '{str_name}' is already defined")
        if self.global_vars.get(str_name):
                raise SemanticAnalyzerException(f"Variable with name '{str_name}' is already defined")
        if var_type == 'numb':
            self.global_vars[str_name] = NumbVariable(str_name, value, self.program_compiler.main_builder)


    def findNumbExprResult(self, ctx:LangParser.NumbExprContext):
        if ctx.returnType():
            expr:LangParser.ReturnTypeContext = ctx.returnType()
            if expr.basicType():
                if expr.basicType().ID():
                    return self.global_vars.get(str(expr.basicType().ID()))
                elif expr.basicType().NUMBER():
                    value = float(str(expr.basicType().NUMBER()))
                    return value
                elif expr.basicType().STRING():
                    value = str(expr.basicType().STRING())
                    return value
            elif expr.builtinFuncStmt():
                pass
            elif expr.indexStmt():
                pass
        elif ctx.boolNumbSign():
            result = self.findExprResultWithTwoOperands(
                self, 
                ctx.numbExpr(0),
                ctx.boolNumbSign(),
                ctx.numbExpr(1)
                )

    def findExprResultWithTwoOperands(self, nexprctx1:LangParser.NumbExprContext, signctxt:LangParser.BoolNumbSignContext, nexprctx2:LangParser.NumbExprContext):
        pass

    # Enter a parse tree produced by LangParser#varDeclStmt.
    def enterVarDeclStmt(self, ctx:LangParser.VarDeclStmtContext):
        pass

    # Exit a parse tree produced by LangParser#varDeclStmt.
    def exitVarDeclStmt(self, ctx:LangParser.VarDeclStmtContext):
        var_type = str(ctx.basicTypeName().children[0])
        var_names = list(map(str, ctx.ID()))
        if len(var_names) != len(set(var_names)):
            raise SemanticAnalyzerException(f"Attempt to define variables with similar name")
        for var_ctxt in ctx.ID():
            self.addNewVariable(str(var_ctxt), var_type)


    # Enter a parse tree produced by LangParser#incDecrStat.
    def enterIncDecrStat(self, ctx:LangParser.IncDecrStatContext):
        pass

    # Exit a parse tree produced by LangParser#incDecrStat.
    def exitIncDecrStat(self, ctx:LangParser.IncDecrStatContext):
        var_type, is_const = self.findVarType(str(ctx.ID()))
        if var_type != 'numb':
            raise SemanticAnalyzerException("Increment and decrement are used for number variables")
        if is_const:
            raise SemanticAnalyzerException(f"Variable {str(ctx.ID())} is constant")

    # Enter a parse tree produced by LangParser#assignSign.
    def enterAssignSign(self, ctx:LangParser.AssignSignContext):
        pass

    # Exit a parse tree produced by LangParser#assignSign.
    def exitAssignSign(self, ctx:LangParser.AssignSignContext):
        pass


    # Enter a parse tree produced by LangParser#basicTypeName.
    def enterBasicTypeName(self, ctx:LangParser.BasicTypeNameContext):
        pass

    # Exit a parse tree produced by LangParser#basicTypeName.
    def exitBasicTypeName(self, ctx:LangParser.BasicTypeNameContext):
        pass


    # Enter a parse tree produced by LangParser#boolSign.
    def enterBoolSign(self, ctx:LangParser.BoolSignContext):
        pass

    # Exit a parse tree produced by LangParser#boolSign.
    def exitBoolSign(self, ctx:LangParser.BoolSignContext):
        pass


    # Enter a parse tree produced by LangParser#numbSign.
    def enterNumbSign(self, ctx:LangParser.NumbSignContext):
        pass

    # Exit a parse tree produced by LangParser#numbSign.
    def exitNumbSign(self, ctx:LangParser.NumbSignContext):
        pass


    # Enter a parse tree produced by LangParser#boolNumbSign.
    def enterBoolNumbSign(self, ctx:LangParser.BoolNumbSignContext):
        pass

    # Exit a parse tree produced by LangParser#boolNumbSign.
    def exitBoolNumbSign(self, ctx:LangParser.BoolNumbSignContext):
        pass


    # Enter a parse tree produced by LangParser#iterBasicType.
    def enterIterBasicType(self, ctx:LangParser.IterBasicTypeContext):
        pass

    # Exit a parse tree produced by LangParser#iterBasicType.
    def exitIterBasicType(self, ctx:LangParser.IterBasicTypeContext):
        pass


    # Enter a parse tree produced by LangParser#basicType.
    def enterBasicType(self, ctx:LangParser.BasicTypeContext):
        pass

    # Exit a parse tree produced by LangParser#basicType.
    def exitBasicType(self, ctx:LangParser.BasicTypeContext):
        pass


    # Enter a parse tree produced by LangParser#returnType.
    def enterReturnType(self, ctx:LangParser.ReturnTypeContext):
        pass

    # Exit a parse tree produced by LangParser#returnType.
    def exitReturnType(self, ctx:LangParser.ReturnTypeContext):
        pass


    # Enter a parse tree produced by LangParser#numbExpr.
    def enterNumbExpr(self, ctx:LangParser.NumbExprContext):
        pass

    # Exit a parse tree produced by LangParser#numbExpr.
    def exitNumbExpr(self, ctx:LangParser.NumbExprContext):
        self.findExpressionOutType(ctx)


    # Enter a parse tree produced by LangParser#boolExpr.
    def enterBoolExpr(self, ctx:LangParser.BoolExprContext):
        pass

    # Exit a parse tree produced by LangParser#boolExpr.
    def exitBoolExpr(self, ctx:LangParser.BoolExprContext):
        first_operand_type = self.findExpressionOutType(ctx.numbExpr(0))
        second_operand_type = self.findExpressionOutType(ctx.numbExpr(1))
        if first_operand_type != second_operand_type:
            raise SemanticAnalyzerException("Bool operations can perform only with equal types")        


    # Enter a parse tree produced by LangParser#ifElseStmt.
    def enterIfElseStmt(self, ctx:LangParser.IfElseStmtContext):
        if isinstance(ctx.parentCtx.parentCtx, LangParser.FuncStatContext):
            self.local_ifels_vars["ifels_local"] = {}
        elif isinstance(ctx.parentCtx.parentCtx, LangParser.ProgramContext):
            self.local_ifels_vars = {}

    # Exit a parse tree produced by LangParser#ifElseStmt.
    def exitIfElseStmt(self, ctx:LangParser.IfElseStmtContext):
        ifels_local_space = self.local_ifels_vars.get("ifels_local")
        if ifels_local_space:
            while ifels_local_space.get("ifels_local"):
                ifels_local_space = ifels_local_space.get("ifels_local")
        else:
            ifels_local_space = self.local_ifels_vars
        for local_var in ifels_local_space:
            if local_var != 'ifels_local':
                self.global_vars.pop(local_var) 

        if not self.local_ifels_vars.get("ifels_local"):
            self.local_ifels_vars = {}
        else:
            tmp = self.local_ifels_vars
            while tmp.get("ifels_local").get("ifels_local"):
                tmp = tmp.get("ifels_local")
            tmp.pop("ifels_local")


    # Enter a parse tree produced by LangParser#whileStmt.
    def enterWhileStmt(self, ctx:LangParser.WhileStmtContext):
        if isinstance(ctx.parentCtx.parentCtx, LangParser.FuncStatContext):
            self.local_while_vars["while_local"] = {}
        elif isinstance(ctx.parentCtx.parentCtx, LangParser.ProgramContext):
            self.local_while_vars = {}

    # Exit a parse tree produced by LangParser#whileStmt.
    def exitWhileStmt(self, ctx:LangParser.WhileStmtContext):
        while_local_space = self.local_while_vars.get("while_local")
        if while_local_space:
            while while_local_space.get("while_local"):
                while_local_space = while_local_space.get("while_local")
        else:
            while_local_space = self.local_while_vars
        for local_var in while_local_space:
            if local_var != 'while_local':
                self.global_vars.pop(local_var) 

        if not self.local_while_vars.get("while_local"):
            self.local_while_vars = {}
        else:
            tmp = self.local_while_vars
            while tmp.get("while_local").get("while_local"):
                tmp = tmp.get("while_local")
            tmp.pop("while_local")


    # Enter a parse tree produced by LangParser#untilStmt.
    def enterUntilStmt(self, ctx:LangParser.UntilStmtContext):
        pass

    # Exit a parse tree produced by LangParser#untilStmt.
    def exitUntilStmt(self, ctx:LangParser.UntilStmtContext):
        until_local_space = self.local_until_vars.get("until_local")
        if until_local_space:
            while until_local_space.get("while_local"):
                until_local_space = until_local_space.get("until_local")
        else:
            until_local_space = self.local_until_vars
        for local_var in until_local_space:
            if local_var != 'until_local':
                self.global_vars.pop(local_var) 

        if not self.local_until_vars.get("until_local"):
            self.local_until_vars = {}
        else:
            tmp = self.local_until_vars
            while tmp.get("until_local").get("until_local"):
                tmp = tmp.get("until_local")
            tmp.pop("until_local")


    # Enter a parse tree produced by LangParser#custFuncCall.
    def enterCustFuncCall(self, ctx:LangParser.CustFuncCallContext):
        pass

    # Exit a parse tree produced by LangParser#custFuncCall.
    def exitCustFuncCall(self, ctx:LangParser.CustFuncCallContext):
        self.checkNumbExprCorrectInFunctionCall(ctx, str(ctx.ID()))


    # Enter a parse tree produced by LangParser#indexStmt.
    def enterIndexStmt(self, ctx:LangParser.IndexStmtContext):
        pass

    # Exit a parse tree produced by LangParser#indexStmt.
    def exitIndexStmt(self, ctx:LangParser.IndexStmtContext):
        self.findIndexStmtType(ctx)


    # Enter a parse tree produced by LangParser#listStmt.
    def enterListStmt(self, ctx:LangParser.ListStmtContext):
        pass

    # Exit a parse tree produced by LangParser#listStmt.
    def exitListStmt(self, ctx:LangParser.ListStmtContext):
        pass


    # Enter a parse tree produced by LangParser#builtinFuncStmt.
    def enterBuiltinFuncStmt(self, ctx:LangParser.BuiltinFuncStmtContext):
        pass

    # Exit a parse tree produced by LangParser#builtinFuncStmt.
    def exitBuiltinFuncStmt(self, ctx:LangParser.BuiltinFuncStmtContext):
        pass


    # Enter a parse tree produced by LangParser#lengthStmt.
    def enterLengthStmt(self, ctx:LangParser.LengthStmtContext):
        pass

    # Exit a parse tree produced by LangParser#lengthStmt.
    def exitLengthStmt(self, ctx:LangParser.LengthStmtContext):
        self.checkNumbExprCorrectInFunctionCall(ctx, str(ctx.LENGTH()))


    # Enter a parse tree produced by LangParser#returnStmt.
    def enterReturnStmt(self, ctx:LangParser.ReturnStmtContext):
        pass

    # Exit a parse tree produced by LangParser#returnStmt.
    def exitReturnStmt(self, ctx:LangParser.ReturnStmtContext):
        pass


    # Enter a parse tree produced by LangParser#createRowStmt.
    def enterCreateRowStmt(self, ctx:LangParser.CreateRowStmtContext):
        pass

    # Exit a parse tree produced by LangParser#createRowStmt.
    def exitCreateRowStmt(self, ctx:LangParser.CreateRowStmtContext):
        pass

    # Enter a parse tree produced by LangParser#createTablStmt.
    def enterCreateTablStmt(self, ctx:LangParser.CreateTablStmtContext):
        pass

    # Exit a parse tree produced by LangParser#createTablStmt.
    def exitCreateTablStmt(self, ctx:LangParser.CreateTablStmtContext):
        pass


    # Enter a parse tree produced by LangParser#createColStmt.
    def enterCreateColStmt(self, ctx:LangParser.CreateColStmtContext):
        pass

    # Exit a parse tree produced by LangParser#createColStmt.
    def exitCreateColStmt(self, ctx:LangParser.CreateColStmtContext):
        pass


    # Enter a parse tree produced by LangParser#copyStmt.
    def enterCopyStmt(self, ctx:LangParser.CopyStmtContext):
        pass

    # Exit a parse tree produced by LangParser#copyStmt.
    def exitCopyStmt(self, ctx:LangParser.CopyStmtContext):
        self.findVarType(str(ctx.ID()))


    # Enter a parse tree produced by LangParser#minMaxFunc.
    def enterMinMaxFunc(self, ctx:LangParser.MinMaxFuncContext):
        pass

    # Exit a parse tree produced by LangParser#minMaxFunc.
    def exitMinMaxFunc(self, ctx:LangParser.MinMaxFuncContext):
        pass


    # Enter a parse tree produced by LangParser#minMaxFuncStmt.
    def enterMinMaxFuncStmt(self, ctx:LangParser.MinMaxFuncStmtContext):
        pass

    # Exit a parse tree produced by LangParser#minMaxFuncStmt.
    def exitMinMaxFuncStmt(self, ctx:LangParser.MinMaxFuncStmtContext):
        self.checkNumbExprCorrectInFunctionCall(ctx, str(ctx.minMaxFunc().children[0]))


    # Enter a parse tree produced by LangParser#delFunc.
    def enterDelFunc(self, ctx:LangParser.DelFuncContext):
        pass

    # Exit a parse tree produced by LangParser#delFunc.
    def exitDelFunc(self, ctx:LangParser.DelFuncContext):
        pass


    # Enter a parse tree produced by LangParser#delFuncStmt.
    def enterDelFuncStmt(self, ctx:LangParser.DelFuncStmtContext):
        pass

    # Exit a parse tree produced by LangParser#delFuncStmt.
    def exitDelFuncStmt(self, ctx:LangParser.DelFuncStmtContext):
        self.checkNumbExprCorrectInFunctionCall(ctx, str(ctx.delFunc().children[0]))


    # Enter a parse tree produced by LangParser#reshapeStmt.
    def enterReshapeStmt(self, ctx:LangParser.ReshapeStmtContext):
        pass

    # Exit a parse tree produced by LangParser#reshapeStmt.
    def exitReshapeStmt(self, ctx:LangParser.ReshapeStmtContext):
        self.checkNumbExprCorrectInFunctionCall(ctx, str(ctx.RESHAPE()))


    # Enter a parse tree produced by LangParser#insertStmt.
    def enterInsertStmt(self, ctx:LangParser.InsertStmtContext):
        pass

    # Exit a parse tree produced by LangParser#insertStmt.
    def exitInsertStmt(self, ctx:LangParser.InsertStmtContext):
        self.checkNumbExprCorrectInFunctionCall(ctx, str(ctx.INSERT()))


    # Enter a parse tree produced by LangParser#findStmt.
    def enterFindStmt(self, ctx:LangParser.FindStmtContext):
        pass

    # Exit a parse tree produced by LangParser#findStmt.
    def exitFindStmt(self, ctx:LangParser.FindStmtContext):
        self.checkNumbExprCorrectInFunctionCall(ctx, str(ctx.FIND()))


    # Enter a parse tree produced by LangParser#printStmt.
    def enterPrintStmt(self, ctx:LangParser.PrintStmtContext):
        pass

    # Exit a parse tree produced by LangParser#printStmt.
    def exitPrintStmt(self, ctx:LangParser.PrintStmtContext):
        self.checkNumbExprCorrectInFunctionCall(ctx, str(ctx.PRINT()))
        self.program_compiler.call_print_func(self.findNumbExprResult(ctx.numbExpr(0)))


    # Enter a parse tree produced by LangParser#readStrStmt.
    def enterReadStrStmt(self, ctx:LangParser.ReadStrStmtContext):
        pass

    # Exit a parse tree produced by LangParser#readStrStmt.
    def exitReadStrStmt(self, ctx:LangParser.ReadStrStmtContext):
        pass


    def checkNumbExprCorrectInFunctionCall(self, ctx, func_name):
        params = ctx.numbExpr() if isinstance(ctx.numbExpr(), list) else [ctx.numbExpr()]
        params_types = list(map(self.findExpressionOutType, params))
        if not self.function_vars.get(func_name):
            raise SemanticAnalyzerException("Function {} is not defined".format(func_name))
        available_types = [aval_param.split('/') for aval_param in self.function_vars.get(func_name).get("params")]
        if len(available_types) != len(params_types):
            raise SemanticAnalyzerException("Expected {} parameters, received - {} in function {}".format(len(available_types), len(params_types), func_name))
        for param_index, aval_types_for_each_param in enumerate(available_types):
            if params_types[param_index] not in aval_types_for_each_param:
                raise SemanticAnalyzerException(f"Expected {param_index} parameter to be {aval_types_for_each_param} in {func_name} function. Received - {params_types[param_index]}")
