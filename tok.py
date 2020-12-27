from enum import Enum


class Token(Enum):
    VAR = 1                         # identifier -> global/local variables, parameters
    KW_INT = 2                      # int
    KW_IF = 3
    KW_WHILE = 4
    KW_FOR = 5
    KW_BREAK = 6
    KW_RETURN = 7
    KW_CONTINUE = 8
    OP_ADD = 9                      # arith operator: +, -, *, /
    OP_SUB = 10
    OP_MUL = 11
    OP_DIV = 12
    OP_GT = 13                      # relation operator: >, <, ==, !=
    OP_LT = 14
    OP_EQ = 15
    OP_NOT_EQ = 16
    CONST_VAL = 17                  # constant integer
    SIGN_SEMICOLON = 18             # ; and ,
    SIGN_COMA = 19
    SIGN_LEFT_BRACE = 20            # { and }
    SIGN_RIGHT_BRACE = 21
    SIGN_LEFT_BRACKET = 22          # [ and ]
    SIGN_RIGHT_BRACKET = 23
    SIGN_LEFT_PARENTHESIS = 24      # ( and )
    SIGN_RIGHT_PARENTHESIS = 25
    SIGN_ASSIGN = 26                # assignment
    OP_ADDR = 27                    # &
    KW_ELSE = 28                    # else
