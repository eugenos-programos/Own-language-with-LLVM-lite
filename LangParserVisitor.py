# Generated from LangParser.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .LangParser import LangParser
else:
    from LangParser import LangParser

# This class defines a complete generic visitor for a parse tree produced by LangParser.

class LangParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by LangParser#program.
    def visitProgram(self, ctx:LangParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LangParser#func.
    def visitFunc(self, ctx:LangParser.FuncContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LangParser#stat.
    def visitStat(self, ctx:LangParser.StatContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LangParser#funcStat.
    def visitFuncStat(self, ctx:LangParser.FuncStatContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LangParser#forStat.
    def visitForStat(self, ctx:LangParser.ForStatContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LangParser#assignExpr.
    def visitAssignExpr(self, ctx:LangParser.AssignExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LangParser#varDeclStmt.
    def visitVarDeclStmt(self, ctx:LangParser.VarDeclStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LangParser#incDecrStat.
    def visitIncDecrStat(self, ctx:LangParser.IncDecrStatContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LangParser#assignSign.
    def visitAssignSign(self, ctx:LangParser.AssignSignContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LangParser#basicTypeName.
    def visitBasicTypeName(self, ctx:LangParser.BasicTypeNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LangParser#boolSign.
    def visitBoolSign(self, ctx:LangParser.BoolSignContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LangParser#numbSign.
    def visitNumbSign(self, ctx:LangParser.NumbSignContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LangParser#boolNumbSign.
    def visitBoolNumbSign(self, ctx:LangParser.BoolNumbSignContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LangParser#iterBasicType.
    def visitIterBasicType(self, ctx:LangParser.IterBasicTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LangParser#basicType.
    def visitBasicType(self, ctx:LangParser.BasicTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LangParser#returnType.
    def visitReturnType(self, ctx:LangParser.ReturnTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LangParser#numbExpr.
    def visitNumbExpr(self, ctx:LangParser.NumbExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LangParser#boolExpr.
    def visitBoolExpr(self, ctx:LangParser.BoolExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LangParser#ifElseStmt.
    def visitIfElseStmt(self, ctx:LangParser.IfElseStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LangParser#whileStmt.
    def visitWhileStmt(self, ctx:LangParser.WhileStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LangParser#untilStmt.
    def visitUntilStmt(self, ctx:LangParser.UntilStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LangParser#custFuncCall.
    def visitCustFuncCall(self, ctx:LangParser.CustFuncCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LangParser#indexStmt.
    def visitIndexStmt(self, ctx:LangParser.IndexStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LangParser#listStmt.
    def visitListStmt(self, ctx:LangParser.ListStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LangParser#builtinFuncStmt.
    def visitBuiltinFuncStmt(self, ctx:LangParser.BuiltinFuncStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LangParser#lengthStmt.
    def visitLengthStmt(self, ctx:LangParser.LengthStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LangParser#returnStmt.
    def visitReturnStmt(self, ctx:LangParser.ReturnStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LangParser#createRowStmt.
    def visitCreateRowStmt(self, ctx:LangParser.CreateRowStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LangParser#createTablStmt.
    def visitCreateTablStmt(self, ctx:LangParser.CreateTablStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LangParser#createColStmt.
    def visitCreateColStmt(self, ctx:LangParser.CreateColStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LangParser#copyStmt.
    def visitCopyStmt(self, ctx:LangParser.CopyStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LangParser#minMaxFunc.
    def visitMinMaxFunc(self, ctx:LangParser.MinMaxFuncContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LangParser#minMaxFuncStmt.
    def visitMinMaxFuncStmt(self, ctx:LangParser.MinMaxFuncStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LangParser#delFunc.
    def visitDelFunc(self, ctx:LangParser.DelFuncContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LangParser#delFuncStmt.
    def visitDelFuncStmt(self, ctx:LangParser.DelFuncStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LangParser#reshapeStmt.
    def visitReshapeStmt(self, ctx:LangParser.ReshapeStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LangParser#insertStmt.
    def visitInsertStmt(self, ctx:LangParser.InsertStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LangParser#findStmt.
    def visitFindStmt(self, ctx:LangParser.FindStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LangParser#printStmt.
    def visitPrintStmt(self, ctx:LangParser.PrintStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LangParser#readStrStmt.
    def visitReadStrStmt(self, ctx:LangParser.ReadStrStmtContext):
        return self.visitChildren(ctx)



del LangParser