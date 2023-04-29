# Generated from LangParser.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .LangParser import LangParser
else:
    from LangParser import LangParser


class SemanticAnalyzerException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


def get_dict(params, out_type):
    return {"params": params, "return_type": out_type}

# This class defines a complete listener for a parse tree produced by LangParser.
class LangParserListener(ParseTreeListener):

    numb_vars = []
    str_vars = []
    column_vars = []
    row_vars = []
    table_vars = []
    function_vars = {
        "print": get_dict(["any"], "void"),
        "length": get_dict(["any"], "numb"),
        "reshape": get_dict(["changing"], ?),
        "del_col": get_dict(["table", "numb"], "table"),
        "del_row": get_dict(["table", "numb"], "table"),
        "del": get_dict(["any"], "void"),
        "insert": get_dict(?, ?), 
        "max": get_dict([], "numb"),
        "min": get_dict([], "numb"),
        "maxlen": get_dict([], "numb"),
        "find": get_dict([], ),
        "create_row", get_dict([], "row"),
        "create_table", get_dict([], "table"),
        "create_column", get_dict([], "column"),
        "read_string", get_dict([], "string"),
        "copy": get_dict(["any"], "any")

    }

    # Enter a parse tree produced by LangParser#program.
    def enterProgram(self, ctx:LangParser.ProgramContext):
        pass

    # Exit a parse tree produced by LangParser#program.
    def exitProgram(self, ctx:LangParser.ProgramContext):
        pass


    # Enter a parse tree produced by LangParser#func.
    def enterFunc(self, ctx:LangParser.FuncContext):
        pass

    # Exit a parse tree produced by LangParser#func.
    def exitFunc(self, ctx:LangParser.FuncContext):
        func_name = ...
        self.function_vars.append(func_name)


    # Enter a parse tree produced by LangParser#stat.
    def enterStat(self, ctx:LangParser.StatContext):
        pass

    # Exit a parse tree produced by LangParser#stat.
    def exitStat(self, ctx:LangParser.StatContext):
        pass


    # Enter a parse tree produced by LangParser#funcStat.
    def enterFuncStat(self, ctx:LangParser.FuncStatContext):
        pass

    # Exit a parse tree produced by LangParser#funcStat.
    def exitFuncStat(self, ctx:LangParser.FuncStatContext):
        pass


    # Enter a parse tree produced by LangParser#forStat.
    def enterForStat(self, ctx:LangParser.ForStatContext):
        pass

    # Exit a parse tree produced by LangParser#forStat.
    def exitForStat(self, ctx:LangParser.ForStatContext):
        pass


    # Enter a parse tree produced by LangParser#assignExpr.
    def enterAssignExpr(self, ctx:LangParser.AssignExprContext):
        pass

    def findBuiltinFunctionType(self, ctx:LangParser.BuiltinFuncStmtContext) -> str:
        return None, None

    def findExpressionOutType(self, expr1, sign, expr2) -> str:
        return None

    # Exit a parse tree produced by LangParser#assignExpr.
    def exitAssignExpr(self, ctx:LangParser.AssignExprContext):
        if ctx.basicTypeName():
            var_type = ctx.basicTypeName().children[0]
        var_names = []
        for var_name in ctx.ID():
            var_names.append(var_name)
        assign_exprs = []
        for expr_index, numb_expr in enumerate(ctx.numbExpr()):
            numb_expr_type = numb_expr.children[0]
            if isinstance(numb_expr_type, LangParser.ReturnTypeContext):
                return_type_type = numb_expr_type.children[0]
                if isinstance(return_type_type, LangParser.BasicTypeContext):
                    assign_exprs.append(str(return_type_type.children[0]))
                if isinstance(return_type_type, LangParser.BuiltinFuncStmtContext):
                    func_type, func_name = self.findBuiltinFunctionType(return_type_type)
                    if var_type != func_type:
                        raise SemanticAnalyzerException(f"Builting function {func_name} return type is incompatible with {var_type} type")
                if isinstance(return_type_type, LangParser.IndexStmtContext):
                    iter_obj_ctxt = return_type_type.children[0]
                    if isinstance(iter_obj_ctxt, LangParser.BuiltinFuncStmtContext):
                        func_type, func_name = self.findBuiltinFunctionType(iter_obj_ctxt)
                        if var_type != func_type:
                            raise SemanticAnalyzerException(f"Builting function {func_name} return type is incompatible with {var_type} type")
                    if isinstance(iter_obj_ctxt, LangParser.BasicTypeContext):
                        obj_type = str(iter_obj_ctxt.children[0])
                        if var_type != obj_type:
                            raise SemanticAnalyzerException(f"Iterable object output doesn't match to variable type")
            else:
                print(numb_expr_type.children)
                sign_ctxt = numb_expr_type.children[1]
                if isinstance(sign_ctxt, LangParser.BoolSignContext):
                    return_type = 'numb'
                    if var_type != return_type:
                        raise SemanticAnalyzerException("Expression returns only numb values")
                if isinstance(sign_ctxt, LangParser.NumbSignContext):
                    expr_type = self.findExpressionOutType(*numb_expr_type.children)
                    if var_type != expr_type:
                        raise SemanticAnalyzerException("Expression returns {} value".format(expr_type))

        if len(var_names) != len(assign_exprs):
            raise SemanticAnalyzerException("Variables number doesn't match to expressions number")        
        print(assign_exprs)

        


    # Enter a parse tree produced by LangParser#varDeclStmt.
    def enterVarDeclStmt(self, ctx:LangParser.VarDeclStmtContext):
        pass

    # Exit a parse tree produced by LangParser#varDeclStmt.
    def exitVarDeclStmt(self, ctx:LangParser.VarDeclStmtContext):
        pass


    # Enter a parse tree produced by LangParser#incDecrStat.
    def enterIncDecrStat(self, ctx:LangParser.IncDecrStatContext):
        pass

    # Exit a parse tree produced by LangParser#incDecrStat.
    def exitIncDecrStat(self, ctx:LangParser.IncDecrStatContext):
        pass


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
        pass


    # Enter a parse tree produced by LangParser#boolExpr.
    def enterBoolExpr(self, ctx:LangParser.BoolExprContext):
        pass

    # Exit a parse tree produced by LangParser#boolExpr.
    def exitBoolExpr(self, ctx:LangParser.BoolExprContext):
        pass


    # Enter a parse tree produced by LangParser#ifElseStmt.
    def enterIfElseStmt(self, ctx:LangParser.IfElseStmtContext):
        pass

    # Exit a parse tree produced by LangParser#ifElseStmt.
    def exitIfElseStmt(self, ctx:LangParser.IfElseStmtContext):
        pass


    # Enter a parse tree produced by LangParser#whileStmt.
    def enterWhileStmt(self, ctx:LangParser.WhileStmtContext):
        pass

    # Exit a parse tree produced by LangParser#whileStmt.
    def exitWhileStmt(self, ctx:LangParser.WhileStmtContext):
        pass


    # Enter a parse tree produced by LangParser#untilStmt.
    def enterUntilStmt(self, ctx:LangParser.UntilStmtContext):
        pass

    # Exit a parse tree produced by LangParser#untilStmt.
    def exitUntilStmt(self, ctx:LangParser.UntilStmtContext):
        pass


    # Enter a parse tree produced by LangParser#custFuncCall.
    def enterCustFuncCall(self, ctx:LangParser.CustFuncCallContext):
        pass

    # Exit a parse tree produced by LangParser#custFuncCall.
    def exitCustFuncCall(self, ctx:LangParser.CustFuncCallContext):
        pass


    # Enter a parse tree produced by LangParser#indexStmt.
    def enterIndexStmt(self, ctx:LangParser.IndexStmtContext):
        pass

    # Exit a parse tree produced by LangParser#indexStmt.
    def exitIndexStmt(self, ctx:LangParser.IndexStmtContext):
        pass


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
        pass


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
        pass


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
        pass


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
        pass


    # Enter a parse tree produced by LangParser#reshapeStmt.
    def enterReshapeStmt(self, ctx:LangParser.ReshapeStmtContext):
        pass

    # Exit a parse tree produced by LangParser#reshapeStmt.
    def exitReshapeStmt(self, ctx:LangParser.ReshapeStmtContext):
        pass


    # Enter a parse tree produced by LangParser#insertStmt.
    def enterInsertStmt(self, ctx:LangParser.InsertStmtContext):
        pass

    # Exit a parse tree produced by LangParser#insertStmt.
    def exitInsertStmt(self, ctx:LangParser.InsertStmtContext):
        pass


    # Enter a parse tree produced by LangParser#findStmt.
    def enterFindStmt(self, ctx:LangParser.FindStmtContext):
        pass

    # Exit a parse tree produced by LangParser#findStmt.
    def exitFindStmt(self, ctx:LangParser.FindStmtContext):
        pass


    # Enter a parse tree produced by LangParser#printStmt.
    def enterPrintStmt(self, ctx:LangParser.PrintStmtContext):
        pass

    # Exit a parse tree produced by LangParser#printStmt.
    def exitPrintStmt(self, ctx:LangParser.PrintStmtContext):
        pass


    # Enter a parse tree produced by LangParser#readStrStmt.
    def enterReadStrStmt(self, ctx:LangParser.ReadStrStmtContext):
        pass

    # Exit a parse tree produced by LangParser#readStrStmt.
    def exitReadStrStmt(self, ctx:LangParser.ReadStrStmtContext):
        pass


