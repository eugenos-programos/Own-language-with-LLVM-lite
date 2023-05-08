parser grammar LangParser;
options { tokenVocab=LangLexer; }

program: func* stat* EOF;


func :
    (basicTypeName|'void') FUNCTION
    ID '(' (basicTypeName ID)? (',' 
        basicTypeName ID)* ')'
    '{' funcStat* '}' ;

stat: 
    (assignExpr SEMI
    | builtinFuncStmt SEMI
    | printStmt SEMI
    | forStat
    | ifElseStmt
    | whileStmt
    | untilStmt
    | incDecrStat SEMI
    | varDeclStmt SEMI)
    COMMENT?
    ;

funcStat: 
    stat
    | returnStmt;

forStat : FOR LPAREN assignExpr? SEMI
    boolExpr? SEMI incDecrStat? RPAREN
    '{' funcStat* '}' ;

assignExpr:
        basicTypeName? 
            (ID|indexStmt)
            (COMMA ID|indexStmt)*
            assignSign
                numbExpr
            (COMMA numbExpr)*;
                
varDeclStmt:
        basicTypeName
            ID (COMMA ID)*; 
    
incDecrStat : (PLUS PLUS | MINUS MINUS)
    ID;

assignSign:
    ASSIGN
    | PLUS_EQUAL
    | MINUS_EQUAL
    | MULT_EQUAL
    | DIV_EQUAL;

basicTypeName:
    'numb'
    | 'string'
    | 'column'
    | 'row'
    | 'table';

    
boolSign:
    EQUAL
    | NOT_EQUAL
    | LESS_EQUAL
    | GREATER_EQUAL
    | LESS
    | GREATER
    | AND
    | OR
    | NOT
    ;
    
numbSign: 
    PLUS
    | MINUS
    | DIV
    | FULL_DIV
    | MULT
    ;
    
boolNumbSign:
    boolSign
    | numbSign
    ;
    
basicType:
    ID
    | NUMBER
    | STRING
    | COLUMN
    | ROW
    | TABLE;
    
returnType:
    basicType
    | builtinFuncStmt 
    | indexStmt
    ;
    
numbExpr:
    returnType
    | numbExpr boolNumbSign
        numbExpr;
        
boolExpr:
    numbExpr boolSign numbExpr;
    
ifElseStmt:
    IF boolExpr '{' 
        funcStat*
    '}'
    (ELSE IF boolExpr '{'
        funcStat*
    '}')*
    (ELSE '{'
        funcStat*
    '}')*
    ;
    
// while stat

whileStmt:
    WHILE LPAREN boolExpr RPAREN
    '{' funcStat* '}';
    
// until stat

untilStmt:
    '{' funcStat* '}'
    UNTIL LPAREN
        boolExpr
            RPAREN;


// function + index
custFuncCall:
    ID LPAREN numbExpr?
     (COMMA numbExpr)* RPAREN;
    

indexStmt: 
    (ID|
        builtinFuncStmt)
    (L_SQBRACK 
            (numbExpr)?
        P_SQBRACK)+
    ;

listStmt : L_SQBRACK 
    (listStmt|NUMBER|STRING)?
    (COMMA (listStmt|NUMBER|
                    STRING))* 
        P_SQBRACK;

builtinFuncStmt:
    lengthStmt
    | createRowStmt
    | custFuncCall
    | createTablStmt
    | createColStmt
    | readStrStmt
    | copyStmt
    | minMaxFuncStmt
    | delFuncStmt
    | reshapeStmt
    | insertStmt
    | findStmt;

lengthStmt: LENGTH LPAREN 
    numbExpr RPAREN;

returnStmt: RETURN numbExpr SEMI;

createRowStmt: CREATE_ROW 
    LPAREN NUMBER?
        (COMMA listStmt)?
        RPAREN;

createTablStmt: CREATE_TABLE
    LPAREN NUMBER? 
        (COMMA NUMBER)*
        (COMMA listStmt)?
    RPAREN;
    
createColStmt: CREATE_COL
    LPAREN NUMBER?
    (COMMA listStmt)? RPAREN;

copyStmt: COPY LPAREN
    ID RPAREN;
    
minMaxFunc:
    MAX
    | MIN
    | MAXLEN
    | MINLEN;
    
minMaxFuncStmt:
    minMaxFunc
    LPAREN numbExpr RPAREN;
    
delFunc:
    DEL_COL
    | DEL_ROW
    | DEL;

delFuncStmt:
    delFunc LPAREN
        numbExpr COMMA
        numbExpr RPAREN;
    
reshapeStmt:
    RESHAPE LPAREN numbExpr
    COMMA numbExpr COMMA
    numbExpr RPAREN;
    
insertStmt: 
    INSERT LPAREN numbExpr
    COMMA numbExpr
    COMMA numbExpr RPAREN;

findStmt:
    FIND LPAREN numbExpr
    COMMA numbExpr RPAREN;

// output thread
printStmt: PRINT '(' numbExpr ')';
    
// input thread
readStrStmt: READ_STRING
    LPAREN RPAREN;
    

