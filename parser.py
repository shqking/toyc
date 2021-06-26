import os
import sys

import tu
from tu import logger
from tu import SUBPHASE_TAG_STR
from tok import Token
from astnode import ASTNode
import lexer


################################
# global index

tok_inx = 0
astnode_inx = -1


################################
# macros to access toks and astnodes

def CUR_TOK_TYPE():
    global tok_inx
    return tu.toks[tok_inx][0]


def CUR_TOK():
    global tok_inx
    return tu.toks[tok_inx]


def MOVE_NEXT():
    global tok_inx
    tok_inx = tok_inx + 1


# match current token type. Return this token if succeed.
def GET_TOK(token_type):
    tok = CUR_TOK()
    if CUR_TOK_TYPE() != token_type:
        logger.error("Mismatch token: " + lexer.get_token_info(tok, True))
        sys.exit()
    MOVE_NEXT()
    return tok


# append new astnode into tu.ast and return the index.
def NEW_NODE(node):
    global astnode_inx
    astnode_inx = astnode_inx + 1
    tu.ast.append(node)
    return astnode_inx


################################
# Algorithm: LL(1)

def parse_arglist(arg_list):
    if CUR_TOK_TYPE() == Token.SIGN_COMA:
        MOVE_NEXT()
        expr = parse_expr()
        arg_list.append(expr)
        return parse_arglist(arg_list)
    else:
        return arg_list


def parse_args():
    if CUR_TOK_TYPE() == Token.SIGN_LEFT_BRACKET:
        return -1
    else:
        expr = parse_expr()
        arg_list = parse_arglist([expr])
        return NEW_NODE([ASTNode.ARGS, len(arg_list), arg_list])


def parse_val_expr():
    if CUR_TOK_TYPE() == Token.CONST_VAL:
        cst = CUR_TOK()
        MOVE_NEXT()
        return NEW_NODE([ASTNode.CST, cst])

    var = GET_TOK(Token.VAR)

    if CUR_TOK_TYPE() == Token.SIGN_LEFT_BRACKET:
        MOVE_NEXT()
        expr = parse_expr()
        _ = GET_TOK(Token.SIGN_RIGHT_BRACKET)
        return NEW_NODE([ASTNode.ARRAY_ELMT, var, expr])
    elif CUR_TOK_TYPE() == Token.SIGN_LEFT_PARENTHESIS:
        MOVE_NEXT()
        args = parse_args()
        _ = GET_TOK(Token.SIGN_RIGHT_PARENTHESIS)
        return NEW_NODE([ASTNode.FCALL, var, args])
    else:
        return NEW_NODE([ASTNode.VAR, var])


def parse_factor():
    if CUR_TOK_TYPE() == Token.OP_MUL \
            or CUR_TOK_TYPE() == Token.OP_SUB \
            or CUR_TOK_TYPE() == Token.OP_ADDR:
        unary_op = CUR_TOK()
        MOVE_NEXT()
        val_expr = parse_val_expr()
        return NEW_NODE([ASTNode.EXPR_UNARY, unary_op, val_expr])
    else:
        return parse_val_expr()


def parse_multail(lval):
    if CUR_TOK_TYPE() == Token.OP_MUL \
            or CUR_TOK_TYPE() == Token.OP_DIV:
        mul_div_op = CUR_TOK()
        MOVE_NEXT()
        fact = parse_factor()
        fact_or_mul = parse_multail(fact)
        return NEW_NODE([ASTNode.EXPR_BINARY, mul_div_op, lval, fact_or_mul])
    else:
        return lval


def parse_mul_expr():
    fact = parse_factor()
    fact_or_mul = parse_multail(fact)
    return fact_or_mul


def parse_addtail(lval):
    if CUR_TOK_TYPE() == Token.OP_ADD \
            or CUR_TOK_TYPE() == Token.OP_SUB:
        add_sub_op = CUR_TOK()
        MOVE_NEXT()
        mul_expr = parse_mul_expr()
        mul_or_add = parse_addtail(mul_expr)
        return NEW_NODE([ASTNode.EXPR_BINARY, add_sub_op, lval, mul_or_add])
    else:
        return lval


def parse_add_expr():
    mul_expr = parse_mul_expr()
    mul_or_add = parse_addtail(mul_expr)
    return mul_or_add


def parse_cmptail(lval):
    if CUR_TOK_TYPE() == Token.OP_GT         \
            or CUR_TOK_TYPE() == Token.OP_LT \
            or CUR_TOK_TYPE() == Token.OP_EQ \
            or CUR_TOK_TYPE() == Token.OP_NOT_EQ:
        rel_op = CUR_TOK()
        MOVE_NEXT()
        add_expr = parse_add_expr()
        add_or_cmp = parse_cmptail(add_expr)
        return NEW_NODE([ASTNode.EXPR_BINARY, rel_op, lval, add_or_cmp])
    else:
        return lval


def parse_cmp_expr():
    add_expr = parse_add_expr()
    add_or_cmp = parse_cmptail(add_expr)
    return add_or_cmp


def parse_asstail(lval):
    if CUR_TOK_TYPE() == Token.SIGN_ASSIGN:
        MOVE_NEXT()
        cmp_expr = parse_cmp_expr()
        cmp_or_ass = parse_asstail(cmp_expr)
        return NEW_NODE([ASTNode.EXPR_ASSIGN, lval, cmp_or_ass])
    else:
        return lval


def parse_expr():
    cmp_expr = parse_cmp_expr()
    cmp_or_ass = parse_asstail(cmp_expr)
    return cmp_or_ass


def parse_para(para_list):
    type = GET_TOK(Token.KW_INT)

    is_ptr = 0
    if CUR_TOK_TYPE() == Token.OP_MUL:
        is_ptr = 1
        MOVE_NEXT()

    var = GET_TOK(Token.VAR)
    para = NEW_NODE([ASTNode.DEF_PARA, type, var, is_ptr])
    para_list.append(para)

    if CUR_TOK_TYPE() == Token.SIGN_COMA:
        MOVE_NEXT()
        return parse_para(para_list)
    else:
        return para_list


def parse_init_expr():
    is_assign = 0
    node = -1

    if CUR_TOK_TYPE() == Token.SIGN_ASSIGN:
        is_assign = 1
        MOVE_NEXT()
        node = parse_expr()

    return is_assign, node


def parse_def(type, is_global):
    if CUR_TOK_TYPE() == Token.OP_MUL:
        MOVE_NEXT()

        var = GET_TOK(Token.VAR)
        is_assign, node = parse_init_expr()
        _ = GET_TOK(Token.SIGN_SEMICOLON)

        return NEW_NODE([ASTNode.DEF_PTR, type, var, is_global, is_assign, node])
    elif CUR_TOK_TYPE() == Token.VAR:
        var = CUR_TOK()
        MOVE_NEXT()

        if CUR_TOK_TYPE() == Token.SIGN_LEFT_BRACKET:
            MOVE_NEXT()

            cst = GET_TOK(Token.CONST_VAL)
            _ = GET_TOK(Token.SIGN_LEFT_BRACKET)
            _ = GET_TOK(Token.SIGN_SEMICOLON)

            return NEW_NODE([ASTNode.DEF_ARRAY, type, var, is_global, cst])
        elif is_global == 1 and CUR_TOK_TYPE() == Token.SIGN_LEFT_PARENTHESIS:
            MOVE_NEXT()

            para_list = list()
            if CUR_TOK_TYPE() != Token.SIGN_RIGHT_PARENTHESIS:
                para_list = parse_para(para_list)

            _ = GET_TOK(Token.SIGN_RIGHT_PARENTHESIS)
            fun_body = parse_block()

            return NEW_NODE([ASTNode.DEF_FUN, type, var, len(para_list), para_list, fun_body])
        else:
            is_assign, node = parse_init_expr()
            _ = GET_TOK(Token.SIGN_SEMICOLON)

            return NEW_NODE([ASTNode.DEF_VAR, type, var, is_global, is_assign, node])
    else:
        logger.error("Mismatch token")
        sys.exit()


def parse_stmtlist():
    if CUR_TOK_TYPE() == Token.KW_INT:
        type = CUR_TOK()
        MOVE_NEXT()

        node = parse_def(type, 0)
        next = parse_stmtlist()
        return NEW_NODE([ASTNode.STMTLIST, node, next])
    elif CUR_TOK_TYPE() == Token.SIGN_RIGHT_BRACE:
        return -1   # NIL
    elif CUR_TOK_TYPE() == Token.KW_BREAK:
        tok = CUR_TOK()
        MOVE_NEXT()
        _ = GET_TOK(Token.SIGN_SEMICOLON)

        brk_stmt = NEW_NODE([ASTNode.STMT_BRK, tok])
        next = parse_stmtlist()
        return NEW_NODE([ASTNode.STMTLIST, brk_stmt, next])
    elif CUR_TOK_TYPE() == Token.KW_CONTINUE:
        tok = CUR_TOK()
        MOVE_NEXT()
        _ = GET_TOK(Token.SIGN_SEMICOLON)

        cont_stmt = NEW_NODE([ASTNode.STMT_CONTINUE, tok])
        next = parse_stmtlist()
        return NEW_NODE([ASTNode.STMTLIST, cont_stmt, next])
    elif CUR_TOK_TYPE() == Token.KW_RETURN:
        MOVE_NEXT()
        ret_expr = parse_expr()
        _ = GET_TOK(Token.SIGN_SEMICOLON)

        ret_stmt = NEW_NODE([ASTNode.STMT_RET, ret_expr])
        next = parse_stmtlist()
        return NEW_NODE([ASTNode.STMTLIST, ret_stmt, next])
    elif CUR_TOK_TYPE() == Token.KW_IF:
        MOVE_NEXT()
        _ = GET_TOK(Token.SIGN_LEFT_PARENTHESIS)
        if_expr = parse_expr()
        _ = GET_TOK(Token.SIGN_RIGHT_PARENTHESIS)
        if_body = parse_block()

        has_else = 0
        else_body = -1
        if CUR_TOK_TYPE() == Token.KW_ELSE:
            MOVE_NEXT()
            has_else = 1
            else_body = parse_block()

        if_stmt = NEW_NODE(
            [ASTNode.STMT_IF, if_expr, if_body, has_else, else_body])
        next = parse_stmtlist()
        return NEW_NODE([ASTNode.STMTLIST, if_stmt, next])
    elif CUR_TOK_TYPE() == Token.KW_FOR:
        MOVE_NEXT()
        _ = GET_TOK(Token.SIGN_LEFT_PARENTHESIS)
        init_expr = parse_expr()
        _ = GET_TOK(Token.SIGN_SEMICOLON)
        bound_expr = parse_expr()
        _ = GET_TOK(Token.SIGN_SEMICOLON)
        update_expr = parse_expr()
        _ = GET_TOK(Token.SIGN_RIGHT_PARENTHESIS)
        body = parse_block()

        for_stmt = NEW_NODE([ASTNode.STMT_FOR, init_expr,
                             bound_expr, update_expr, body])
        next = parse_stmtlist()
        return NEW_NODE([ASTNode.STMTLIST, for_stmt, next])
    elif CUR_TOK_TYPE() == Token.KW_WHILE:
        MOVE_NEXT()
        _ = GET_TOK(Token.SIGN_LEFT_PARENTHESIS)
        cond_expr = parse_expr()
        _ = GET_TOK(Token.SIGN_RIGHT_PARENTHESIS)
        body = parse_block()

        while_stmt = NEW_NODE([ASTNode.STMT_FOR, cond_expr, body])
        next = parse_stmtlist()
        return NEW_NODE([ASTNode.STMTLIST, while_stmt, next])
    elif CUR_TOK_TYPE() == Token.SIGN_SEMICOLON:
        tok = CUR_TOK()
        MOVE_NEXT()

        empty_stmt = NEW_NODE([ASTNode.STMT_EMPTY, tok])
        next = parse_stmtlist()
        return NEW_NODE([ASTNode.STMTLIST, empty_stmt, next])
    else:
        expr = parse_expr()
        _ = GET_TOK(Token.SIGN_SEMICOLON)
        next = parse_stmtlist()
        return NEW_NODE([ASTNode.STMTLIST, expr, next])


def parse_block():
    _ = GET_TOK(Token.SIGN_LEFT_BRACE)
    node = parse_stmtlist()
    _ = GET_TOK(Token.SIGN_RIGHT_BRACE)

    return NEW_NODE([ASTNode.BLOCK, node])


# node: global variable | function
def parse_program():
    # check whether there is available token
    global tok_inx
    if tok_inx == len(tu.toks):
        return -1

    type = GET_TOK(Token.KW_INT)
    node = parse_def(type, 1)
    next = parse_program()

    return NEW_NODE([ASTNode.DEF_PROG, node, next])


# tu.ast: [node, node, node, ..., ROOT]
def do_parse():
    parse_program()
    return


################################
# dump AST

def get_astnode_info(node):
    node_info = ''
    if node[0] == ASTNode.DEF_PROG:
        node_info = "%s, global def: %d, next: %d" % (
            node[0].name, node[1], node[2])
    elif node[0] == ASTNode.DEF_VAR \
            or node[0] == ASTNode.DEF_PTR:
        node_info = "%s, type: %s, var: %s, is_global: %d, is_assign: %d, expr: %d" % (
            node[0].name,
            lexer.get_token_info(node[1]),
            lexer.get_token_info(node[2]),
            node[3], node[4], node[5])
    elif node[0] == ASTNode.DEF_ARRAY:
        node_info = "%s, type: %s, var: %s, is_global: %d, size: %s" % (
            node[0].name,
            lexer.get_token_info(node[1]),
            lexer.get_token_info(node[2]),
            node[3],
            lexer.get_token_info(node[4]))
    elif node[0] == ASTNode.DEF_FUN:
        node_info = "%s, type: %s, var: %s, para_num: %d, paralist: %s, body: %d" % (
            node[0].name,
            lexer.get_token_info(node[1]),
            lexer.get_token_info(node[2]),
            node[3], node[4], node[5])
    elif node[0] == ASTNode.DEF_PARA:
        node_info = "%s, type: %s, var: %s, is_ptr: %d" % (
            node[0].name,
            lexer.get_token_info(node[1]),
            lexer.get_token_info(node[2]),
            node[3])
    elif node[0] == ASTNode.BLOCK:
        node_info = "%s, stmt_list: %d" % (node[0].name, node[1])
    elif node[0] == ASTNode.STMTLIST:
        node_info = "%s, stmt: %d, next: %d" % (node[0].name, node[1], node[2])
    elif node[0] == ASTNode.STMT_BRK \
            or node[0] == ASTNode.STMT_CONTINUE \
            or node[0] == ASTNode.STMT_EMPTY:
        node_info = "%s, stmt: %s" % (
            node[0].name,
            lexer.get_token_info(node[1]))
    elif node[0] == ASTNode.STMT_RET:
        node_info = "%s, ret_expr: %d" % (node[0].name, node[1])
    elif node[0] == ASTNode.STMT_IF:
        node_info = "%s, if_expr: %d, if_body: %d, has_else: %d, else_body: %d" % (
            node[0].name, node[1], node[2], node[3], node[4])
    elif node[0] == ASTNode.STMT_FOR:
        node_info = "%s, init_expr: %d, bound_expr: %d, update_expr: %d, body: %d" % (
            node[0].name, node[1], node[2], node[3], node[4])
    elif node[0] == ASTNode.STMT_WHILE:
        node_info = "%s, cond_expr: %d, body: %d" % (
            node[0].name, node[1], node[2])
    elif node[0] == ASTNode.EXPR_ASSIGN:
        node_info = "%s, lval: %d, expr: %d" % (
            node[0].name, node[1], node[2])
    elif node[0] == ASTNode.EXPR_BINARY:
        node_info = "%s, op: %s, lval: %d, expr: %d" % (
            node[0].name,
            lexer.get_token_info(node[1]),
            node[2], node[3])
    elif node[0] == ASTNode.EXPR_UNARY:
        node_info = "%s, op: %s, val: %d" % (
            node[0].name,
            lexer.get_token_info(node[1]),
            node[2])
    elif node[0] == ASTNode.CST:
        node_info = "%s, cst: %s" % (
            node[0].name,
            lexer.get_token_info(node[1]))
    elif node[0] == ASTNode.ARRAY_ELMT:
        node_info = "%s, array: %s, index: %d" % (
            node[0].name,
            lexer.get_token_info(node[1]),
            node[2])
    elif node[0] == ASTNode.FCALL:
        node_info = "%s, function: %s, arglist: %d" % (
            node[0].name,
            lexer.get_token_info(node[1]),
            node[2])
    elif node[0] == ASTNode.VAR:
        node_info = "%s, var: %s" % (
            node[0].name,
            lexer.get_token_info(node[1]))
    elif node[0] == ASTNode.ARGS:
        node_info = "%s, arg_num: %d, arglist: %s" % (
            node[0].name, node[1], node[2])
    else:
        logger.error("Invalid AST node type.")
        sys.exit()
    return node_info


def dump_ast():
    logger.debug("%d astnode:" % len(tu.ast))
    inx = 0
    for node in tu.ast:
        inx_str = "%d-th node: " % (inx)
        node_info = get_astnode_info(node)

        logger.debug(inx_str + node_info)
        inx = inx + 1
    return


################################
# main entry

def parse():
    # check whether lexer succeeds
    if len(tu.toks) == 0:
        logger.error("No available tokens.")
        sys.exit()

    logger.debug(SUBPHASE_TAG_STR)
    logger.debug('Start to parse')
    do_parse()
    logger.debug('Parsing succeeds')

    # dump the ast
    logger.debug(SUBPHASE_TAG_STR)
    logger.debug('Dump the AST')
    ast_str = dump_ast()

    # TODO: generate the checksum of ast
    # if tu.CHECK_FLAG_AST:
    #    import hashlib

    # finish
    logger.info("Done")
