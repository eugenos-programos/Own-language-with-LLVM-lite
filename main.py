import sys
from antlr4 import *
from LangLexer import LangLexer
from LangParser import LangParser
from LangParserVisitor import LangParserVisitor


def get_username():
    from pwd import getpwuid
    from os import getuid
    return getpwuid(getuid())[ 0 ]


class MyVisitor(LangParserVisitor):
    def visitNumbExpr(self, ctx: LangParser.NumbExprContext):
        return super().visitNumbExpr(ctx)
    

if __name__ == '__main__':
    while True:
        data = InputStream(input(">>> "))
        lexer = LangLexer(data)
        stream = CommonTokenStream(lexer)
        parser = LangParser(stream)
        tree = ...
        visitor = MyVisitor()
        output = visitor.visit(tree)
        print(output)
