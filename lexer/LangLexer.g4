  lexer grammar LangLexer;

  // number expressions
  // bool signs
  AND : '&' ;
  OR : '|' ;
  NOT : '!' ;
  EQUAL: '==';
  NOT_EQUAL: '!=';
  LESS_EQUAL: '<=';
  GREATER_EQUAL: '>=';
  LESS: '<';
  GREATER: '>';

  // not bool signs
  PLUS : '+' ;
  MINUS : '-' ;
  DIV : '/';
  FULL_DIV : '//';
  MULT : '*';


  // 
  COMMA : ',' ;
  SEMI : ';' ;
  LPAREN : '(' ;
  RPAREN : ')' ;
  LCURLY : '{' ;
  RCURLY : '}' ;
  L_SQBRACK : '[' ;
  P_SQBRACK : ']' ;

  // assign signs
  PLUS_EQUAL : '+=';
  ASSIGN : '=' ;
  MINUS_EQUAL : '-=';
  MULT_EQUAL : '*=' ;
  DIV_EQUAL : '/=' ;


  // built-in keywords
  FUNCTION : 'function' ;
  FOR : 'for' ;
  RETURN : 'return' ;
  IF : 'if' ;
  ELSE : 'else' ;
  WHILE : 'while' ;
  UNTIL : 'until' ;
  COMMENT :  '#' ~( '\r' | '\n' )*;


  // built-in functions 
  PRINT: 'print';
  LENGTH: 'length';
  RESHAPE: 'reshape';
  DEL_COL: 'del_col';
  DEL_ROW: 'del_row';
  DEL: 'del';
  INSERT: 'insert';
  MAX: 'max';
  MIN: 'min';
  MAXLEN: 'maxlen';
  MINLEN: 'minlen';
  FIND: 'find';
  CREATE_ROW: 'create_row';
  CREATE_TABLE: 'create_table';
  CREATE_COL: 'create_column';
  READ_STRING: 'read_string';
  COPY: 'copy';


  // built-in types
  NUMBER_type : 'numb' ;
  STRING_type : 'string' ;
  TABLE : 'table';
  COLUMN : 'column';
  ROW : 'row';
  VOID : 'void';
  
  
  NUMBER: (PLUS | MINUS)? [0-9]+ ('.' [0-9]+)? 
  ([eE] (PLUS | MINUS)? [0-9]+)?;
  STRING : '"' ( ~["\\] | '\\' . 
                  )*'"';
                  
  ID: [a-zA-Z_][a-zA-Z_0-9]* ;
  WS: [ \t\n\r\f]+ -> skip ;


  CONST_NUMBER : 'const' NUMBER;
  CONST_STRING : 'const' STRING;

