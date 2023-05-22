import sys
import os
from antlr4 import *
from lexer.LangLexer import LangLexer
from parser.LangParser import LangParser
from parser.LangParserListener import LangParserListener, SemanticAnalyzerException
from parser.LangParserVisitor import LangParserVisitor
from MyErrorStrategy import MyErrorStrategy
from MyErrorListener import MyErrorListener


def get_username():
    from pwd import getpwuid
    from os import getuid
    return getpwuid(getuid())[0]


if __name__ == '__main__':
    print(get_username())
    if len(sys.argv) > 1:
        data = FileStream(sys.argv[1])
        lexer = LangLexer(data)
        stream = CommonTokenStream(lexer)
        parser = LangParser(stream)
        parser.removeErrorListeners()
        parser.addErrorListener(MyErrorListener())
        parser.addParseListener(LangParserListener())
        parser.resetErrHandler(MyErrorStrategy())
        tree = parser.program()
        visitor = LangParserVisitor()
        output = visitor.visit(tree)
        if output:
            print(output)
    else:
        listener = LangParserListener()
        while True:
            try:
                data = InputStream(input(">>> "))
                lexer = LangLexer(data)
                stream = CommonTokenStream(lexer)
                parser = LangParser(stream)
                parser.removeErrorListeners()
                parser.addErrorListener(MyErrorListener())
                parser.addParseListener(listener)
                parser.resetErrHandler(MyErrorStrategy())
                tree = parser.program()
                visitor = LangParserVisitor()
                output = visitor.visit(tree)
            except SemanticAnalyzerException as exc:
                listener.clear_func_cache()
                print("Error - ", exc)
