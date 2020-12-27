# toyc：a toy compiler for C subset


##### Lexer

The following tokens are supported currently. See `tok.py` and `lexer.py` for more details.

```bash
# Keywords: int, if, while, for, break, return, continue, else
KW_INT: 'int'
KW_IF: 'if'
KW_ELSE: 'else'
KW_WHILE: 'while'
KW_FOR: 'for'
KW_BREAK: 'break'
KW_RETURN: 'return'
KW_CONTINUE: 'continue'

# Arithmetic operators
OP_ADD: '+'
OP_SUB: '-'
OP_MUL: '*'  # also used to indicate 'star' for pointers
OP_DIV: '/'

# Relation operators
OP_GT: '>'
OP_LT: '<'
OP_EQ: '=='
OP_NOT_EQ: '!='

# Address operator
OP_ADDR: '&'

# Specific signs
SIGN_SEMICOLON: ';'
SIGN_COMA: ','
SIGN_LEFT_BRACE: '{'
SIGN_RIGHT_BRACE: '}'
SIGN_LEFT_BRACKET: '['
SIGN_RIGHT_BRACKET: ']'
SIGN_LEFT_PARENTHESIS: '('
SIGN_RIGHT_PARENTHESIS: ')'
SIGN_ASSIGN: '=' # assignment

# Constant value
CONST_VAL: [0-9]+ # only decimal integers are supported.

# Identifiers
VAR: [0-9, a-z, A-Z]+	# exclude Keywords and CONST_VAL
```



The following tokens would be produced for `test/fib.c`

```bash
Get all the tokens
43 tokens:
0-th token: KW_INT, (1,1,1,3)
1-th token: VAR, fib, (1,1,5,7)
2-th token: SIGN_LEFT_PARENTHESIS, (1,1,8,8)
3-th token: KW_INT, (1,1,9,11)
4-th token: VAR, num, (1,1,13,15)
5-th token: SIGN_RIGHT_PARENTHESIS, (1,1,16,16)
6-th token: SIGN_LEFT_BRACE, (2,2,1,1)
7-th token: KW_IF, (3,3,5,6)
8-th token: SIGN_LEFT_PARENTHESIS, (3,3,8,8)
9-th token: VAR, num, (3,3,9,11)
10-th token: OP_EQ, (3,3,13,14)
11-th token: CONST_VAL, (3,3,16,16)
12-th token: SIGN_RIGHT_PARENTHESIS, (3,3,17,17)
13-th token: KW_RETURN, (4,4,9,14)
14-th token: CONST_VAL, (4,4,16,16)
15-th token: SIGN_SEMICOLON, (4,4,17,17)
16-th token: KW_ELSE, (5,5,5,8)
17-th token: KW_IF, (5,5,10,11)
18-th token: SIGN_LEFT_PARENTHESIS, (5,5,13,13)
19-th token: VAR, num, (5,5,14,16)
20-th token: OP_EQ, (5,5,18,19)
21-th token: CONST_VAL, (5,5,21,21)
22-th token: SIGN_RIGHT_PARENTHESIS, (5,5,22,22)
23-th token: KW_RETURN, (6,6,9,14)
24-th token: CONST_VAL, (6,6,16,16)
25-th token: SIGN_SEMICOLON, (6,6,17,17)
26-th token: KW_ELSE, (7,7,5,8)
27-th token: KW_RETURN, (8,8,9,14)
28-th token: VAR, fib, (8,8,16,18)
29-th token: SIGN_LEFT_PARENTHESIS, (8,8,19,19)
30-th token: VAR, num, (8,8,20,22)
31-th token: OP_SUB, (8,8,24,24)
32-th token: CONST_VAL, (8,8,26,26)
33-th token: SIGN_RIGHT_PARENTHESIS, (8,8,27,27)
34-th token: OP_ADD, (8,8,29,29)
35-th token: VAR, fib, (8,8,31,33)
36-th token: SIGN_LEFT_PARENTHESIS, (8,8,34,34)
37-th token: VAR, num, (8,8,35,37)
38-th token: OP_SUB, (8,8,39,39)
39-th token: CONST_VAL, (8,8,41,41)
40-th token: SIGN_RIGHT_PARENTHESIS, (8,8,42,42)
41-th token: SIGN_SEMICOLON, (8,8,43,43)
42-th token: SIGN_RIGHT_BRACE, (9,9,1,1)
```



##### Parser

TODO