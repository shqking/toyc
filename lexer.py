import tu
from tu import logger
from tu import SUBPHASE_TAG_STR
import os
import sys

from tok import Token

'''
    token = (token_type, content, row_begin, row_end, col_begin, col_end)
    token_type: enum
    content: currently valid for identifier; None otherwise
'''

single_char_tok_map = {
    '{': Token.SIGN_LEFT_BRACE,
    '}': Token.SIGN_RIGHT_BRACE,
    '(': Token.SIGN_LEFT_PARENTHESIS,
    ')': Token.SIGN_RIGHT_PARENTHESIS,
    '[': Token.SIGN_LEFT_BRACKET,
    ']': Token.SIGN_RIGHT_BRACKET,
    ';': Token.SIGN_SEMICOLON,
    ',': Token.SIGN_COMA,
    '>': Token.OP_GT,
    '<': Token.OP_LT,
    '+': Token.OP_ADD,
    '-': Token.OP_SUB,
    '*': Token.OP_MUL,
    '/': Token.OP_DIV,
    '&': Token.OP_ADDR
}

keyword_tok_map = {
    'if': Token.KW_IF,
    'else': Token.KW_ELSE,
    'for': Token.KW_FOR,
    'while': Token.KW_WHILE,
    'return': Token.KW_RETURN,
    'int': Token.KW_INT,
    'continue': Token.KW_CONTINUE,
    'break': Token.KW_BREAK
}

whitespace = [' ', '\t', '\b', '\n']
chars_per_tab = 4


def is_digit_or_letter(ch):
    if ch >= '0' and ch <= '9':
        return True
    if ch >= 'a' and ch <= 'z':
        return True
    if ch >= 'A' and ch <= 'Z':
        return True
    return False


def dump_checksum(checksum_str):
    with open('/tmp/toyc.lex', 'w') as file:
        file.write(checksum_str)
        file.close()


def read_line(line, lineno):
    num = len(line)
    inx = 0
    col_b = 1
    while inx < num:
        cur_char = line[inx]
        if cur_char in whitespace:
            logger.debug("\t%d-th char at col %d: WS" % (inx, col_b))
        else:
            logger.debug("\t%d-th char at col %d: %c" % (inx, col_b, cur_char))

        # single character token
        if cur_char in single_char_tok_map.keys():
            logger.debug("\t\tis single character token.")
            token_type = single_char_tok_map[cur_char]
            token = [token_type, None, lineno, lineno, col_b, col_b]
            tu.toks.append(token)
            inx = inx + 1
            col_b = col_b + 1
            continue

        # escape whitespace
        if cur_char in whitespace:
            while cur_char in whitespace:
                logger.debug("\t\tis whitespace.")
                if cur_char == '\t':
                    col_b = col_b + chars_per_tab
                else:
                    col_b = col_b + 1
                inx = inx + 1
                if inx == num:
                    break
                cur_char = line[inx]
            if inx == num:
                break
            continue

        # = and ==
        if cur_char == '=':
            if line[inx + 1] == '=':
                logger.debug("\t\tis ==")
                token = [Token.OP_EQ, None,
                         lineno, lineno, col_b, col_b + 1]
                tu.toks.append(token)
                inx = inx + 2
                col_b = col_b + 2
            else:
                logger.debug("\t\tis =")
                token = [Token.SIGN_ASSIGN, None, lineno, lineno, col_b, col_b]
                tu.toks.append(token)
                inx = inx + 1
                col_b = col_b + 1
            continue

        # !=
        if cur_char == '!':
            if line[inx + 1] == '=':
                logger.debug("\t\tis !=")
                token = [Token.OP_NOT_EQ, None,
                         lineno, lineno, col_b, col_b + 1]
                tu.toks.append(token)
                inx = inx + 2
                col_b = col_b + 2
                continue
            else:
                err_str = "tokenization failed at line:%d, column:%d" % (
                    lineno, col_b + 1)
                if tu.CHECK_FLAG_LEX:
                    dump_checksum(err_str)
                logger.error(err_str)
                sys.exit()

        # keywrod/identifier/constant
        if is_digit_or_letter(cur_char):
            prev_inx = inx
            while is_digit_or_letter(cur_char):
                inx = inx + 1
                if inx == num:
                    break
                cur_char = line[inx]
            tok_str = line[prev_inx: inx]
            prev_col_b = col_b
            col_b = col_b + inx - prev_inx
            logger.debug("\t\tis string:%s" % tok_str)

            if tok_str in keyword_tok_map.keys():
                token_type = keyword_tok_map[tok_str]
                token = [token_type, None, lineno,
                         lineno, prev_col_b, col_b - 1]
            elif tok_str.isdigit():
                token_type = Token.CONST_VAL
                token = [token_type, None, lineno,
                         lineno, prev_col_b, col_b - 1]
            else:
                token_type = Token.VAR
                token = [token_type, tok_str, lineno,
                         lineno, prev_col_b, col_b - 1]
            tu.toks.append(token)
            continue

        # unrecoginized token
        err_str = "unrecognized token at line:%d, column:%d" % (lineno, col_b)
        if tu.CHECK_FLAG_LEX:
            dump_checksum(err_str)
        logger.error(err_str)
        sys.exit()


def dump_tokens():
    tokens_str = ""
    logger.debug("%d tokens:" % len(tu.toks))
    inx = 0
    for tok in tu.toks:
        tok_info = ''
        if tok[0] == Token.VAR:
            tok_info = "%d-th token: %s, %s, (%d,%d,%d,%d)" % (
                inx, tok[0].name, tok[1], tok[2], tok[3], tok[4], tok[5])
        else:
            tok_info = "%d-th token: %s, (%d,%d,%d,%d)" % (inx,
                                                           tok[0].name, tok[2], tok[3], tok[4], tok[5])
        logger.debug(tok_info)
        tokens_str += tok_info + '\t'
        inx = inx + 1
    return tokens_str


def lex():
    logger.debug(SUBPHASE_TAG_STR)
    logger.debug('Start to tokenize')
    with open(tu.src_file_name, 'r') as src_file:
        lines = src_file.readlines()
        lineno = 1
        for line in lines:
            logger.debug("analyzing line: %d" % lineno)
            read_line(line, lineno)
            lineno = lineno + 1
        src_file.close()

    # dump all the tokens
    logger.debug(SUBPHASE_TAG_STR)
    logger.debug('Get all the tokens')
    tokens_str = dump_tokens()

    # generate the checksum and dump it
    if tu.CHECK_FLAG_LEX:
        import hashlib
        tokens_checksum = hashlib.md5(
            tokens_str.encode('utf-8')).hexdigest()
        dump_checksum(tokens_checksum)

    # finish
    logger.info('Done')
