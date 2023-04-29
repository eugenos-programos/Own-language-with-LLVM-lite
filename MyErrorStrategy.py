from antlr4.error.Errors import RecognitionException, NoViableAltException, InputMismatchException, \
    FailedPredicateException
from antlr4.error.ErrorStrategy import DefaultErrorStrategy
from antlr4 import *
from parser.LangParser import LangParser


class MyErrorStrategy(DefaultErrorStrategy):
    def __init__(self) -> None:
        super().__init__()

    def reportError(self, recognizer: Parser, e: RecognitionException, localctx: ParserRuleContext = None):
       # if we've already reported an error and have not matched a token
       # yet successfully, don't report any errors.
        if self.inErrorRecoveryMode(recognizer):
            return # don't report spurious errors
        self.beginErrorCondition(recognizer)
        if isinstance( e, NoViableAltException ):
            msg = self.checkContext(localctx)
            self.reportNoViableAlternative(recognizer, e, msg)
        elif isinstance( e, InputMismatchException ):
            msg = self.checkContext(localctx)
            self.reportInputMismatch(recognizer, e, msg)
        elif isinstance( e, FailedPredicateException ):
            msg = self.checkContext(localctx)
            self.reportFailedPredicate(recognizer, e, msg)
        else:
            print("unknown recognition error type: " + type(e).__name__)
            recognizer.notifyErrorListeners(e.message, e.offendingToken, e)

    def checkContext(self, localctx : ParserRuleContext):
        msg = None
        if isinstance(localctx, LangParser.ForStatContext):
            msg = "For statement mismatched input - {}. Expected expression like for(<>;<>;<>)..."
        elif isinstance(localctx, LangParser.IfElseStmtContext):
            msg = "IF/Else statement mismatched input - {}. Expected expression like if bool_stmt <else >."
        elif isinstance(localctx, LangParser.AssignExprContext):
            msg = "Assign expression mismatched form - {}. Expected expression <type> ID [= value];"
        elif isinstance(localctx, LangParser.PrintStmtContext):
            msg = "Print function mismatched form - {}. Expected print(<value>);"
        elif isinstance(localctx, LangParser.FuncContext):
            msg = "Function definition mismatched form - {}. Expected <type> function ID (params)."
        elif isinstance(localctx, LangParser.WhileStmtContext):
            msg = "While statement mismatched form - {}. Expected while(boolExpr)..."
        elif isinstance(localctx, LangParser.UntilStmtContext):
            msg = "Until statement mismatched form - {}. Expected ...until(boolExpr)"
        elif isinstance(localctx, LangParser.IncDecrStatContext):
            msg = "Increment or decrement statement mismatched form - {}. Expected ++/--value."
        elif isinstance(localctx, LangParser.VarDeclStmtContext):
            msg = "Variable declaration mismatched form - {}. Expected basic_type <name> value?"
        elif isinstance(localctx, LangParser.CustFuncCallContext):
            msg = "Function call mismatched form - {}. Expected func_name(params)"
        elif isinstance(localctx, LangParser.IndexStmtContext):
            msg = "Index statement mismatched form - {}. Expected value[value]"
        elif isinstance(localctx, LangParser.ReadStrStmtContext):
            msg = "read_string function mismatched form - {}. Expected read_string();"
        elif isinstance(localctx, LangParser.ReturnStmtContext):
            msg = "return statement mismatched form - {}. Expected return value;"
        elif isinstance(localctx, (LangParser.CreateColStmtContext, LangParser.CreateRowStmtContext, LangParser.CreateTablStmtContext)):
            msg = "create function has a different form - {}. Expected create_function(params)."
        elif isinstance(localctx, LangParser.DelFuncContext):
            msg = "delete function has a mismatched form - {}. Expected delete_function(params)."
        elif isinstance(localctx, LangParser.InsertStmtContext):
            msg = "Insert function has a mismatched form - {}. Expected insert(value, value, value)."
        elif isinstance(localctx, LangParser.FindStmtContext):
            msg = "Find function has a different form - {}. Expected find(val1, val2)"
        elif isinstance(localctx, LangParser.LengthStmtContext):
            msg = "Find function has a different form - {}. Expected length(value)"
        elif isinstance(localctx, LangParser.CustFuncCallContext):
            msg = "Custom function call has a different form - {}. Expected func_name(params)"
        elif isinstance(localctx, LangParser.MinMaxFuncStmtContext):
            msg = "min/max function call has a different form - {}. Expected min_max_name(value)"
        elif isinstance(localctx, LangParser.ReshapeStmtContext):
            msg = "reshape function has a different form - {}. Expected reshape(val1, val2, val3)"
        elif isinstance(localctx, LangParser.ListStmtContext):
            msg = "List definition has a different form - {}. Expected [...,...,...]"
        elif isinstance(localctx, LangParser.BoolExprContext):
            msg = "Boolean expresion has a different form - {}. Expeted val1 <bool_sign> val2"
        elif isinstance(localctx, LangParser.ReturnTypeContext):
            msg = "Return value has a different form - {}. Gotten non return statement."
        elif isinstance(localctx, LangParser.BasicTypeNameContext):
            msg = "Basic type name expected. But {} received."
        elif isinstance(localctx, LangParser.StatContext):
            msg = "Expression has an incorrect form - {}."
        return msg

    def reportNoViableAlternative(self, recognizer: Parser, e: NoViableAltException, msg : str = None):
        tokens = recognizer.getTokenStream()
        if tokens is not None:
            if e.startToken.type==Token.EOF:
                input = "<EOF>"
            else:
                input = tokens.getText((e.startToken, e.offendingToken))
        else:
            input = "<unknown input>"
        if msg:
            msg = msg.format(self.escapeWSAndQuote(input))
        else:
            msg = "Name " + self.escapeWSAndQuote(input) + " is not defined"
        recognizer.notifyErrorListeners(msg, e.offendingToken, e)

    def reportInputMismatch(self, recognizer: Parser, e: InputMismatchException, msg : str = None):
        if msg:
            msg = msg.format(self.getTokenErrorDisplay(e.offendingToken))
        if not msg: 
            msg = "mismatched input " + self.getTokenErrorDisplay(e.offendingToken) \
              + " expecting " + e.getExpectedTokens().toString(recognizer.literalNames, recognizer.symbolicNames)
        recognizer.notifyErrorListeners(msg, e.offendingToken, e)

    def reportFailedPredicate(self, recognizer, e, msg):
        ruleName = recognizer.ruleNames[recognizer._ctx.getRuleIndex()]
        msg = msg.format(ruleName)
        if not msg:
            msg = "rule " + ruleName + " " + e.message
        recognizer.notifyErrorListeners(msg, e.offendingToken, e)

    def reportMissingToken(self, recognizer:Parser):
        if self.inErrorRecoveryMode(recognizer):
            return
        self.beginErrorCondition(recognizer)
        t = recognizer.getCurrentToken()
        expecting = self.getExpectedTokens(recognizer)
        msg = "missing " + expecting.toString(recognizer.literalNames, recognizer.symbolicNames) \
              + " after line " + self.getTokenErrorDisplay(t)
        recognizer.notifyErrorListeners(msg, t, None)

    