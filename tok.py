from enum import Enum


class Token(Enum):
    VAR = 1                         # identifier -> global/local variables, parameters
    KW_INT = 2                      # int
    KW_IF = 3
    KW_ELSE = 4
    KW_WHILE = 5
    KW_FOR = 6
    KW_BREAK = 7
    KW_RETURN = 8
    KW_CONTINUE = 9
    OP_ADD = 10                     # arith operator: +, -, *, /
    OP_SUB = 11
    OP_MUL = 12
    OP_DIV = 13
    OP_GT = 14                      # relation operator: >, <, ==, !=
    OP_LT = 15
    OP_EQ = 16
    OP_NOT_EQ = 17
    OP_ADDR = 18                    # &
    CONST_VAL = 19                  # constant integer
    SIGN_SEMICOLON = 20             # ; and ,
    SIGN_COMA = 21
    SIGN_LEFT_BRACE = 22            # { and }
    SIGN_RIGHT_BRACE = 23
    SIGN_LEFT_BRACKET = 24          # [ and ]
    SIGN_RIGHT_BRACKET = 25
    SIGN_LEFT_PARENTHESIS = 26      # ( and )
    SIGN_RIGHT_PARENTHESIS = 27
    SIGN_ASSIGN = 28                # assignment
