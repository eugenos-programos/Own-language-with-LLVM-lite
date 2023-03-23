# Generated from LangParser.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .LangParser import LangParser
else:
    from LangParser import LangParser

# This class defines a complete listener for a parse tree produced by LangParser.
class LangParserListener(ParseTreeListener):

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
        pass


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

    # Exit a parse tree produced by LangParser#assignExpr.
    def exitAssignExpr(self, ctx:LangParser.AssignExprContext):
        pass


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


